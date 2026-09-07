# BUSINESS REQUIREMENTS DOCUMENT (BRD)
## HRep Insights: Enterprise Reporting & Analytics Platform
### Unified Legislative Intelligence, Operational Lakehouse, and Cross-System Decision Support for the House of Representatives

**Document Reference:** HREP-BRD-S14-2026-v1.0  
**System Code:** UGNAYAN-SYS-14  
**Deployment Tier:** Enterprise Data & Intelligence Layer (High Priority)  
**Target Release:** Phase 2 (Month 6)  
**Classification:** Internal Restricted / Official Business Intelligence Platform  

---

### Table of Contents
1. [Document Control & Sign-off](#1-document-control--sign-off)
2. [Executive Summary & Strategic Mandate](#2-executive-summary--strategic-mandate)
3. [Business Problem Statement & Institutional Pain Points](#3-business-problem-statement--institutional-pain-points)
4. [Project Objectives & Quantifiable Benefits](#4-project-objectives--quantifiable-benefits)
5. [Stakeholder Analysis & Specialized Personas](#5-stakeholder-analysis--specialized-personas)
6. [Scope of Work: In-Scope vs. Out-of-Scope](#6-scope-of-work-in-scope-vs-out-of-scope)
7. [Core Reporting Domains & Analytical Framework](#7-core-reporting-domains--analytical-framework)
8. [Detailed Functional Requirements (FRs)](#8-detailed-functional-requirements-frs)
9. [Non-Functional Requirements (NFRs)](#9-non-functional-requirements-nfrs)
10. [Data Governance, Security & RA 10173 Compliance](#10-data-governance-security--ra-10173-compliance)
11. [UGNAYAN Super App Integration Requirements](#11-ugnayan-super-app-integration-requirements)
12. [Risk Assessment & Mitigation Matrix](#12-risk-assessment--mitigation-matrix)
13. [Implementation Schedule & UAT Acceptance Criteria](#13-implementation-schedule--uat-acceptance-criteria)

---

### 1. Document Control & Sign-off

#### Document History
| Version | Date | Author / Role | Summary of Changes |
| :--- | :--- | :--- | :--- |
| **1.0** | 2026-09-07 | Principal Enterprise Data Architect | Baseline BRD for HRep Insights Reporting & Analytics Platform (System 14) |

#### Approvals
| Role | Name / Title | Department | Signature / Status |
| :--- | :--- | :--- | :--- |
| **Business Sponsor** | Speaker of the House | Office of the Speaker | Approved |
| **Operational Owner**| Secretary General | Office of the Secretary General (OSG) | Approved |
| **Administrative Owner**| Deputy Secretary General, Finance & Admin | Finance & Admin Department | Reviewed |
| **Audit Authority**| Director, Internal Audit Service | Internal Audit Service (IAS) | Reviewed |
| **Technical Authority**| Director, ICTS | Information & Communications Tech. Service | Reviewed |

---

### 2. Executive Summary & Strategic Mandate

The Philippine House of Representatives generates massive volumes of operational, legislative, administrative, financial, and citizen interaction data across its 13 specialized UGNAYAN subsystems. However, this wealth of data currently remains trapped in departmental silos, preventing leadership from acquiring real-time visibility into overall institutional velocity, budget execution, legislative bottlenecks, and service delivery performance.

**HRep Insights (UGNAYAN System 14)** fulfills the mandate for institutional evidence-based decision-making and transparency. It serves as the single source of truth enterprise analytics platform, aggregating operational event streams, transaction logs, and operational databases into a governed modern cloud lakehouse (Google Cloud BigQuery). It empowers the House Leadership, Committee Chairs, Department Directors, and COA/Internal Audit teams with intuitive interactive dashboards, predictive bottleneck alerts, and automated regulatory reporting.

---

### 3. Business Problem Statement & Institutional Pain Points

1. **Fragmented Data Silos:** Financial disbursements (FAD), e-requests (PPU), HR attendance (Lingkod-Kawani), legislative bills (LODS), and inventory movements (PPE) operate in separate datastores, requiring painful manual spreadsheet consolidation.
2. **Lagging Legislative Throughput Metrics:** Committee leadership cannot easily analyze why certain bills stall between 1st reading and committee reporting or identify cross-committee referral backlogs.
3. **Complex Audit & COA Reporting:** Preparing annual COA compliance reports and inventory reconciliation requires weeks of manual reconciliation, exposing the Secretariat to audit observation memorandums (AOMs).
4. **Lack of Citizen Satisfaction Visibility (ARTA Compliance):** Citizen feedback and transaction completion SLAs under RA 11032 are not synthesized into automated executive scorecards.

---

### 4. Project Objectives & Quantifiable Benefits

- **Unified Analytics Single Source of Truth:** 100% of UGNAYAN operational subsystem databases unified into a centralized analytical data warehouse.
- **Reporting Velocity:** Slash statutory and management report preparation time from **14 business days down to real-time self-service queries (< 5 seconds)**.
- **Legislative Cycle Transparency:** Automated tracking of legislative milestones, bill aging metrics, and committee hearing productivity.
- **Proactive Budget & Asset Governance:** Automated reconciliation of Purchase Orders (System 05), Physical Assets (System 10), and Travel Expenses (System 07).

---

### 5. Stakeholder Analysis & Specialized Personas

- **House Leadership (Speaker / Majority Leader):** High-level legislative velocity, priority bill dashboards, plenary quorum analytics.
- **Committee Chairs & Secretaries:** Committee hearing frequency, witness attendance, bill aging, committee report turnaround times.
- **Department Directors (LOD, CAD, FAD, PPU):** Operational performance, employee productivity, SLA compliance under RA 11032.
- **Internal Audit & COA Auditors:** Cross-system audit trails, travel expense anomaly detection, procurement bid analysis.
- **Citizens & Civil Society Organizations (CSOs):** Curated public open data portal for voting records, enacted republic acts, and citizen service metrics.

---

### 6. Scope of Work: In-Scope vs. Out-of-Scope

#### In-Scope
- Near real-time data ingestion (ELT) from all UGNAYAN operational databases (PostgreSQL/Cloud Storage) into BigQuery.
- Curated semantic data models and Looker/Metabase executive dashboards.
- Self-service ad-hoc query builder with role-based row/column-level access control.
- Automated scheduled PDF/Excel report delivery to Secretariat executive email inboxes.
- Public Open Data API and statistical exports for transparency advocacy groups.

#### Out-of-Scope
- Direct operational transaction processing (OLTP updates are handled by Systems 01–13).
- Modification of historical audit logs (audit trail data in the lakehouse is write-once/immutable).

---

### 7. Core Reporting Domains & Analytical Framework

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           HREP INSIGHTS REPORTING DOMAINS                               │
├──────────────────────────┬────────────────────────────┬─────────────────────────────────┤
│ 1. Legislative Analytics │ 2. Secretariat Operations  │ 3. Financial & Resource Control │
│ - Bill Aging & Velocity  │ - ARTA 3-7-20 SLA Metrics  │ - Budget Utilization Rate (BUR) │
│ - Committee Throughput   │ - DTR Attendance Patterns  │ - Travel Expense Compliance     │
│ - Plenary Quorum Trends  │ - DMS Routing Bottlenecks  │ - Asset Lifecycle & Deprec.     │
└──────────────────────────┴────────────────────────────┴─────────────────────────────────┘
```

---

### 8. Detailed Functional Requirements (FRs)

- **FR-14-01 (Automated Ingestion & ELT):** Continuous micro-batch ingestion from all 13 UGNAYAN operational databases into raw BigQuery staging tables using Change Data Capture (CDC).
- **FR-14-02 (Curated Data Marts):** Daily materialized dbt transformations structuring data into dimensional schemas (Star Schema / Fact & Dimension tables).
- **FR-14-03 (Executive KPI Dashboards):** Pre-built interactive dashboards with dynamic slicing by 19th/20th Congress, Committee, Political Party, and Date Range.
- **FR-14-04 (Automated Compliance Alerts):** Trigger automated email/webhook notifications when ARTA SLA breaches exceed 5% or budget variance exceeds 10%.
- **FR-14-05 (Data Export & Scheduled Delivery):** Export to CSV, XLSX, and formatted PDF with digital watermark and timestamping.
- **FR-14-06 (Open Data API):** RESTful endpoints serving public aggregated legislative statistics conforming to Philippine Open Government Partnership (OGP) standards.

---

### 9. Non-Functional Requirements (NFRs)

- **Performance:** 95% of standard analytical queries return in $\le 3.0$ seconds.
- **Data Freshness:** Maximum lag of $\le 15$ minutes for operational operational dashboards; sub-second for plenary active voting counters.
- **Scalability:** Capable of storing 10+ years of congressional records, transactions, and event logs (100+ TB) without performance degradation.
- **High Availability:** 99.9% uptime SLA during regular legislative session periods.

---

### 10. Data Governance, Security & RA 10173 Compliance

- **Column-Level Masking:** Automatic SHA-256 pseudonymization or masking of citizen PII, residential addresses, and personal phone numbers for non-authorized analysts.
- **Row-Level Security (RLS):** Department heads can only inspect granular transaction records belonging to their respective jurisdiction unless granted Secretariat-wide auditor roles.
- **Immutable Audit Logging:** Every SQL query executed against the analytical warehouse is permanently recorded with user identity, timestamp, and query text.

---

### 11. UGNAYAN Super App Integration Requirements

- Single Sign-On integration with Google Workspace / IAP / Keycloak.
- Embedding of contextual widget analytics inside each UGNAYAN subsystem (e.g., embedding the bill velocity widget directly in LODS System 01).
- Deep-linking from analytics alerts directly to the relevant record in the UGNAYAN Super App Action Center.
