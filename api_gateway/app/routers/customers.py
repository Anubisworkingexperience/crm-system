from fastapi import APIRouter, Depends, HTTPException, Request, Query
from pydantic import BaseModel, EmailStr
from app.grpc.customer_client import CustomerClient

router = APIRouter(prefix="/customers", tags=["customers"])

class CustomerIn(BaseModel):
    name: str
    email: EmailStr

@router.post("", status_code=201)
async def create_customer(data: CustomerIn, request: Request):
    client: CustomerClient = request.app.state.customer_client
    try:
        res = await client.create(data.name, data.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "id": res.customer.id,
        "name": res.customer.name,
        "email": res.customer.email,
        "created_at": res.customer.created_at.ToDatetime().isoformat()
    }

@router.get("/{customer_id}")
async def get_customer(customer_id: str, request: Request):
    client: CustomerClient = request.app.state.customer_client
    try:
        c = await client.get(customer_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "id": c.id, "name": c.name, "email": c.email,
        "created_at": c.created_at.ToDatetime().isoformat()
    }

@router.put("/{customer_id}")
async def update_customer(customer_id: str, data: CustomerIn, request: Request):
    client: CustomerClient = request.app.state.customer_client
    try:
        c = await client.update(customer_id, data.name, data.email)
    except Exception:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "id": c.id, "name": c.name, "email": c.email,
        "created_at": c.created_at.ToDatetime().isoformat()
    }

@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, request: Request):
    client: CustomerClient = request.app.state.customer_client
    try:
        await client.delete(customer_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Not Found")
    return

@router.get("")
async def list_customers(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    client: CustomerClient = request.app.state.customer_client
    res = await client.list(page=page, page_size=page_size)
    return {
        "customers": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "created_at": c.created_at.ToDatetime().isoformat(),
            } for c in res.customers
        ]
    }
