import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.seed_data import seed_database_if_empty

# In-memory SQLite for fast, isolated testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    # Seed data
    db = TestingSessionLocal()
    try:
        from app.models import Department, ServiceCatalog, User
        dept = Department(name="Administrative Department", code="ADMIN", description="Admin services")
        db.add(dept)
        db.commit()

        user = User(email="staff.maria@hrep.gov.ph", full_name="Maria Santos", role="Requester", department_id=dept.id)
        approver = User(email="director.reyes@hrep.gov.ph", full_name="Atty. Roberto Reyes", role="Approver", department_id=dept.id)
        db.add(user)
        db.add(approver)
        db.commit()

        service = ServiceCatalog(
            department_id=dept.id,
            service_name="Motor Pool Vehicle & Driver Dispatch",
            service_code="MOTOR_POOL",
            description="Vehicle dispatch",
            sla_hours=24,
            form_schema={"title": "Test Form", "fields": [{"name": "destination", "type": "text", "required": True}]}
        )
        db.add(service)
        db.commit()
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

