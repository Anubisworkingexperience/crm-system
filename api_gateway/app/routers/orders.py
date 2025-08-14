from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel, Field
from app.grpc.order_client import OrderClient

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
    o = res.order
    return {
        "id": o.id,
        "customer_id": o.customer_id,
        "product_name": o.product_name,
        "price": o.price,
        "created_at": o.created_at.ToDatetime().isoformat()
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
        "price": o.price, "created_at": o.created_at.ToDatetime().isoformat()
    }

@router.get("/by-customer/{customer_id}")
async def get_customer_orders(
    customer_id: str,
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    client: OrderClient = request.app.state.order_client
    res = await client.get_customer_orders(customer_id, page, page_size)
    return {
        "total": res.total,
        "orders": [
            {
                "id": o.id,
                "customer_id": o.customer_id,
                "product_name": o.product_name,
                "price": o.price,
                "created_at": o.created_at.ToDatetime().isoformat()
            } for o in res.orders
        ]
    }
