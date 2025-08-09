import grpc
from concurrent import futures
from .proto import customer_pb2_grpc
from .proto import customer_pb2
from sqlalchemy.orm import Session
from models import Customer
from db import get_db
import uuid
from datetime import datetime

class CustomerServiceServicer(customer_pb2_grpc.CustomerServiceServicer):
    def CreateCustomer(self, request, context):
        db = next(get_db())
        customer = Customer(name=request.name, email=request.email)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer_pb2.CustomerResponse(
            id=str(customer.id),
            name=customer.name,
            email=customer.email,
            created_at=customer.created_at.isoformat()
        )

    def GetCustomer(self, request, context):
        db = next(get_db())
        customer = db.query(Customer).filter(Customer.id == uuid.UUID(request.id)).first()
        if not customer:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Customer not found")
            return customer_pb2.CustomerResponse()
        return customer_pb2.CustomerResponse(
            id=str(customer.id),
            name=customer.name,
            email=customer.email,
            created_at=customer.created_at.isoformat()
        )

    def UpdateCustomer(self, request, context):
        db = next(get_db())
        customer = db.query(Customer).filter(Customer.id == uuid.UUID(request.id)).first()
        if not customer:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Customer not found")
            return customer_pb2.CustomerResponse()
        customer.name = request.name
        customer.email = request.email
        db.commit()
        return customer_pb2.CustomerResponse(
            id=str(customer.id),
            name=customer.name,
            email=customer.email,
            created_at=customer.created_at.isoformat()
        )

    def DeleteCustomer(self, request, context):
        db = next(get_db())
        customer = db.query(Customer).filter(Customer.id == uuid.UUID(request.id)).first()
        if not customer:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Customer not found")
            return customer_pb2.Empty()
        db.delete(customer)
        db.commit()
        return customer_pb2.Empty()

    def ListCustomers(self, request, context):
        db = next(get_db())
        customers = db.query(Customer).all()
        return customer_pb2.CustomerListResponse(
            customers=[
                customer_pb2.CustomerResponse(
                    id=str(c.id),
                    name=c.name,
                    email=c.email,
                    created_at=c.created_at.isoformat()
                ) for c in customers
            ]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Customer Service started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()