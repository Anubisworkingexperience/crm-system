import grpc
from grpc import aio
from app.config import settings
from app.proto import order_pb2, order_pb2_grpc

class OrderClient:
    def __init__(self, addr: str):
        self.addr = addr
        self.channel: aio.Channel | None = None
        self.stub: order_pb2_grpc.OrderServiceStub | None = None

    async def start(self):
        self.channel = aio.insecure_channel(self.addr)
        self.stub = order_pb2_grpc.OrderServiceStub(self.channel)

    async def close(self):
        if self.channel:
            await self.channel.close()

    async def create_order(self, customer_id: str, product_name: str, price: float):
        req = order_pb2.CreateOrderRequest(customer_id=customer_id, product_name=product_name, price=price)
        return await self.stub.CreateOrder(req)

    async def get_order(self, id: str):
        return await self.stub.GetOrder(order_pb2.GetOrderRequest(id=id))

    async def get_customer_orders(self, customer_id: str, page: int = 1, page_size: int = 20):
        req = order_pb2.GetCustomerOrdersRequest(customer_id=customer_id, page=page, page_size=page_size)
        return await self.stub.GetCustomerOrders(req)
