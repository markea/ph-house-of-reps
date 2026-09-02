import os
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import settings, logger
from app.database import engine, Base, SessionLocal
from app.seed_data import seed_database_if_empty
from app.routers import auth, services, requests, agent

# Initialize DB tables (for local dev)
if settings.APP_ENV == "local":
    Base.metadata.create_all(bind=engine)
    # Seed initial catalogs and test accounts in local dev mode
    seed_database_if_empty()

app = FastAPI(
    title=settings.APP_NAME,
    description="Digital Service Request Portal for the House of Representatives of the Philippines",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security Response Headers Middleware (OWASP & NPC Privacy Compliance)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    return response

# Include API Routers
app.include_router(auth.router)
app.include_router(services.router)
app.include_router(requests.router)
app.include_router(agent.router)

# Liveness Probe (Cloud Run / K8s)
@app.get("/healthz", tags=["Observability"])
def health_check():
    return {
        "status": "healthy",
        "app_env": settings.APP_ENV,
        "auth_mode": settings.AUTH_MODE,
        "storage_type": settings.STORAGE_TYPE
    }

# Readiness Probe (Checks database availability)
@app.get("/readyz", tags=["Observability"])
def readiness_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return Response(content='{"status": "unhealthy", "database": "disconnected"}', status_code=503, media_type="application/json")
    finally:
        db.close()

# Mount static uploads directory for local mode
if settings.STORAGE_TYPE == "local" and os.path.exists(settings.LOCAL_UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.LOCAL_UPLOAD_DIR), name="uploads")

# Mount static web frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=(settings.APP_ENV == "local"))
