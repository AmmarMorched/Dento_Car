from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid, enum

class ScanContext(str, enum.Enum):
    rental    = "rental"
    purchase  = "purchase"
    personal  = "personal"
    insurance = "insurance"

class ScanStatus(str, enum.Enum):
    in_progress = "in_progress"
    processing  = "processing"
    complete    = "complete"
    failed      = "failed"

class ScanSession(Base):
    __tablename__ = "scan_sessions"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    location_lat   = Column(Float, nullable=True)
    location_lng   = Column(Float, nullable=True)
    vehicle_plate  = Column(String, nullable=True)
    context        = Column(Enum(ScanContext), default=ScanContext.personal)
    status         = Column(Enum(ScanStatus), default=ScanStatus.in_progress)

    user    = relationship("User", back_populates="sessions")
    images  = relationship("ScanImage",  back_populates="session")
    reports = relationship("Report",     back_populates="session")