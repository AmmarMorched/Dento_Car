from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.report import Report
from app.models.scan_session import ScanSession
from app.services.pdf_generator import generate_pdf
from app.core.security import get_current_user
import uuid

router = APIRouter()

@router.post("/generate/{session_id}")
async def generate_report(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    session = db.query(ScanSession).filter_by(id=session_id, user_id=current_user.id).first()
    if not session:
        raise HTTPException(status_code=404)

    pdf_url = await generate_pdf(session)
    report = Report(session_id=session_id, pdf_url=pdf_url)
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "report_id": str(report.id),
        "share_link": f"/reports/view/{report.share_token}",
        "pdf_url": report.pdf_url,
    }


@router.get("/view/{share_token}")
def view_report(share_token: str, db: Session = Depends(get_db)):
    """Public endpoint — no auth required. Used for sharing."""
    report = db.query(Report).filter_by(share_token=share_token, is_expired=False).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or expired")
    report.viewed_count += 1
    db.commit()
    return {"pdf_url": report.pdf_url, "generated_at": report.generated_at}