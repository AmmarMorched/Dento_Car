from app.core.celery_app import celery_app
from app.db.database import SessionLocal
from app.models.scan_image import ScanImage
from app.models.scan_session import ScanSession, ScanStatus
from app.services.r2_storage import upload_image
import httpx, os

INFERENCE_URL = os.getenv("INFERENCE_SERVICE_URL")

@celery_app.task(bind=True, max_retries=3)
def run_inference(self, image_id: str):
    db = SessionLocal()
    try:
        image = db.query(ScanImage).filter_by(id=image_id).first()
        if not image:
            return

        # call inference service (Vast.ai)
        response = httpx.post(
            f"{INFERENCE_URL}/detect",
            json={"image_url": image.original_url, "image_id": image_id},
            timeout=120,
        )
        result = response.json()

        # save annotated image back to R2
        if result.get("annotated_image_b64"):
            import base64
            img_bytes = base64.b64decode(result["annotated_image_b64"])
            annotated_url = upload_image(img_bytes, folder="annotated")  # sync version
            image.annotated_url = annotated_url

        # save detections
        from app.models.detection import Detection
        for det in result.get("detections", []):
            detection = Detection(
                image_id=image_id,
                defect_type=det["type"],
                severity=det["severity"],
                confidence=det["confidence"],
                mask_polygon=det.get("mask_polygon"),
                bbox_x=det["bbox"][0], bbox_y=det["bbox"][1],
                bbox_w=det["bbox"][2], bbox_h=det["bbox"][3],
                mask_area_px=det.get("mask_area_px"),
            )
            db.add(detection)

        db.commit()
        _check_session_complete(db, image.session_id)

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=10)
    finally:
        db.close()


def _check_session_complete(db, session_id):
    session = db.query(ScanSession).filter_by(id=session_id).first()
    all_done = all(img.annotated_url for img in session.images if not img.is_rejected)
    if all_done:
        session.status = ScanStatus.complete
        db.commit()
        # TODO: send push notification here