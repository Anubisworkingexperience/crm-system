from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel, Field
from app.grpc.order_client import OrderClient
from grpc import aio, StatusCode

router = APIRouter(prefix="/orders", tags=["orders"])

class OrderIn(BaseModel):
    customer_id: str
    product_name: str = Field(min_length=1, max_length=255)
    price: float = Field(ge=0)

@router.post("", status_code=201)
async def create_order(data: OrderIn, request: Request):
    client: OrderClient = request.app.state.order_client
    try:
        res = await client.create_order(data.customer_id, data.product_name, float(data.price))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
   
    return {
        "id": res.id,
        "customer_id": res.customer_id,
        "product_name": res.product_name,
        "price": res.price,
        "created_at": res.created_at
    }

@router.get("/{order_id}")
async def get_order(order_id: str, request: Request):
    client: OrderClient = request.app.state.order_client
    try:
        o = await client.get_order(order_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": o.id, "customer_id": o.customer_id, "product_name": o.product_name,
        "price": o.price, "created_at": o.created_at
    }

@router.get("/by-customer/{customer_id}")
async def get_customer_orders(
    customer_id: str,
    request: Request,
):
    client: OrderClient = request.app.state.order_client
    try:
        res = await client.get_customer_orders(customer_id)
    except aio.AioRpcError as e:
        if e.code() == StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
        raise HTTPException(status_code=500, detail="grpc error: " + e.details())
    
    return {
        "orders": [
            {
                "id": o.id,
                "customer_id": o.customer_id,
                "product_name": o.product_name,
                "price": o.price,
                "created_at": o.created_at
            } for o in res.orders
        ]
    }
