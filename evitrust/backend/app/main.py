from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, cases, evidence, analysis, decisions, reports, audit, admin, auth, forensic
from app.db.mongo import init_mongo
from app.db.indexes import ensure_indexes
from app.config import settings

app = FastAPI(title="EviTrust API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.api_cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    init_mongo()
    ensure_indexes()

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(evidence.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(decisions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(forensic.router, prefix="/api")
