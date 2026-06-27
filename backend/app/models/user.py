from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid, enum


class UserPlan(str, enum.Enum):
    free    = "free"
    premium = "premium"


class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email           = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name       = Column(String, nullable=True)
    phone           = Column(String, nullable=True)
    plan            = Column(Enum(UserPlan), default=UserPlan.free, nullable=False)
    is_active       = Column(Boolean, default=True, nullable=False)
    is_verified     = Column(Boolean, default=False, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    sessions = relationship("ScanSession", back_populates="user", cascade="all, delete-orphan")