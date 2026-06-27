from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid, enum

class DefectType(str, enum.Enum):
    dent    = "dent"
    scratch = "scratch"
    crack   = "crack"
    other   = "other"

class Severity(str, enum.Enum):
    minor    = "minor"
    moderate = "moderate"
    severe   = "severe"

class Detection(Base):
    __tablename__ = "detections"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id     = Column(UUID(as_uuid=True), ForeignKey("scan_images.id"), nullable=False)
    defect_type  = Column(Enum(DefectType), nullable=False)
    severity     = Column(Enum(Severity), nullable=False)
    confidence   = Column(Float, nullable=False)
    mask_polygon = Column(JSONB, nullable=True)   # pixel coords from YOLO seg
    bbox_x       = Column(Float)
    bbox_y       = Column(Float)
    bbox_w       = Column(Float)
    bbox_h       = Column(Float)
    mask_area_px = Column(Integer, nullable=True)  # used for severity scoring

    image = relationship("ScanImage", back_populates="detections")