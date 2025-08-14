import grpc
from grpc import aio
from app.config import settings
from app.proto import customer_pb2, customer_pb2_grpc
from google.protobuf import empty_pb2

class CustomerClient:
    def __init__(self, addr: str):
        self.addr = addr
        self.channel: aio.Channel | None = None
        self.stub: customer_pb2_grpc.CustomerServiceStub | None = None

    async def start(self):
        self.channel = aio.insecure_channel(self.addr)
        self.stub = customer_pb2_grpc.CustomerServiceStub(self.channel)

    async def close(self):
        if self.channel:
            await self.channel.close()

    async def create(self, name: str, email: str):
        req = customer_pb2.CreateCustomerRequest(name=name, email=email)
        return await self.stub.CreateCustomer(req)

    async def get(self, id: str):
        return await self.stub.GetCustomer(customer_pb2.GetCustomerRequest(id=id))

    async def update(self, id: str, name: str, email: str):
        return await self.stub.UpdateCustomer(customer_pb2.UpdateCustomerRequest(id=id, name=name, email=email))

    async def delete(self, id: str):
        return await self.stub.DeleteCustomer(customer_pb2.DeleteCustomerRequest(id=id))

    async def list(self, page: int = 1, page_size: int = 20):
        return await self.stub.ListCustomers(customer_pb2.ListCustomersRequest(page=page, page_size=page_size))
