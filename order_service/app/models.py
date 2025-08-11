from sqlalchemy import Column, String, Float, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Order(Base):
  __tablename__ = 'orders'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
  product_name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  created_at = Column(DateTime, default=func.now())