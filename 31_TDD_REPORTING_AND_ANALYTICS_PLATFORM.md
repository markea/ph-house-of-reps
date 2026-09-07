# TECHNICAL DESIGN DOCUMENT (TDD)
## HRep Insights: Enterprise Reporting & Analytics Platform
### Modern Lakehouse Architecture, CDC Pipelines, dbt Dimensional Modeling, and Looker / Metabase Semantic Analytics Layer

**Document Reference:** HREP-TDD-S14-2026-v1.0  
**System Code:** UGNAYAN-SYS-14  
**Classification:** Internal Restricted / Official Business Intelligence Architecture  
**Target Deployment:** Google Cloud Platform (BigQuery + Cloud Storage + dbt Core + FastAPI + Looker/Metabase)  

---

### Table of Contents
1. [Architecture Overview & Lakehouse Topology](#1-architecture-overview--lakehouse-topology)
2. [Data Ingestion & Change Data Capture (CDC) Pipeline](#2-data-ingestion--change-data-capture-cdc-pipeline)
3. [Dimensional Data Modeling (dbt Star Schemas)](#3-dimensional-data-modeling-dbt-star-schemas)
4. [Semantic Layer & BI Integration](#4-semantic-layer--bi-integration)
5. [Data Governance, Security & RA 10173 PII Masking](#5-data-governance-security--ra-10173-pii-masking)
6. [Analytics API & Embedded Dashboard Specifications](#6-analytics-api--embedded-dashboard-specifications)
7. [UGNAYAN Super App Integration Architecture](#7-ugnayan-super-app-integration-architecture)

---

### 1. Architecture Overview & Lakehouse Topology

HRep Insights (System 14) aggregates data across all 13 operational UGNAYAN microservices into a unified, high-performance analytical lakehouse on Google Cloud BigQuery.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             OPERATIONAL DATA SOURCES (OLTP)                              │
├─────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┤
│ Systems 01, 02, 03  │ Systems 04, 06, 07   │ Systems 05, 08, 09   │ Systems 10, 11, 12   │
│ (LODS, DMS, RMS)    │ (Sked, VAMS, Travel) │ (e-Req, DTR, SPMS)   │ (PPE, LMS, Exec Dash)│
└──────────┬──────────┴──────────┬───────────┴──────────┬───────────┴──────────┬───────────┘
           │                     │                      │                      │
           ▼                     ▼                      ▼                      ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                   INGESTION & CHANGE DATA CAPTURE LAYER (CDC / STREAMING)                │
│  - Debezium / Cloud Datastream PostgreSQL CDC Connectors                                 │
│  - Google Cloud Pub/Sub Real-time Event Mesh                                             │
└────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         GOOGLE CLOUD BIGQUERY LAKEHOUSE STORAGE                          │
│ ┌──────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. Bronze Layer (Raw Ingestion / Landing Tables)                                      │ │
│ │    - raw_hrep_operational_events (JSON payload, append-only)                         │ │
│ │    - raw_postgresql_table_mirrors (CDC replicated)                                   │ │
│ ├──────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. Silver Layer (Cleaned, Standardized & Conformed Data Marts)                       │ │
│ │    - Transformed via dbt Core / BigQuery SQL                                         │ │
│ │    - PII Pseudonymized / RA 10173 Compliance Filters Applied                         │ │
│ ├──────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. Gold Layer (Dimensional Star Schema / Fact & Dimension Tables)                    │ │
│ │    - fact_legislative_milestones, fact_service_requests, fact_attendance             │ │
│ │    - dim_members, dim_committees, dim_departments, dim_calendar_dates                │ │
│ └──────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                          SEMANTIC LAYER & EMBEDDED ANALYTICS API                         │
│  - Looker / Metabase Semantic Models (Metrics definitions, drill-downs)                  │
│  - FastAPI HRep Insights Microservice (`/api/v1/analytics/*`)                            │
│  - Embedded Signed Iframe Dashboards inside UGNAYAN Super App Shell                      │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Data Ingestion & Change Data Capture (CDC) Pipeline

#### 2.1 Ingestion Topology
1. **Real-time Change Data Capture (CDC):** Google Cloud Datastream captures write-ahead logs (WAL) from PostgreSQL database instances and streams changes directly into BigQuery Bronze landing datasets with sub-minute latency.
2. **Audit & Event Stream Ingestion:** High-volume operational events published to Pub/Sub topics (`ugnayan.events.*`) are continuously written into BigQuery partitioned streaming tables via BigQuery Subscription without intermediate servers.

---

### 3. Dimensional Data Modeling (dbt Star Schemas)

#### 3.1 Star Schema Definition (Gold Analytics Layer)

```sql
-- Dimensional Model: Gold Layer DDL

-- 1. Date Dimension
CREATE TABLE hrep_gold.dim_dates (
    date_key DATE PRIMARY KEY,
    day_of_week STRING,
    is_weekend BOOLEAN,
    is_congressional_session_day BOOLEAN,
    is_ph_holiday BOOLEAN,
    fiscal_year INT64,
    congress_number INT64
);

-- 2. Lawmaker Dimension
CREATE TABLE hrep_gold.dim_members (
    member_id STRING PRIMARY KEY,
    full_name STRING,
    district_or_partylist STRING,
    region STRING,
    political_party STRING,
    is_committee_chair BOOLEAN,
    tenure_start_date DATE,
    tenure_end_date DATE,
    is_active BOOLEAN
);

-- 3. Fact: Legislative Milestones
CREATE TABLE hrep_gold.fact_legislative_milestones (
    milestone_id STRING PRIMARY KEY,
    bill_id STRING,
    bill_number STRING,
    committee_id STRING,
    principal_author_id STRING,
    milestone_type STRING, -- 'FILED', 'FIRST_READING', 'COMMITTEE_REPORT', 'SECOND_READING', 'THIRD_READING', 'ENACTED'
    date_key DATE REFERENCES hrep_gold.dim_dates(date_key),
    days_in_previous_stage INT64,
    quorum_count INT64,
    yes_votes INT64,
    no_votes INT64,
    abstain_votes INT64
)
PARTITION BY date_key
CLUSTER BY committee_id, milestone_type;

-- 4. Fact: Service Requests & ARTA SLA Performance
CREATE TABLE hrep_gold.fact_service_requests (
    request_id STRING PRIMARY KEY,
    tracking_number STRING,
    department_id STRING,
    service_type_id STRING,
    date_key DATE REFERENCES hrep_gold.dim_dates(date_key),
    sla_category STRING, -- 'SIMPLE_3D', 'COMPLEX_7D', 'HIGHLY_TECH_20D'
    processing_time_hours NUMERIC,
    is_sla_breached BOOLEAN,
    citizen_feedback_rating INT64,
    status STRING
)
PARTITION BY date_key
CLUSTER BY department_id, is_sla_breached;
```

---

### 4. Semantic Layer & BI Integration

- **Standardized Metric Calculations:**
  - **Legislative Throughput Index (LTI):** $\frac{\text{Bills Approved on 3rd Reading}}{\text{Total Bills Filed}} \times 100\%$
  - **ARTA SLA Compliance Rate:** $\frac{\text{Requests Completed within Working Day Limit}}{\text{Total Completed Requests}} \times 100\%$
  - **Budget Execution Velocity:** $\frac{\text{Obligations Incurred to Date}}{\text{Total Allotment Released}} \times 100\%$
- **Looker / Metabase Semantic Models:** Metric definitions are centralized in version-controlled dbt semantic models ensuring zero discrepancies across departmental reports.

---

### 5. Data Governance, Security & RA 10173 PII Masking

```sql
-- BigQuery Row-Level Security Example
CREATE OR REPLACE ROW ACCESS POLICY dept_analyst_filter
ON hrep_gold.fact_service_requests
GRANT TO ('group:dept-analysts@hrep.gov.ph')
FILTER USING (department_id = SESSION_USER_DEPARTMENT());

-- BigQuery Column-Level Policy Tags (PII Masking)
-- Applies automatic SHA-256 hash masking for citizen national ID, phone, and home address.
```

---

### 6. Analytics API & Embedded Dashboard Specifications

#### 6.1 Endpoints
- `GET /api/v1/analytics/legislative/summary`: Aggregate counts of bills by stage, author, and committee.
- `GET /api/v1/analytics/arta/compliance`: Real-time SLA compliance percentages across all secretariat departments.
- `GET /api/v1/analytics/budget/utilization`: Budget Allotment vs. Obligation vs. Disbursement trends.
- `POST /api/v1/analytics/reports/generate`: Request custom generated PDF/Excel executive dossiers.

---

### 7. UGNAYAN Super App Integration Architecture

1. **Dashboard Embedding:** Secure signed Looker Embed URLs / Metabase tokens injected into React frontend tabs in the UGNAYAN Super App shell.
2. **Contextual In-App Widgets:** Micro-charts embedded in individual system UIs (e.g., SLA speedometer on e-Requests dashboard).
3. **Automated Notification Triggers:** Cloud Functions monitor BigQuery scheduled query anomalies and dispatch urgent alerts to the Super App Universal Action Center.
