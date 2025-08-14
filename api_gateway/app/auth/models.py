import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.auth.db import Base
import uuid

def uuid_col():
    try:
        return sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    except Exception:
        return sa.Column(sa.String, primary_key=True, default=lambda: str(uuid.uuid4()))

class User(Base):
    __tablename__ = "users"
    id = uuid_col()
    email = sa.Column(sa.String(255), unique=True, nullable=False, index=True)
    password_hash = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
