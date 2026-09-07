# Technical Design Document (TDD)
## System 09: Planning, Monitoring & Evaluation System (Target-Kongreso SPMS)
### UGNAYAN Super App - Strategic Performance & SPMS Module

**Document Reference:** HREP-UGNAYAN-TDD-2026-022  
**Target Organization:** House of Representatives of the Philippines (HRep) Secretariat  
**Author:** Technical Consulting & Solutions Architecture Team  
**Date:** September 2026  
**Status:** Approved for Core Engineering  

---

### 1. Architectural Design & Scoring Algorithm

The Target-Kongreso engine automates SPMS score aggregation across 15 Secretariat departments:

$$\text{FinalScore} = \sum_{i=1}^{K} \left( \text{Weight}_i \times \frac{Q_i + E_i + T_i}{3} \right)$$
- **Outstanding:** $4.500 - 5.000$
- **Very Satisfactory:** $3.500 - 4.499$
- **Satisfactory:** $2.500 - 3.499$
- **Unsatisfactory:** $1.500 - 2.499$
- **Poor:** Below $1.500$

---

### 2. Database Schema (PostgreSQL)

```sql
-- 1. Strategic Goals & Institutional MFOs
CREATE TABLE pme_strategic_goals (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    fiscal_year INT NOT NULL,
    goal_code VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_metric VARCHAR(100) NOT NULL,
    target_value NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Office Performance Commitment and Review (OPCR)
CREATE TABLE pme_opcr_plans (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id VARCHAR(36) NOT NULL REFERENCES departments(id),
    rating_period_year INT NOT NULL,
    rating_period_semester INT NOT NULL CHECK (rating_period_semester IN (1, 2)),
    status VARCHAR(30) DEFAULT 'DRAFT', -- DRAFT, SUBMITTED_PMRB, APPROVED, EVALUATED
    overall_rating NUMERIC(4, 3),
    adjectival_rating VARCHAR(30),
    approved_by_secgen_stamp VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Success Indicators & Accomplishments
CREATE TABLE pme_success_indicators (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    opcr_id VARCHAR(36) NOT NULL REFERENCES pme_opcr_plans(id) ON DELETE CASCADE,
    mfo_title VARCHAR(255) NOT NULL,
    performance_indicator TEXT NOT NULL,
    target_quantity INT NOT NULL,
    actual_accomplishment INT DEFAULT 0,
    weight_percentage NUMERIC(5, 2) NOT NULL,
    rating_quality NUMERIC(3, 2) DEFAULT 0.00,
    rating_efficiency NUMERIC(3, 2) DEFAULT 0.00,
    rating_timeliness NUMERIC(3, 2) DEFAULT 0.00,
    average_score NUMERIC(4, 3) DEFAULT 0.000,
    evidence_document_uri TEXT
);

-- 4. Individual Performance Commitment (IPCR)
CREATE TABLE pme_ipcr_plans (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    opcr_id VARCHAR(36) NOT NULL REFERENCES pme_opcr_plans(id),
    final_numerical_rating NUMERIC(4, 3),
    final_adjectival_rating VARCHAR(30),
    status VARCHAR(30) DEFAULT 'PENDING_REVIEW'
);
```

---

### 3. REST API Specification

- `POST /api/pme/opcr/`: Create / update departmental OPCR commitment targets.
- `POST /api/pme/ipcr/submit-accomplishment`: Log actual deliverable proof and calculate auto (Q, E, T) score.
- `GET /api/pme/dashboard/secretariat-scorecard?year=2026`: Real-time executive performance dashboard.
