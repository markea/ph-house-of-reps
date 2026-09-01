from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Department, ServiceCatalog
from app.schemas import DepartmentResponse, ServiceCatalogResponse

router = APIRouter(prefix="/api/services", tags=["Service Catalog"])

@router.get("/departments", response_model=List[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.get("/", response_model=List[ServiceCatalogResponse])
def list_services(department_code: str = None, db: Session = Depends(get_db)):
    query = db.query(ServiceCatalog).filter(ServiceCatalog.is_active == True)
    if department_code:
        dept = db.query(Department).filter(Department.code == department_code.upper()).first()
        if dept:
            query = query.filter(ServiceCatalog.department_id == dept.id)
    return query.all()

@router.get("/{service_id}", response_model=ServiceCatalogResponse)
def get_service_details(service_id: str, db: Session = Depends(get_db)):
    service = db.query(ServiceCatalog).filter(ServiceCatalog.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
