# Technical Design Document (TDD)
## System 03: Records Management System (RMS / HRep Archives & Retention)
### UGNAYAN Super App - Institutional Archival Module

**Document Reference:** HREP-UGNAYAN-TDD-2026-014  
**Target Organization:** House of Representatives of the Philippines (HRep) Secretariat  
**Author:** Technical Consulting & Solutions Architecture Team  
**Date:** September 2026  
**Status:** Approved for Core Engineering  

---

### 1. Architectural Design & Storage Tiering

The RMS architecture establishes a multi-tiered archival storage strategy designed for 100+ years of institutional preservation:

1. **Hot Storage (Cloud Storage Standard):** Active Congress records accessible for instantaneous search and retrieval.
2. **Cold / Archive Storage (Cloud Storage Archive Tier):** Historical Congress records (1st to 18th Congress) stored at fraction of cost with 99.999999999% (11 9's) durability.
3. **Immutability & Legal Hold (Bucket Lock / Object Retention):** WORM (Write Once, Read Many) retention compliance preventing accidental or unauthorized record deletion.

---

### 2. Database Schema (PostgreSQL)

```sql
-- 1. Archival Series & Collections Table
CREATE TABLE rms_record_series (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    series_code VARCHAR(50) UNIQUE NOT NULL, -- e.g. HREP-SERIES-JOURNALS
    title VARCHAR(255) NOT NULL,
    description TEXT,
    retention_period_years INT NOT NULL, -- 0 for Permanent
    disposition_action VARCHAR(50) NOT NULL, -- PERMANENT_PRESERVATION, NAP_TRANSFER, SECURE_SHREDDING
    legal_basis VARCHAR(255) -- RA 9470, NAP General Circular No. 1
);

-- 2. Archived Record Items Master Table
CREATE TABLE rms_archived_records (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    accession_no VARCHAR(50) UNIQUE NOT NULL, -- HREP-ARCH-2026-00001
    series_id VARCHAR(36) NOT NULL REFERENCES rms_record_series(id),
    congress_number INT NOT NULL,
    record_title VARCHAR(255) NOT NULL,
    originating_department_id VARCHAR(36) REFERENCES departments(id),
    physical_location_box_shelf VARCHAR(100), -- e.g. Vault B, Shelf 4, Box 12
    digital_vault_uri TEXT NOT NULL, -- GCS Archive URI
    sha256_checksum VARCHAR(64) NOT NULL, -- Immutable content hash
    classification_level VARCHAR(30) DEFAULT 'PUBLIC', -- PUBLIC, RESTRICTED, CONFIDENTIAL_EXECUTIVE
    declassification_due_date DATE,
    is_declassified BOOLEAN DEFAULT TRUE,
    accession_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rms_accession ON rms_archived_records(accession_no);
CREATE INDEX idx_rms_congress ON rms_archived_records(congress_number);

-- 3. Declassification Review Logs
CREATE TABLE rms_declassification_logs (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id VARCHAR(36) NOT NULL REFERENCES rms_archived_records(id),
    reviewed_by VARCHAR(36) NOT NULL REFERENCES users(id),
    decision VARCHAR(20) NOT NULL, -- APPROVED, EXTENDED, REJECTED
    justification TEXT NOT NULL,
    secgen_approval_stamp VARCHAR(255) NOT NULL,
    review_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3. REST API Specification

- `POST /api/rms/accession`: Accession new archival records with SHA-256 validation.
- `GET /api/rms/records/?congress=18&series=JOURNALS`: Query historical archive catalog.
- `POST /api/rms/declassify/{id}`: Submit formal declassification review with dual sign-off.
- `GET /api/rms/disposition/eligible`: List records eligible for NAP disposal approval.
