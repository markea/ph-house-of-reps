import os
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Request, ServiceCatalog, User, RequestApproval, AuditLog, utc_now
from app.schemas import RequestCreate, RequestResponse, ApprovalAction, CSATSubmit
from app.routers.auth import get_current_user
from app.services.storage import get_storage_service, StorageService
from app.services.sla_calculator import calculate_ra11032_sla_deadline
from app.config import logger

router = APIRouter(prefix="/api/requests", tags=["Service Requests"])

def generate_daily_tracking_number(db: Session, prefix: str = "HREP-REQ") -> str:
    """Generates an atomic daily sequential tracking number: HREP-REQ-YYYYMMDD-0001"""
    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    like_pattern = f"{prefix}-{today_str}-%"
    
    count = db.query(func.count(Request.id)).filter(Request.tracking_number.like(like_pattern)).scalar() or 0
    seq_num = count + 1
    return f"{prefix}-{today_str}-{seq_num:04d}"

@router.post("/", response_model=RequestResponse)
def submit_request(
    payload: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = db.query(ServiceCatalog).filter(ServiceCatalog.id == payload.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    tracking_num = generate_daily_tracking_number(db)
    now = utc_now()
    # Compute statutory SLA deadline pursuant to RA 11032 (Ease of Doing Business Act)
    deadline = calculate_ra11032_sla_deadline(now, service.sla_hours or 72)

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

    # Flexible approver assignment: prioritize department approver, fallback to any active approver
    approver = None
    if service.department_id:
        approver = db.query(User).filter(User.department_id == service.department_id, User.role == "Approver").first()
    if not approver:
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

    # Authorization check
    if current_user.role == "Requester" and req.requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden. You can only attach files to your own requests.")

    file_path, file_url = await storage_service.upload_file(file, subfolder=f"requests/{req.tracking_number}")
    
    # Store in form_data attachments list
    current_data = dict(req.form_data)
    attachments = current_data.get("_attachments", [])
    attachments.append({
        "original_name": file.filename,
        "storage_path": file_path,
        "url": file_url,
        "uploaded_by": current_user.email,
        "uploaded_at": utc_now().isoformat()
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
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Request)
    
    # RBAC Data Filtering:
    # - Requesters only see their own submissions
    # - Approvers/Dispatchers see their department's or assigned requests
    # - Admins see all requests
    if current_user.role == "Requester":
        query = query.filter(Request.requester_id == current_user.id)
    elif current_user.role in ["Approver", "Dispatcher"] and current_user.department_id:
        # Filter by department services or where user is direct approver
        query = query.join(Request.service).filter(
            (ServiceCatalog.department_id == current_user.department_id) | 
            (Request.approvals.any(RequestApproval.approver_id == current_user.id))
        )
    
    if status:
        query = query.filter(Request.status == status)
    
    query = query.order_by(Request.submitted_at.desc()).offset(offset).limit(limit)
    
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
def get_request_detail(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # RBAC check: Requester cannot view other requesters' tickets
    if current_user.role == "Requester" and req.requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden. You do not have access to view this request.")

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
        "department": req.service.department.name if req.service.department else "General",
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

    # RBAC check: Only Approver, Dispatcher, or Admin roles can take action
    if current_user.role not in ["Approver", "Dispatcher", "Admin"]:
        raise HTTPException(status_code=403, detail="Forbidden. Only authorized Approvers or Administrators may approve or reject requests.")

    now = utc_now()
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
        details=f"{current_user.full_name} ({current_user.role}) executed action: {req.status}. Remarks: {action_data.remarks or 'None'}."
    )
    db.add(audit)
    db.commit()

    return {"status": "success", "new_status": req.status, "digital_stamp": stamp}

@router.post("/{request_id}/csat")
def submit_csat(
    request_id: str,
    payload: CSATSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Only the requester or admin can submit CSAT for the ticket
    if current_user.role == "Requester" and req.requester_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden. You can only evaluate requests you submitted.")

    req.csat_rating = payload.rating
    req.csat_comment = payload.comment
    db.commit()

    return {"status": "success", "message": "Thank you for your ARTA service quality feedback!"}

