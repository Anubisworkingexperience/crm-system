import grpc
from concurrent import futures
from proto import order_pb2
from proto import order_pb2_grpc
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Order
from db import get_db
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderServiceServicer(order_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        if request.price <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Price must be positive")
            return order_pb2.OrderResponse()
        
        db = next(get_db())
        order = Order(
            customer_id=uuid.UUID(request.customer_id),
            product_name=request.product_name,
            price=request.price
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        logger.info(f"Created order {order.id} for customer {order.customer_id}")
        
        return order_pb2.OrderResponse(
            id=str(order.id),
            customer_id=str(order.customer_id),
            product_name=order.product_name,
            price=order.price,
            created_at=order.created_at.isoformat()
        )

    def GetCustomerOrder(self, request, context):
        db = next(get_db())
        query = db.query(Order).filter(Order.customer_id == uuid.UUID(request.customer_id))
        
        if not query.first():
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No orders found for this customer")
            return order_pb2.CustomerOrder()
        
        orders = query.order_by(desc(Order.created_at)).all()
        
        return order_pb2.CustomerOrder(
            orders=[
                order_pb2.OrderResponse(
                    id=str(o.id),
                    customer_id=str(o.customer_id),
                    product_name=o.product_name,
                    price=o.price,
                    created_at=o.created_at.isoformat()
                ) for o in orders
            ]
        )
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logger.info("Order Service started on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()