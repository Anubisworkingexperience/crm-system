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
        "id": res.id,
        "name": res.name,
        "email": res.email,
        "created_at": res.created_at
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
        "created_at": c.created_at
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
):
    client: CustomerClient = request.app.state.customer_client
    res = await client.list()
    return {
        "customers": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "created_at": c.created_at
            } for c in res.customers
        ]
    }
