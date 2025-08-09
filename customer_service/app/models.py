from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Customer(Base):
  __tablename__ = 'customers'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid64)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  created_at = Column(DateTime, default=func.now())

