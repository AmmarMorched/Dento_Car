from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, scans, reports, health
from app.core.config import settings

from app.models import user, scan_session, scan_image, detection, report

app = FastAPI(title="DentoCAr API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router,   prefix="/auth",   tags=["auth"])
app.include_router(scans.router,  prefix="/scans",  tags=["scans"])
app.include_router(reports.router,prefix="/reports",tags=["reports"])