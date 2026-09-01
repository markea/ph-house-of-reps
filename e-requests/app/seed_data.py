from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Department, ServiceCatalog, User, Request, RequestApproval, AuditLog

def seed_database_if_empty():
    db = SessionLocal()
    try:
        if db.query(Department).first():
            return  # Already seeded

        print("Seeding initial HRep e-Request database...")

        # 1. Departments
        depts = {
            "ADMIN": Department(name="Administrative Department", code="ADMIN", description="Motor Pool, logistics, supplies, and general administrative services."),
            "EPFD": Department(name="Engineering & Physical Facilities Department", code="EPFD", description="Building infrastructure, electrical, plumbing, and air-conditioning maintenance."),
            "ICTS": Department(name="Information & Communications Technology Service", code="ICTS", description="Workstations, network, plenary sound/video systems, and IT software support."),
            "OSAA": Department(name="Office of the Sergeant-at-Arms", code="OSAA", description="Perimeter security, VIP protection, access passes, and official ID cards."),
            "LAD": Department(name="Legal Affairs Department", code="LAD", description="Legal review of contracts, MOAs, procurement terms, and legislative counsel.")
        }
        for d in depts.values():
            db.add(d)
        db.commit()

        # 2. Users
        users = {
            "requester": User(
                email="staff.maria@hrep.gov.ph",
                full_name="Maria Santos (Legislative Staff Officer)",
                role="Requester",
                department_id=depts["ADMIN"].id,
                position="Legislative Staff Officer II - Office of Rep. Ramos"
            ),
            "approver": User(
                email="director.reyes@hrep.gov.ph",
                full_name="Atty. Roberto Reyes (Service Director)",
                role="Approver",
                department_id=depts["ADMIN"].id,
                position="Director - Administrative Services"
            ),
            "dispatcher_motorpool": User(
                email="dispatcher.motor@hrep.gov.ph",
                full_name="Danilo Cruz (Motor Pool Dispatcher)",
                role="Dispatcher",
                department_id=depts["ADMIN"].id,
                position="Supervising Transport Officer"
            ),
            "tech_icts": User(
                email="support.icts@hrep.gov.ph",
                full_name="Engr. Allan Garcia (ICT Support Lead)",
                role="Dispatcher",
                department_id=depts["ICTS"].id,
                position="Information Technology Officer III"
            )
        }
        for u in users.values():
            db.add(u)
        db.commit()

        # 3. Core 5 Service Catalogs with Dynamic JSON Schemas
        services = [
            ServiceCatalog(
                department_id=depts["ADMIN"].id,
                service_name="Motor Pool Vehicle & Driver Dispatch",
                service_code="MOTOR_POOL",
                description="Request official government vehicle dispatch and driver for legislative, committee, or official district business.",
                sla_hours=24,
                form_schema={
                    "title": "Official Vehicle Dispatch Request",
                    "fields": [
                        {"name": "trip_purpose", "label": "Purpose of Trip", "type": "select", "options": ["Committee Hearing / Ocular", "Official VIP / Diplomatic Escort", "District Consultation", "Inter-Agency Coordination"], "required": True},
                        {"name": "destination", "label": "Destination Address", "type": "text", "placeholder": "e.g., Senate of the Philippines, Pasay City", "required": True},
                        {"name": "departure_datetime", "label": "Date & Time of Departure", "type": "datetime-local", "required": True},
                        {"name": "return_datetime", "label": "Estimated Return Date & Time", "type": "datetime-local", "required": True},
                        {"name": "passenger_count", "label": "Number of Passengers", "type": "number", "min": 1, "max": 15, "required": True},
                        {"name": "lead_passenger", "label": "Lead Passenger / Official Contact", "type": "text", "required": True},
                        {"name": "special_requirements", "label": "Special Instructions (e.g. VIP Van, Luggage Space)", "type": "textarea", "required": False}
                    ]
                }
            ),
            ServiceCatalog(
                department_id=depts["EPFD"].id,
                service_name="Building & Air-Conditioning Maintenance",
                service_code="AC_REPAIR",
                description="Report facility defects, air-con water leaks or temperature issues, lighting fixtures, and plumbing repairs.",
                sla_hours=48,
                form_schema={
                    "title": "Facility Maintenance Job Order",
                    "fields": [
                        {"name": "building_location", "label": "Building / Wing", "type": "select", "options": ["Main Building", "South Wing Annex", "North Wing Annex", "Mitra Building", "Plenary Hall"], "required": True},
                        {"name": "room_number", "label": "Room / Office Number", "type": "text", "placeholder": "e.g., Room 314, Committee on Appropriations", "required": True},
                        {"name": "category", "label": "Issue Category", "type": "select", "options": ["Air-Conditioning (Leaking/Not Cold)", "Electrical / Power Outlets", "Lighting Fixtures", "Plumbing / Restroom", "Carpentry / Locksmith"], "required": True},
                        {"name": "issue_description", "label": "Detailed Problem Description", "type": "textarea", "placeholder": "Describe what is malfunctioning...", "required": True},
                        {"name": "urgency", "label": "Operational Urgency", "type": "select", "options": ["Routine", "Urgent (Disrupting Office Work)", "Emergency (Active Flooding/Electrical Spark)"], "required": True}
                    ]
                }
            ),
            ServiceCatalog(
                department_id=depts["ICTS"].id,
                service_name="ICT Equipment Loan & Technical Support",
                service_code="ICT_SUPPORT",
                description="Request laptops, projectors, PA sound systems for hearings, Wi-Fi troubleshooting, and printer repairs.",
                sla_hours=24,
                form_schema={
                    "title": "ICT Service & Equipment Request",
                    "fields": [
                        {"name": "request_type", "label": "Request Type", "type": "select", "options": ["Equipment Loan (Hearing / Presentation)", "Workstation / Laptop Troubleshooting", "Network / Wi-Fi Access Issue", "Software / Email Configuration"], "required": True},
                        {"name": "hearing_or_event", "label": "Event / Hearing Title (if applicable)", "type": "text", "placeholder": "e.g., Public Hearing on House Bill 402", "required": False},
                        {"name": "equipment_needed", "label": "Equipment Needed", "type": "select", "options": ["None (Service Only)", "Laptop + Wireless Clicker", "High-Lumen Projector & Screen", "Portable PA Sound System", "Video Conference Kit (Owl / Mic)"], "required": True},
                        {"name": "venue", "label": "Venue / Room", "type": "text", "required": True},
                        {"name": "needed_datetime", "label": "Date & Time Required", "type": "datetime-local", "required": True}
                    ]
                }
            ),
            ServiceCatalog(
                department_id=depts["OSAA"].id,
                service_name="HRep Official ID Issuance & Replacement",
                service_code="ID_REPLACEMENT",
                description="Apply for new employee/congressional staff ID badges, temporary visitor IDs, or replacement of lost/damaged RFID cards.",
                sla_hours=72,
                form_schema={
                    "title": "HRep Identification Card Application",
                    "fields": [
                        {"name": "application_type", "label": "Application Type", "type": "select", "options": ["New Plantilla Employee", "Coterminous Congressional Staff", "Replacement for Lost ID (Affidavit of Loss Required)", "Replacement for Damaged / Worn ID"], "required": True},
                        {"name": "full_name_on_id", "label": "Full Name to Appear on Card", "type": "text", "required": True},
                        {"name": "item_or_district", "label": "Plantilla Item No. / Congressional District", "type": "text", "required": True},
                        {"name": "blood_type", "label": "Blood Type", "type": "select", "options": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"], "required": True},
                        {"name": "emergency_contact", "label": "Emergency Contact Person & Phone", "type": "text", "required": True}
                    ]
                }
            ),
            ServiceCatalog(
                department_id=depts["LAD"].id,
                service_name="Legal Contract & Agreement Review",
                service_code="CONTRACT_REVIEW",
                description="Submit procurement contracts, Memoranda of Agreement (MOA), non-disclosure agreements, or legal queries for LAD review.",
                sla_hours=120,
                form_schema={
                    "title": "Legal Affairs Document Review Request",
                    "fields": [
                        {"name": "document_type", "label": "Document Type", "type": "select", "options": ["Procurement Contract / Supply Agreement", "Memorandum of Agreement (MOA) / MOU", "Software License / SLA Agreement", "Legal Opinion Request"], "required": True},
                        {"name": "contract_title", "label": "Title of Contract / Project Name", "type": "text", "placeholder": "e.g., Supply & Delivery of ICT Servers 2026", "required": True},
                        {"name": "contract_party", "label": "Second Party / Counterparty Name", "type": "text", "placeholder": "e.g., ABC Solutions Inc.", "required": True},
                        {"name": "contract_amount", "label": "Total Contract Value (PHP)", "type": "number", "placeholder": "0.00", "required": False},
                        {"name": "background_summary", "label": "Executive Summary & Key Concerns", "type": "textarea", "required": True}
                    ]
                }
            )
        ]
        for s in services:
            db.add(s)
        db.commit()

        # 4. Sample Seed Request Tickets
        req1 = Request(
            tracking_number="HREP-REQ-2026-0001",
            requester_id=users["requester"].id,
            service_id=services[0].id,  # Motorpool
            status="Approved",
            priority="Urgent",
            form_data={
                "trip_purpose": "Committee Hearing / Ocular",
                "destination": "Senate of the Philippines, GSIS Bldg, Pasay City",
                "departure_datetime": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT09:00"),
                "return_datetime": (datetime.utcnow() + timedelta(days=1, hours=5)).strftime("%Y-%m-%dT14:00"),
                "passenger_count": 4,
                "lead_passenger": "Atty. Clara Dizon (Committee Secretary)",
                "special_requirements": "Luggage space for 3 boxes of hearing records."
            },
            submitted_at=datetime.utcnow() - timedelta(hours=5),
            sla_deadline=datetime.utcnow() + timedelta(hours=19)
        )
        db.add(req1)
        db.commit()

        appr1 = RequestApproval(
            request_id=req1.id,
            approver_id=users["approver"].id,
            step_sequence=1,
            status="Approved",
            remarks="Approved for official committee mission.",
            digital_stamp="SHA256-STAMP-DIR-ROBERTO-REYES-20260901-AUTHENTICATED",
            action_timestamp=datetime.utcnow() - timedelta(hours=2)
        )
        db.add(appr1)

        audit1 = AuditLog(
            request_id=req1.id,
            actor_email=users["approver"].email,
            action="APPROVAL_COMPLETED",
            details="Service Director approved ticket HREP-REQ-2026-0001."
        )
        db.add(audit1)

        # Seed Request 2: AC Repair (In Progress)
        req2 = Request(
            tracking_number="HREP-REQ-2026-0002",
            requester_id=users["requester"].id,
            service_id=services[1].id,  # EPFD AC Repair
            status="In Progress",
            priority="Normal",
            form_data={
                "building_location": "South Wing Annex",
                "room_number": "Room 214",
                "category": "Air-Conditioning (Leaking/Not Cold)",
                "issue_description": "Ceiling cassette air-conditioner is blowing warm air and dripping water onto the filing cabinets.",
                "urgency": "Urgent (Disrupting Office Work)"
            },
            submitted_at=datetime.utcnow() - timedelta(hours=12),
            sla_deadline=datetime.utcnow() + timedelta(hours=36)
        )
        db.add(req2)
        db.commit()

        print("Seeding completed successfully with Core 5 Services and sample transactions!")
    finally:
        db.close()
