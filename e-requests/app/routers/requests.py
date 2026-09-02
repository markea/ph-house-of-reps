import random
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Request, ServiceCatalog, User, RequestApproval, AuditLog
from app.schemas import RequestCreate, RequestResponse, ApprovalAction, CSATSubmit
from app.routers.auth import get_current_user
from app.services.storage import get_storage_service, StorageService
from app.config import logger

router = APIRouter(prefix="/api/requests", tags=["Service Requests"])

@router.post("/", response_model=RequestResponse)
def submit_request(
    payload: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = db.query(ServiceCatalog).filter(ServiceCatalog.id == payload.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    tracking_num = f"HREP-REQ-2026-{random.randint(1000, 9999)}"
    now = datetime.utcnow()
    deadline = now + timedelta(hours=service.sla_hours)

    req = Request(
        tracking_number=tracking_num,
        requester_id=current_user.id,
        service_id=service.id,
        status="Pending Approval",
        priority=payload.priority or "Normal",
        form_data=payload.form_data,
        submitted_at=now,
        sla_deadline=deadline
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # Automatically find an approver
    approver = db.query(User).filter(User.role == "Approver").first()
    if approver:
        appr = RequestApproval(
            request_id=req.id,
            approver_id=approver.id,
            step_sequence=1,
            status="Pending"
        )
        db.add(appr)

    # Write Audit Log
    audit = AuditLog(
        request_id=req.id,
        actor_email=current_user.email,
        action="REQUEST_SUBMITTED",
        details=f"Submitted request {tracking_num} for service '{service.service_name}'."
    )
    db.add(audit)
    db.commit()

    logger.info(f"Created request {tracking_num} by {current_user.email}")

    return RequestResponse(
        id=req.id,
        tracking_number=req.tracking_number,
        service_name=service.service_name,
        department_code=service.department.code if service.department else "ADMIN",
        requester_name=current_user.full_name,
        requester_email=current_user.email,
        status=req.status,
        priority=req.priority,
        form_data=req.form_data,
        submitted_at=req.submitted_at,
        sla_deadline=req.sla_deadline,
        completed_at=req.completed_at,
        csat_rating=req.csat_rating
    )

@router.post("/{request_id}/attachments")
async def upload_attachment(
    request_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    storage_service: StorageService = Depends(get_storage_service)
):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    file_path, file_url = await storage_service.upload_file(file, subfolder=f"requests/{req.tracking_number}")
    
    # Store in form_data attachments list
    current_data = dict(req.form_data)
    attachments = current_data.get("_attachments", [])
    attachments.append({
        "original_name": file.filename,
        "storage_path": file_path,
        "url": file_url,
        "uploaded_by": current_user.email,
        "uploaded_at": datetime.utcnow().isoformat()
    })
    current_data["_attachments"] = attachments
    req.form_data = current_data
    
    audit = AuditLog(
        request_id=req.id,
        actor_email=current_user.email,
        action="ATTACHMENT_UPLOADED",
        details=f"Uploaded attachment '{file.filename}'."
    )
    db.add(audit)
    db.commit()

    return {
        "status": "success",
        "filename": file.filename,
        "file_url": file_url
    }

@router.get("/", response_model=List[RequestResponse])
def list_requests(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Request).order_by(Request.submitted_at.desc())
    if status:
        query = query.filter(Request.status == status)
    
    results = []
    for r in query.all():
        results.append(
            RequestResponse(
                id=r.id,
                tracking_number=r.tracking_number,
                service_name=r.service.service_name if r.service else "General Service",
                department_code=r.service.department.code if r.service and r.service.department else "ADMIN",
                requester_name=r.requester.full_name if r.requester else "Unknown",
                requester_email=r.requester.email if r.requester else "unknown@hrep.gov.ph",
                status=r.status,
                priority=r.priority,
                form_data=r.form_data,
                submitted_at=r.submitted_at,
                sla_deadline=r.sla_deadline,
                completed_at=r.completed_at,
                csat_rating=r.csat_rating
            )
        )
    return results

@router.get("/{request_id}")
def get_request_detail(request_id: str, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    approvals = [
        {
            "id": a.id,
            "approver_name": a.approver.full_name,
            "status": a.status,
            "remarks": a.remarks,
            "digital_stamp": a.digital_stamp,
            "action_timestamp": a.action_timestamp
        }
        for a in req.approvals
    ]
    
    audits = [
        {
            "actor": log.actor_email,
            "action": log.action,
            "details": log.details,
            "timestamp": log.timestamp
        }
        for log in req.audit_logs
    ]

    return {
        "id": req.id,
        "tracking_number": req.tracking_number,
        "service_name": req.service.service_name,
        "department": req.service.department.name,
        "requester": {
            "name": req.requester.full_name,
            "email": req.requester.email,
            "position": req.requester.position
        },
        "status": req.status,
        "priority": req.priority,
        "form_data": req.form_data,
        "submitted_at": req.submitted_at,
        "sla_deadline": req.sla_deadline,
        "completed_at": req.completed_at,
        "approvals": approvals,
        "audit_logs": audits,
        "csat_rating": req.csat_rating,
        "csat_comment": req.csat_comment
    }

@router.post("/{request_id}/action")
def take_approval_action(
    request_id: str,
    action_data: ApprovalAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    now = datetime.utcnow()
    stamp = f"SHA256-AUTHENTICATED-{current_user.full_name.upper().replace(' ', '-')}-{now.strftime('%Y%m%d%H%M%S')}"

    if action_data.action.lower() == "approved":
        req.status = "Approved"
    elif action_data.action.lower() == "completed":
        req.status = "Completed"
        req.completed_at = now
    else:
        req.status = "Rejected"

    # Update approval step
    appr = db.query(RequestApproval).filter(RequestApproval.request_id == req.id).first()
    if appr:
        appr.status = req.status
        appr.remarks = action_data.remarks
        appr.digital_stamp = stamp
        appr.action_timestamp = now

    # Audit log
    audit = AuditLog(
        request_id=req.id,
        actor_email=current_user.email,
        action=f"STATUS_{req.status.upper()}",
        details=f"{current_user.full_name} executed action: {req.status}. Remarks: {action_data.remarks or 'None'}."
    )
    db.add(audit)
    db.commit()

    return {"status": "success", "new_status": req.status, "digital_stamp": stamp}

@router.post("/{request_id}/csat")
def submit_csat(
    request_id: str,
    payload: CSATSubmit,
    db: Session = Depends(get_db)
):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    req.csat_rating = payload.rating
    req.csat_comment = payload.comment
    db.commit()

    return {"status": "success", "message": "Thank you for your ARTA service quality feedback!"}
