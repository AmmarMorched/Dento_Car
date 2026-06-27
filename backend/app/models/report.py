from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Report(Base):
    __tablename__ = "reports"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id   = Column(UUID(as_uuid=True), ForeignKey("scan_sessions.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    pdf_url      = Column(String, nullable=True)
    share_token  = Column(String, unique=True, default=lambda: uuid.uuid4().hex)
    is_expired   = Column(Boolean, default=False)
    expires_at   = Column(DateTime(timezone=True), nullable=True)  # null = permanent
    viewed_count = Column(Integer, default=0)

    session = relationship("ScanSession", back_populates="reports")