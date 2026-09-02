from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from app.config import settings, logger

# Configure Engine parameters depending on driver
engine_kwargs = {
    "echo": (settings.APP_ENV == "local" and settings.LOG_LEVEL.upper() == "DEBUG")
}

if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL / Cloud SQL Production Pool Settings
    engine_kwargs.update({
        "poolclass": QueuePool,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True  # Prevents stale connection errors in Cloud Run
    })

logger.info(f"Initializing database engine with driver: {settings.DATABASE_URL.split('://')[0]} (ENV: {settings.APP_ENV})")
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
