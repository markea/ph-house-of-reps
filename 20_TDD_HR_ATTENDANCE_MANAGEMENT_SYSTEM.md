# Technical Design Document (TDD)
## System 08: HR & Attendance Management System (Lingkod-Kawani DTR)
### UGNAYAN Super App - Human Capital & Civil Service Compliance Module

**Document Reference:** HREP-UGNAYAN-TDD-2026-020  
**Target Organization:** House of Representatives of the Philippines (HRep) Secretariat  
**Author:** Technical Consulting & Solutions Architecture Team  
**Date:** September 2026  
**Status:** Approved for Core Engineering  

---

### 1. Architectural Design & Biometric Ingestion Pipeline

Lingkod-Kawani ingests attendance logs from **ZKTEco / Suprema Biometric Turnstiles** via a secure **Cloud Pub/Sub IoT Ingestion Bridge** and geofenced mobile PWA submissions.

```mermaid
flowchart TD
    subgraph Ingestion_Edge [Edge Capture Devices]
        Bio1[Batasan Lobby Fingerprint / Face Scanners]
        Bio2[North/South Gate Optical Turnstiles]
        Mobile_App[Geofenced Mobile PWA Clock-In]
    end

    subgraph IoT_Bridge [IoT Gateway & Pub/Sub]
        Edge_Daemon[Biometric Sync Daemon (TCP/IP to HTTPS)]
        PubSub_Queue[(Pub/Sub: ugnayan-dtr-punches)]
    end

    subgraph DTR_Processing [DTR Micro-Services]
        Ingestion_Worker[DTR Punch De-duplication Worker]
        CSC_Engine[CSC Leave Accrual & Tardy Calculator]
        Form48_Generator[CSC Form 48 PDF Generator]
    end

    subgraph Persistence [Database & Lakehouse]
        CloudSQL[(Cloud SQL PostgreSQL)]
        BigQuery[(BigQuery HR Analytics)]
    end

    Ingestion_Edge --> IoT_Bridge
    IoT_Bridge --> DTR_Processing
    DTR_Processing --> Persistence
```

---

### 2. Database Schema (PostgreSQL)

```sql
-- 1. Employee Leave Ledger Master Table
CREATE TABLE hr_leave_balances (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(36) UNIQUE NOT NULL REFERENCES users(id),
    vacation_leave_balance NUMERIC(6, 3) NOT NULL DEFAULT 0.000,
    sick_leave_balance NUMERIC(6, 3) NOT NULL DEFAULT 0.000,
    special_privilege_leave_balance INT DEFAULT 3,
    forced_leave_balance INT DEFAULT 5,
    solo_parent_leave_balance INT DEFAULT 7,
    magna_carta_leave_balance INT DEFAULT 60,
    last_accrual_date DATE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Daily Time Record (DTR) Raw & Processed Punches
CREATE TABLE hr_attendance_logs (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    log_date DATE NOT NULL,
    time_in TIMESTAMP WITH TIME ZONE,
    time_out TIMESTAMP WITH TIME ZONE,
    tardiness_minutes INT DEFAULT 0,
    undertime_minutes INT DEFAULT 0,
    overtime_hours NUMERIC(4, 2) DEFAULT 0.0,
    clock_source VARCHAR(30) NOT NULL, -- BIOMETRIC_MAIN, BIOMETRIC_NORTH, GEOFENCED_MOBILE
    is_official_business BOOLEAN DEFAULT FALSE,
    ob_reference_id VARCHAR(50),
    CONSTRAINT unq_user_log_date UNIQUE (user_id, log_date)
);

CREATE INDEX idx_hr_dtr_date ON hr_attendance_logs(log_date);
CREATE INDEX idx_hr_dtr_user ON hr_attendance_logs(user_id);

-- 3. CSC Form No. 6 Digital Leave Applications
CREATE TABLE hr_leave_applications (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    application_number VARCHAR(50) UNIQUE NOT NULL, -- LEAVE-2026-XXXXX
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    leave_type VARCHAR(50) NOT NULL, -- VACATION, SICK, MANDATORY_FORCED, MATERNITY, PATERNITY, SOLO_PARENT, MAGNA_CARTA_WOMEN, CTO
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    working_days_applied NUMERIC(4, 2) NOT NULL,
    commutation_requested BOOLEAN DEFAULT FALSE,
    medical_certificate_url TEXT,
    status VARCHAR(30) DEFAULT 'PENDING_SUPERVISOR', -- PENDING_SUPERVISOR, PENDING_HR, APPROVED, REJECTED
    supervisor_id VARCHAR(36) REFERENCES users(id),
    supervisor_digital_stamp VARCHAR(255),
    hr_approver_id VARCHAR(36) REFERENCES users(id),
    hr_digital_stamp VARCHAR(255),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3. REST API Specification

- `POST /api/dtr/punch`: Ingest biometric/mobile clock-in event with geofence check.
- `GET /api/dtr/form48?user_id={id}&month=2026-09`: Generate certified CSC Form No. 48 PDF.
- `POST /api/dtr/leave/apply`: Submit electronic CSC Form No. 6 leave application.
- `GET /api/dtr/leave/balances`: Retrieve real-time statutory leave balances.
