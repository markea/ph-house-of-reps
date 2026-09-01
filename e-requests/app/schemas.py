from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DepartmentResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ServiceCatalogResponse(BaseModel):
    id: str
    department_id: str
    service_name: str
    service_code: str
    description: str
    sla_hours: int
    form_schema: Dict[str, Any]

    class Config:
        from_attributes = True

class RequestCreate(BaseModel):
    service_id: str
    form_data: Dict[str, Any]
    priority: Optional[str] = "Normal"

class ApprovalAction(BaseModel):
    action: str = Field(..., description="'Approved' or 'Rejected'")
    remarks: Optional[str] = None

class CSATSubmit(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class RequestResponse(BaseModel):
    id: str
    tracking_number: str
    service_name: Optional[str] = None
    department_code: Optional[str] = None
    requester_name: Optional[str] = None
    requester_email: Optional[str] = None
    status: str
    priority: str
    form_data: Dict[str, Any]
    submitted_at: datetime
    sla_deadline: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    csat_rating: Optional[int] = None

    class Config:
        from_attributes = True

class AgentTriageRequest(BaseModel):
    user_prompt: str

class AgentTriageResponse(BaseModel):
    suggested_service_code: str
    suggested_service_name: str
    extracted_fields: Dict[str, Any]
    confidence_score: float
    reasoning: str
    next_question: Optional[str] = None
