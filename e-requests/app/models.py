import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Department(Base):
    __tablename__ = "departments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)  # ADMIN, EPFD, ICTS, OSAA, LAD
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="department")
    services = relationship("ServiceCatalog", back_populates="department")

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(120), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default="Requester")  # Requester, Approver, Dispatcher, Admin
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    position = Column(String(100), nullable=True)

    department = relationship("Department", back_populates="users")
    submitted_requests = relationship("Request", back_populates="requester", foreign_keys="Request.requester_id")
    approvals = relationship("RequestApproval", back_populates="approver")

class ServiceCatalog(Base):
    __tablename__ = "service_catalogs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False, index=True)
    service_name = Column(String(150), nullable=False)
    service_code = Column(String(50), unique=True, nullable=False, index=True)  # MOTOR_POOL, AC_REPAIR, ICT_SUPPORT, ID_REPLACEMENT, CONTRACT_REVIEW
    description = Column(Text, nullable=False)
    sla_hours = Column(Integer, default=72)  # In working hours
    is_active = Column(Boolean, default=True)
    form_schema = Column(JSON, nullable=False)  # Dynamic JSON Schema for Form Builder

    department = relationship("Department", back_populates="services")
    requests = relationship("Request", back_populates="service")

class Request(Base):
    __tablename__ = "requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tracking_number = Column(String(50), unique=True, nullable=False, index=True)
    requester_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    service_id = Column(String(36), ForeignKey("service_catalogs.id"), nullable=False, index=True)
    status = Column(String(50), default="Pending Approval", index=True)  # Draft, Pending Approval, Approved, In Progress, Completed, Rejected
    form_data = Column(JSON, nullable=False)  # User submitted field answers
    priority = Column(String(20), default="Normal")  # Routine, Urgent, VIP
    submitted_at = Column(DateTime, default=utc_now, index=True)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    sla_deadline = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    csat_rating = Column(Integer, nullable=True)
    csat_comment = Column(Text, nullable=True)

    requester = relationship("User", back_populates="submitted_requests", foreign_keys=[requester_id])
    service = relationship("ServiceCatalog", back_populates="requests")
    approvals = relationship("RequestApproval", back_populates="request", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="request", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_requests_requester_status", "requester_id", "status"),
        Index("idx_requests_service_status", "service_id", "status"),
    )

class RequestApproval(Base):
    __tablename__ = "request_approvals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("requests.id"), nullable=False, index=True)
    approver_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    step_sequence = Column(Integer, default=1)
    status = Column(String(50), default="Pending", index=True)  # Pending, Approved, Rejected
    remarks = Column(Text, nullable=True)
    digital_stamp = Column(String(255), nullable=True)  # Cryptographic stamp
    action_timestamp = Column(DateTime, nullable=True)

    request = relationship("Request", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")

    __table_args__ = (
        Index("idx_approvals_approver_status", "approver_id", "status"),
    )

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("requests.id"), nullable=True, index=True)
    actor_email = Column(String(120), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)

    request = relationship("Request", back_populates="audit_logs")

