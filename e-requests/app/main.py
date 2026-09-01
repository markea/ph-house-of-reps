import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.seed_data import seed_database_if_empty
from app.routers import auth, services, requests, agent

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Seed with Core 5 catalogs & test accounts if empty
seed_database_if_empty()

app = FastAPI(
    title=settings.APP_NAME,
    description="Digital Service Request Portal for the House of Representatives of the Philippines",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(services.router)
app.include_router(requests.router)
app.include_router(agent.router)

# Health Check for Cloud Run / Kubernetes probes
@app.get("/healthz")
def health_check():
    return {
        "status": "healthy",
        "app_env": settings.APP_ENV,
        "auth_mode": settings.AUTH_MODE,
        "storage_type": settings.STORAGE_TYPE
    }

# Mount static web frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
