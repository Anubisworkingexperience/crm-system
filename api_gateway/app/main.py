import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.middleware.jwt_middleware import JWTMiddleware
from app.routers import customers, orders, health
from app.auth import routers as auth_routers
from app.grpc.customer_client import CustomerClient
from app.grpc.order_client import OrderClient
from app.auth.db import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.customer_client = CustomerClient(settings.CUSTOMER_SERVICE_ADDR)
    app.state.order_client = OrderClient(settings.ORDER_SERVICE_ADDR)
    await app.state.customer_client.start()
    await app.state.order_client.start()
    
    yield

    await app.state.customer_client.close()
    await app.state.order_client.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="REST API Gateway for CRM",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # routes
    app.include_router(auth_routers.router)    
    app.include_router(customers.router)      
    app.include_router(orders.router)          

    # middleware
    app.add_middleware(JWTMiddleware)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
