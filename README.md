# UGNAYAN: HREP SECRETARIAT DIGITAL TRANSFORMATION PROGRAM
## Technical Advisory & Requirements Architecture Workspace
### Complete 14-System Business Requirements Documents (BRDs), Technical Design Documents (TDDs), and UGNAYAN Super App Platform Architecture

**Client:** House of Representatives of the Philippines (HRep) Secretariat  
**Program:** UGNAYAN Digital Transformation Program  
**Prepared by:** Technical Consulting & Solutions Architecture Team  
**Date:** September 2026  
**Workspace Path:** `/usr/local/google/home/markea/Desktop/hor`  
**Git Repository:** `https://github.com/markea/ph-house-of-reps` (branch `main`)  

---

### Executive Overview

This workspace contains the complete technical analysis, prioritization framework, formal **Business Requirements Documents (BRDs)**, **Technical Design Documents (TDDs)**, and reference implementations developed for the **House of Representatives (HRep) Secretariat** under the **UGNAYAN Digital Transformation Program**.

The HRep Secretariat provides essential administrative, legal, technical, and operational machinery for the 315+ Members of the Philippine House of Representatives. Currently, operations are constrained by fragmented legacy tools (e.g., custom *Housedocs*, on-premise *Globodox*, disparate Google Drives, and physical paper folders), manual multi-office routing slips, heavy legislative transcription backlogs, travel clearance/liquidation bottlenecks, and physical perimeter access queues at the Batasan Pambansa complex.

This deliverables package provides **100% complete coverage for all 14 Common Systems** mandated by the UGNAYAN Charter, unifying them under a shared **UGNAYAN Super App Platform Architecture** while maintaining standalone modularity for independent software development execution.

---

### Master Deliverables Directory (32 Core Artifacts)

| Ref # | Document / Deliverable | System / Domain | Description & Architectural Scope |
| :--- | :--- | :--- | :--- |
| `00` | [00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md](file:///usr/local/google/home/markea/Desktop/hor/00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md) | **Strategic Assessment** | Institutional landscape analysis (15 offices), 14-system prioritization scoring, 24-month phased roadmap, and GAD compliance. |
| `08` | [08_TDD_UGNAYAN_SUPER_APP_ARCHITECTURE.md](file:///usr/local/google/home/markea/Desktop/hor/08_TDD_UGNAYAN_SUPER_APP_ARCHITECTURE.md) | **Core Super App Platform** | Single Sign-On (Google IAP / Keycloak OIDC), API Gateway, Universal Action Center, shared PostgreSQL/BigQuery schema, and Pub/Sub mesh. |
| `09` | [09_BRD_LEGISLATIVE_OPERATIONS_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/09_BRD_LEGISLATIVE_OPERATIONS_SYSTEM.md) | **System 01: Batas-Bayan (LODS)** | BRD for digital bill lifecycle, committee referrals, plenary amendments, digital voting roll call, and Republic Act transmission. |
| `10` | [10_TDD_LEGISLATIVE_OPERATIONS_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/10_TDD_LEGISLATIVE_OPERATIONS_SYSTEM.md) | **System 01: Batas-Bayan (LODS)** | TDD for high-availability plenary engine, real-time WebSocket voting, bill state machines, and DMS/RMS synchronizers. |
| `11` | [11_BRD_DOCUMENT_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/11_BRD_DOCUMENT_MANAGEMENT_SYSTEM.md) | **System 02: Housedocs Modernization** | BRD for centralized optical character recognition (OCR), metadata indexing, full-text search, and cross-department document routing. |
| `12` | [12_TDD_DOCUMENT_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/12_TDD_DOCUMENT_MANAGEMENT_SYSTEM.md) | **System 02: Housedocs Modernization** | TDD for Cloud Storage / MinIO bucket tiering, PostgreSQL pgvector embeddings, and Tesseract/Cloud Vision OCR pipeline. |
| `13` | [13_BRD_RECORDS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/13_BRD_RECORDS_MANAGEMENT_SYSTEM.md) | **System 03: HRep Archives (RMS)** | BRD for National Archives of the Philippines (NAP) retention compliance, archival accessioning, declassification, and pest/climate tracking. |
| `14` | [14_TDD_RECORDS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/14_TDD_RECORDS_MANAGEMENT_SYSTEM.md) | **System 03: HRep Archives (RMS)** | TDD for WORM (Write Once Read Many) immutable Cloud Storage, retention lifecycle workers, and digital preservation checksums. |
| `15` | [15_BRD_SHARED_CALENDAR_SCHEDULING_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/15_BRD_SHARED_CALENDAR_SCHEDULING_SYSTEM.md) | **System 04: Kumberso-Sked** | BRD for plenary/committee room reservations, lawmaker hearing conflict detection, and digital hearing notices. |
| `16` | [16_TDD_SHARED_CALENDAR_SCHEDULING_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/16_TDD_SHARED_CALENDAR_SCHEDULING_SYSTEM.md) | **System 04: Kumberso-Sked** | TDD for Google Calendar API two-way sync, CalDAV server, Redis room conflict locks, and digital signage displays. |
| `01` | [01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md) | **System 05: e-Request Portal** | BRD for unified administrative service catalog eliminating routing slips across 12 offices (PPU, Motorpool, ICTS, Building Maint). |
| `05` | [05_TDD_ONLINE_SERVICE_REQUEST_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/05_TDD_ONLINE_SERVICE_REQUEST_SYSTEM.md) | **System 05: e-Request Portal** | TDD detailing dual-mode execution (Local vs. GCP), PostgreSQL JSONB dynamic forms, IAP authentication, and ADK AI Agent. |
| `06` | [06_PRODUCTION_DEPLOYMENT_PLAN_E_REQUESTS.md](file:///usr/local/google/home/markea/Desktop/hor/06_PRODUCTION_DEPLOYMENT_PLAN_E_REQUESTS.md) | **System 05: e-Request Portal** | Production hardening plan covering Cloud Run concurrency, Cloud SQL pooling, IAP token validation, and Terraform IaC. |
| `e-requests/` | [e-requests/](file:///usr/local/google/home/markea/Desktop/hor/e-requests/) | **System 05: Reference Codebase** | Full FastAPI/Python application, dynamic schema engine, ADK AI Triage agent, and 18/18 passing pytest test suite. |
| `03` | [03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md) | **System 06: Batasan Pass (VAMS)** | BRD for perimeter gate security, sponsor approvals, rotating QR-passes, handheld gate scanners, and emergency muster. |
| `17` | [17_TDD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/17_TDD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md) | **System 06: Batasan Pass (VAMS)** | TDD for TOTP rotating QR-code cryptographic tokens, offline-capable PWA scanner, turnstile relay controllers, and OSAA watchlists. |
| `04` | [04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md) | **System 07: Lakbay-Kongreso** | BRD for local/foreign travel, automated EO 77/UNDP per diems, DFA passport vault, mobile receipt COA liquidation, and IPAD archives. |
| `18` | [18_TDD_TRAVEL_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/18_TDD_TRAVEL_MANAGEMENT_SYSTEM.md) | **System 07: Lakbay-Kongreso** | TDD for automated statutory per diem calculation engine, COA OCR expense extraction, and passport custody tracking. |
| `19` | [19_BRD_HR_ATTENDANCE_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/19_BRD_HR_ATTENDANCE_MANAGEMENT_SYSTEM.md) | **System 08: Lingkod-Kawani (DTR)** | BRD for biometric/geofenced attendance, Civil Service Commission (CSC) Form 48, digital leave ledger, and monetization. |
| `20` | [20_TDD_HR_ATTENDANCE_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/20_TDD_HR_ATTENDANCE_MANAGEMENT_SYSTEM.md) | **System 08: Lingkod-Kawani (DTR)** | TDD for biometric clock TCP push receiver, Haversine geofence verification, automated leave accrual engine, and CSC Form 48 PDF renderer. |
| `21` | [21_BRD_PLANNING_MONITORING_EVALUATION_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/21_BRD_PLANNING_MONITORING_EVALUATION_SYSTEM.md) | **System 09: Target-Kongreso (SPMS)** | BRD for Strategic Performance Management System (SPMS), OPCR/IPCR rating cycles, milestone tracking, and PBB incentive calculations. |
| `22` | [22_TDD_PLANNING_MONITORING_EVALUATION_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/22_TDD_PLANNING_MONITORING_EVALUATION_SYSTEM.md) | **System 09: Target-Kongreso (SPMS)** | TDD for SPMS performance score calculators, PMT calibration workflow engines, and automated performance reward ledgers. |
| `23` | [23_BRD_INVENTORY_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/23_BRD_INVENTORY_MANAGEMENT_SYSTEM.md) | **System 10: Asset-Track (PPE)** | BRD for Property, Plant & Equipment (PPE), RFID/barcode tagging, PAR/ICS issuance, COA depreciation, and annual physical inventory. |
| `24` | [24_TDD_INVENTORY_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/24_TDD_INVENTORY_MANAGEMENT_SYSTEM.md) | **System 10: Asset-Track (PPE)** | TDD for RFID scanner MQTT broker, COA straight-line depreciation calculation workers, and digital PAR cryptographic signing. |
| `25` | [25_BRD_LEARNING_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/25_BRD_LEARNING_MANAGEMENT_SYSTEM.md) | **System 11: Kongreso Academy** | BRD for legislative staff onboarding, bill drafting masterclasses, SCORM/xAPI course tracking, and accredited training certificates. |
| `26` | [26_TDD_LEARNING_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/26_TDD_LEARNING_MANAGEMENT_SYSTEM.md) | **System 11: Kongreso Academy** | TDD for SCORM/xAPI compliant learning runtime, Cloudflare Stream / HLS video delivery, quiz evaluation engine, and PDF certificate signer. |
| `27` | [27_BRD_EXECUTIVE_DASHBOARD_COMMAND_CENTER.md](file:///usr/local/google/home/markea/Desktop/hor/27_BRD_EXECUTIVE_DASHBOARD_COMMAND_CENTER.md) | **System 12: Command Center** | BRD for Speaker / Secretary General real-time command center, plenary live floor telemetry, budget burn rate, and ARTA SLA heatmaps. |
| `28` | [28_TDD_EXECUTIVE_DASHBOARD_COMMAND_CENTER.md](file:///usr/local/google/home/markea/Desktop/hor/28_TDD_EXECUTIVE_DASHBOARD_COMMAND_CENTER.md) | **System 12: Command Center** | TDD for Redis Pub/Sub low-latency WebSocket live updates, TimescaleDB time-series storage, and React wallboard dashboard. |
| `02` | [02_BRD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/02_BRD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md) | **System 13: Lingkod-Dinig AI** | BRD for plenary/committee speech-to-text, Taglish code-switching, stenographer audio-synced editor, and air-gapped Executive Sessions. |
| `29` | [29_TDD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/29_TDD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md) | **System 13: Lingkod-Dinig AI** | TDD for Google Cloud Chirp 2, PyAnnote diarization, air-gapped on-prem Whisper v3, WaveSurfer.js foot pedal editor, and LLM minutes generator. |
| `30` | [30_BRD_REPORTING_AND_ANALYTICS_PLATFORM.md](file:///usr/local/google/home/markea/Desktop/hor/30_BRD_REPORTING_AND_ANALYTICS_PLATFORM.md) | **System 14: HRep Insights** | BRD for enterprise data lakehouse, cross-department analytics, legislative velocity tracking, and COA/ARTA compliance dashboards. |
| `31` | [31_TDD_REPORTING_AND_ANALYTICS_PLATFORM.md](file:///usr/local/google/home/markea/Desktop/hor/31_TDD_REPORTING_AND_ANALYTICS_PLATFORM.md) | **System 14: HRep Insights** | TDD for BigQuery dimensional lakehouse, Datastream CDC, dbt Core transformations, Looker/Metabase semantic models, and row/column security. |
| `32` | [32_UGNAYAN_GCP_COST_ESTIMATE_SINGAPORE.md](file:///usr/local/google/home/markea/Desktop/hor/32_UGNAYAN_GCP_COST_ESTIMATE_SINGAPORE.md)<br/>📊 Standard CSVs: [32A Shared BOM](file:///usr/local/google/home/markea/Desktop/hor/32A_UGNAYAN_GCP_SKU_BOM_SINGAPORE.csv) • [32B Per-System](file:///usr/local/google/home/markea/Desktop/hor/32B_UGNAYAN_PER_SYSTEM_COST_ALLOCATION.csv) • [32C 24-Mo Cashflow](file:///usr/local/google/home/markea/Desktop/hor/32C_UGNAYAN_24_MONTH_PHASED_BUDGET_CASHFLOW.csv)<br/>🏛️ Federated 15-System CSVs: [32D 15-System SKU BOM](file:///usr/local/google/home/markea/Desktop/hor/32D_UGNAYAN_FEDERATED_15_SYSTEM_SKU_BOM_SINGAPORE.csv) • [32E 15-System Summary](file:///usr/local/google/home/markea/Desktop/hor/32E_UGNAYAN_FEDERATED_SYSTEMS_SUMMARY.csv)<br/>🚀 High-Scale (100K Users/Wk) CSVs: [32F 100K Federated BOM](file:///usr/local/google/home/markea/Desktop/hor/32F_UGNAYAN_100K_USERS_FEDERATED_15_SYSTEM_BOM.csv) • [32G 100K Shared BOM](file:///usr/local/google/home/markea/Desktop/hor/32G_UGNAYAN_100K_USERS_SHARED_SUPER_APP_BOM.csv) | **FinOps & Budget (ABC)** | Granular GCP Singapore (`asia-southeast1`) cost estimates for all 14 systems + UGNAYAN Super-App Hub across Standard and 100,000 Users/Week High-Scale capacities. |
| `07` | [07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md](file:///usr/local/google/home/markea/Desktop/hor/07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md) | **Technical FAQ** | Master FAQ covering authentication (Google IAP), local vs. cloud execution, statutory compliance, AI evaluation, and Antigravity slash commands. |

---

### Core UGNAYAN Super App Platform Topology

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    UGNAYAN SUPER APP SHELL                                      │
│                (React 18 Microfrontend Architecture + Mobile Capacitor iOS/Android)            │
├───────────────────────────────┬─────────────────────────────────┬───────────────────────────────┤
│ 🏛️ LEGISLATIVE PILLAR         │ 📋 OPERATIONS & SERVICES PILLAR │ 📊 INTELLIGENCE & AUDIT PILLAR│
│ - System 01: LODS             │ - System 05: e-Requests Portal  │ - System 12: Command Center   │
│ - System 02: DMS              │ - System 06: Batasan Pass VAMS  │ - System 13: Lingkod-Dinig AI │
│ - System 03: RMS Archives     │ - System 07: Travel Management  │ - System 14: HRep Insights DW │
│ - System 04: Calendar Sked    │ - System 08: Lingkod-Kawani DTR │                               │
│                               │ - System 09: Target SPMS        │                               │
│                               │ - System 10: PPE Inventory      │                               │
│                               │ - System 11: Kongreso Academy   │                               │
└───────────────────────────────┴─────────────────────────────────┴───────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            ENTERPRISE API GATEWAY & COMMON SERVICES                             │
│  - Google Identity-Aware Proxy (IAP) / Keycloak OIDC Single Sign-On                             │
│  - Unified Role-Based Access Control (RBAC) & Institutional Jurisdiction Filter                 │
│  - Universal Action Center Hub (Cross-System Approvals, Tasks, Routing Slips)                   │
│  - Asynchronous Event Mesh (Google Cloud Pub/Sub Topics: `ugnayan.events.*`)                     │
└───────────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          SHARED ENTERPRISE DATA & ANALYTICS FABRIC                              │
│  - PostgreSQL 16 (OLTP Multi-Tenant Subsystem Databases with pgvector)                          │
│  - Google Cloud Storage / MinIO (Encrypted WORM Object Storage for Documents & Recordings)      │
│  - Google Cloud BigQuery (Enterprise Analytical Lakehouse & dbt Dimensional Data Marts)         │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Statutory Compliance & Regulatory Framework

All systems in the UGNAYAN portfolio strictly enforce Philippine legal and civil service statutes:
1. **Republic Act No. 10173 (Data Privacy Act of 2012):** Strict data minimization, TLS 1.3/AES-256 encryption at rest, automatic PII masking, and 30-day visitor log purging.
2. **Republic Act No. 11032 (Ease of Doing Business & Efficient Government Service Delivery Act of 2018):** Strict enforcement of 3-day (simple), 7-day (complex), and 20-day (highly technical) transaction SLAs with automated escalation triggers.
3. **Executive Order No. 77 (s. 2019):** Automated per diem rate computation (DTA Clusters I, II, III and UNDP DSA).
4. **COA Circulars No. 2012-001 & 2023-004:** Strict liquidation tracking, prevention of unliquidated cash advance accumulation, and immutable audit logs.
5. **Civil Service Commission (CSC) Rules & Omnibus Rules on Leave:** Automated CSC Form 48 monthly DTR generation, leave ledger accrual, and SPMS calibration.
6. **National Archives of the Philippines (NAP) General Circulars:** Records retention schedules, disposal authorizations, and permanent preservation standards.

---

### Antigravity Slash Commands Acceleration Guide

During project ideation, refinement, implementation, and quality auditing, team members can leverage specialized Antigravity slash commands in the chat interface:

- 🎯 `/goal`: **Ideation & Autonomous Execution:** Runs deep, long-running tasks (e.g. overnight) and ensures the agent is extra thorough until the objective is fully achieved without stopping early.
- 🎙️ `/grill-me`: **Requirements Alignment & Interview:** Proactively interviews the user through an interactive question tree to resolve design decisions, statutory trade-offs, and user preferences.
- 📋 `/plan`: **Technical Planning & Safety Gate:** Researches the codebase and creates an implementation plan artifact for user review before touching any code or making modifications.
- 🦉 `/owl`: **Deep Reasoning & Multi-Perspective Architecture:** Engages in rigorous analysis, evaluating edge cases, security postures, and alternative technical strategies for complex projects.
- 🌐 `/browser`: **Live Web Research & Investigation:** Navigates live web pages, parses online statutory circulars, documentation, or portals.
- 👥 `/teamwork-preview`: **Multi-Agent Orchestration:** Deploys a coordinated team of autonomous subagents working simultaneously across tasks.
- ⏰ `/schedule`: **Continuous Automation & Cron:** Schedules recurring background checks or one-time timers to monitor deployments or builds.
- 🧠 `/learn`: **Knowledge Persistence:** Records user preferences, project setup nuances, or corrections so the agent retains them forever.

*(For detailed examples and FAQ on command usage, refer to [07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md](file:///usr/local/google/home/markea/Desktop/hor/07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md)).*
