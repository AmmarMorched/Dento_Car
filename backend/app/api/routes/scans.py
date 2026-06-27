from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.scan_session import ScanSession, ScanStatus
from app.models.scan_image import ScanImage, Panel
from app.services.r2_storage import upload_image
from app.workers.tasks import run_inference
from app.core.security import get_current_user
import uuid

router = APIRouter()

@router.post("/session")
def create_session(
    context: str = "personal",
    vehicle_plate: str = None,
    lat: float = None,
    lng: float = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = ScanSession(
        user_id=current_user.id,
        context=context,
        vehicle_plate=vehicle_plate,
        location_lat=lat,
        location_lng=lng,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": str(session.id)}


@router.post("/session/{session_id}/upload")
async def upload_panel(
    session_id: uuid.UUID,
    panel: Panel,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = db.query(ScanSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # upload original to R2
    image_bytes = await file.read()
    original_url = await upload_image(image_bytes, folder="originals")

    # create DB record — captured_at is server-side (model default)
    scan_image = ScanImage(
        session_id=session_id,
        panel=panel,
        original_url=original_url,
    )
    db.add(scan_image)
    db.commit()
    db.refresh(scan_image)

    # dispatch inference job
    task = run_inference.delay(str(scan_image.id))
    scan_image.celery_task_id = task.id
    db.commit()

    return {
        "image_id": str(scan_image.id),
        "task_id": task.id,
        "status": "processing",
    }


@router.get("/session/{session_id}/status")
def session_status(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = db.query(ScanSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "status": session.status,
        "panels": [
            {"panel": img.panel, "status": "done" if img.annotated_url else "processing"}
            for img in session.images
        ],
    }