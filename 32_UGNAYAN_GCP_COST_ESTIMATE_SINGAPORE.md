# UGNAYAN: HREP SECRETARIAT DIGITAL TRANSFORMATION PROGRAM
## Google Cloud Platform (GCP) Infrastructure & AI Cost Estimates (Singapore Region `asia-southeast1`)
### Granular Per-System Breakdown, Shared Super App BOM, and 24-Month Phased Budget Forecast

**Document Reference:** HREP-UGNAYAN-FINOPS-2026-032  
**Target Organization:** House of Representatives of the Philippines (HRep) Secretariat — ICTS & Finance Department  
**Cloud Region:** Google Cloud Singapore (`asia-southeast1`)  
**Currency Conversion:** 1.00 USD = 58.50 PHP (Budgetary Planning Rate with FX Buffer)  
**Date:** September 2026  
**Status:** Approved for BAC Approved Budget for the Contract (ABC) & DBM Budget Defense  

---

### Table of Contents
1. [Executive Summary & TCO Highlights](#1-executive-summary--tco-highlights)
2. [Institutional Workload & Sizing Assumptions](#2-institutional-workload--sizing-assumptions)
3. [Architectural Efficiency: Shared Super App vs. 14 Siloed Deployments](#3-architectural-efficiency-shared-super-app-vs-14-siloed-deployments)
4. [Granular Cost Breakdown by Use-Case (All 14 Systems)](#4-granular-cost-breakdown-by-use-case-all-14-systems)
5. [Master Bill of Materials (BOM) — Singapore Region (`asia-southeast1`)](#5-master-bill-of-materials-bom--singapore-region-asia-southeast1)
6. [Phased 24-Month Rollout Budget (Phase 1 to Phase 4)](#6-phased-24-month-rollout-budget-phase-1-to-phase-4)
7. [HRep FinOps & Cost-Optimization Strategies](#7-hrep-finops--cost-optimization-strategies)

---

### 1. Executive Summary & TCO Highlights

This document provides the official Google Cloud Platform (GCP) infrastructure, database, storage, networking, and Artificial Intelligence (Vertex AI / Speech-to-Text Chirp 2 / Gemini 2.5) cost estimates for the **UGNAYAN Digital Transformation Program** deployed in the **Singapore (`asia-southeast1`)** region.

By unifying all 14 Secretariat systems under the **UGNAYAN Super App Platform Architecture** ([08_TDD_UGNAYAN_SUPER_APP_ARCHITECTURE.md](file:///usr/local/google/home/markea/Desktop/hor/08_TDD_UGNAYAN_SUPER_APP_ARCHITECTURE.md)), the House of Representatives eliminates redundant database licensing, duplicate load balancers, and idle compute overhead—reducing total cloud infrastructure expenditure by **73.8%** compared to deploying 14 standalone software silos.

#### Summary Cost Matrix (Full Production Scale — All 14 Systems Live)

| Pricing Model | Monthly Cost (USD) | Monthly Cost (PHP) | Annual Cost (USD) | Annual Cost (PHP) | Recommended Use Case |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **On-Demand List Price** | **$2,845 / mo** | **₱166,433 / mo** | **$34,140 / yr** | **₱1,997,190 / yr** | Initial ramp-up & flexible elasticity |
| **1-Year Committed Use (CUD)** | **$2,290 / mo** | **₱133,965 / mo** | **$27,480 / yr** | **₱1,607,580 / yr** | **Recommended for GAA Annual Budget** |
| **3-Year Committed Use (CUD)** | **$1,865 / mo** | **₱109,103 / mo** | **$22,380 / yr** | **₱1,309,230 / yr** | Multi-Year Obligational Authority (MYOA) |

> [!TIP]
> **Phase 1 Quick Wins Budget (Months 1–3):** Launching the Top 4 Phase 1 systems (**e-Request Portal**, **Lakbay-Kongreso Travel**, **Batasan Pass VAMS**, and **Lingkod-Dinig AI Transcription**) requires an initial cloud run-rate of only **$1,120 / month (~₱65,520 / month)** on-demand in Singapore (`asia-southeast1`).

---

### 2. Institutional Workload & Sizing Assumptions

All estimates are calibrated to the actual operational scale of the House of Representatives at the Batasan Pambansa Complex:

1. **Active Internal Users (~4,000 Concurrent/Daily Users):**
   - **315+ Congressional District & Party-List Offices** (approx. 6–10 staff per office = ~2,500 legislative staff).
   - **15 Secretariat Departments & Bureaus** (~1,500 permanent plantilla, contractual, and technical staff).
2. **External / Public Touchpoints (~80,000 Monthly Transactions):**
   - **Batasan Pass (VAMS):** 2,500 to 5,000 daily visitors during session days (~75,000 QR passes issued/scanned per month).
3. **Legislative & Committee Audio Transcription (~300 Audio Hours / Month):**
   - **60+ Standing and Special Committees** + **Plenary Sessions** generating ~15 hours of recorded proceedings per session day (~300 hours or 18,000 minutes per month) processed through **Google Cloud Speech-to-Text V2 (Chirp 2 Taglish model)** and **Gemini 2.5 Pro/Flash**.
4. **Enterprise Document & Archival Storage (~6 TB Year 1 $\rightarrow$ 18 TB Year 3):**
   - High-resolution PDF bills, committee reports, COA travel liquidation receipts, CCTV/ID snapshots, and audio/video masters stored across **Cloud Storage Standard, Nearline, and Archive (WORM)** tiers.
5. **Parliamentary Session Traffic Profile:**
   - Peak compute loads occur Monday–Wednesday (Plenary & Committee days, 8:00 AM – 8:00 PM PHT). Thursday–Sunday and Congressional Recess periods experience 70% lower compute demand, which **Cloud Run auto-scaling** automatically captures.

---

### 3. Architectural Efficiency: Shared Super App vs. 14 Siloed Deployments

If HRep procured 14 separate software systems from different vendors, each vendor would provision its own isolated PostgreSQL HA database, load balancer, Redis cluster, and NAT gateway. The UGNAYAN Super App consolidates these into a shared high-availability fabric:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       MONTHLY GCP COST COMPARISON (SINGAPORE)                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ❌ 14 Siloed Vendor Deployments (14x DBs, 14x LBs, 14x Redis) :  $10,850 / month      │
│  ✅ UGNAYAN Shared Super App Architecture (Unified Fabric)      :   $2,845 / month      │
│  ────────────────────────────────────────────────────────────────────────────────────  │
│  💰 NET INSTITUTIONAL SAVINGS FOR HREP                         :   $8,005 / month (-74%)│
│                                                                : ₱468,293 / month      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

| Infrastructure Layer | 14 Siloed Systems Approach | UGNAYAN Shared Super App Approach | Monthly Savings (USD) |
| :--- | :--- | :--- | :---: |
| **Relational Database (Cloud SQL HA)** | 14x separate `db-custom-2-7680` HA instances ($410 x 14 = $5,740) | 1x Enterprise Shared `db-custom-8-32768` HA + Read Replica ($1,240) | **-$4,500 / mo** |
| **Application Compute (Cloud Run)** | 28x minimum warm containers across 14 silos ($1,680) | Consolidated modular FastAPI microservices with shared worker pool ($480) | **-$1,200 / mo** |
| **Load Balancing & WAF (Cloud Armor)** | 14x External Application LBs + 14x WAF policies ($630) | 1x Global Application LB + Unified IAP + Host/Path Routing ($65) | **-$565 / mo** |
| **In-Memory Cache (Memorystore Redis)** | 14x separate Redis instances ($1,932) | 1x Shared HA Redis M2 Cluster with namespace key isolation ($138) | **-$1,794 / mo** |
| **AI, Storage & BigQuery Lakehouse** | Fragmented storage buckets & duplicate AI calls ($868) | Unified GCS WORM Lakehouse + Shared Vertex AI ADK Gateway ($922) | **+$54 / mo** |
| **TOTAL MONTHLY RUN-RATE (ON-DEMAND)** | **$10,850 / mo (₱634,725)** | **$2,845 / mo (₱166,433)** | **-$8,005 / mo (-73.8%)** |

---

### 4. Granular Cost Breakdown by Use-Case (All 14 Systems)

Below is the system-by-system cost attribution. Each row shows the **Standalone Cost** (if deployed alone) vs. the **Marginal Cost inside UGNAYAN** (sharing the core Cloud SQL HA cluster, Load Balancer, Redis, and IAP security layer).

#### Tier 1: Foundational Systems

| System # & Name | Primary GCP Resources & Workload Drivers | Standalone Monthly (USD) | UGNAYAN Marginal Monthly (USD) | UGNAYAN Marginal Monthly (PHP) |
| :--- | :--- | :---: | :---: | :---: |
| **Shared Core Platform**<br/>*(Super App Shell, IAP, DB, Redis, Bus)* | • **Cloud SQL Postgres HA** (`db-custom-8-32768`, 8 vCPU, 32GB RAM, 1TB SSD): $1,240<br/>• **Memorystore Redis HA** (2GB Standard): $138<br/>• **Global HTTPS LB + Cloud Armor WAF + Cloud IAP**: $65<br/>• **Cloud Pub/Sub + Secret Manager + Cloud Logging**: $92 | **$1,535** | **$1,535** *(Base)* | **₱89,798** |
| **System 01: Batas-Bayan (LODS)**<br/>*Legislative Operations Digital System* | • **Cloud Run** (Real-time Plenary WebSocket & Bill State Machine, 2 warm instances during session): $75<br/>• **Cloud Storage** (Bills, Committee Reports, House Journals - 500 GB Standard): $12<br/>• **Vertex AI Gemini 2.5 Pro** (Bill version diffing & constitutional checks - 8M tokens): $28 | $640 | **$115** | **₱6,728** |
| **System 02: Housedocs (DMS)**<br/>*Enterprise Document Management* | • **Cloud Run** (Document indexing & search API): $45<br/>• **Cloud Storage** (3 TB Standard + 3 TB Nearline for active documents): $108<br/>• **Gemini 2.5 Flash Multimodal OCR** (40,000 legacy/new pages/mo + pgvector embeddings): $32 | $710 | **$185** | **₱10,823** |
| **System 03: HRep Archives (RMS)**<br/>*Records Management System* | • **Cloud Run** (Retention worker & NAP disposition service): $20<br/>• **Cloud Storage Archive Tier (WORM Locked)** (5 TB historical archives @ $0.0025/GB): $13<br/>• **Cryptographic SHA-256 Audit Verification**: $5 | $450 | **$38** | **₱2,223** |
| **System 04: Kumberso-Sked**<br/>*Shared Calendar & Room Scheduling* | • **Cloud Run** (CalDAV / Google Calendar two-way sync microservice): $25<br/>• **Redis Distributed Locks** (Included in Shared Redis): $0<br/>• **Push/Email Notification Egress**: $10 | $445 | **$35** | **₱2,048** |
| **System 05: e-Request Portal**<br/>*Online Service / Request System* | • **Cloud Run** (Dynamic JSONB form engine & SLA tracker - 2 warm instances): $55<br/>• **Cloud Storage** (Job order photos, contract attachments - 250 GB): $6<br/>• **Vertex AI Gemini 2.5 Flash** (ADK Triage Agent - 15,000 requests/mo): $14 | $580 | **$75** | **₱4,388** |

#### Tier 2: Service Platform Systems

| System # & Name | Primary GCP Resources & Workload Drivers | Standalone Monthly (USD) | UGNAYAN Marginal Monthly (USD) | UGNAYAN Marginal Monthly (PHP) |
| :--- | :--- | :---: | :---: | :---: |
| **System 06: Batasan Pass (VAMS)**<br/>*Visitor / Access Management* | • **Cloud Run** (High-concurrency gate QR validator & pre-registration API): $60<br/>• **Cloud Storage** (Visitor ID/selfie snapshots with 30-day auto-delete DPA rule - 150 GB): $4<br/>• **SMS / Email Pass Dispatch Gateway**: $26 | $595 | **$90** | **₱5,265** |
| **System 07: Lakbay-Kongreso**<br/>*Travel Management System* | • **Cloud Run** (EO 77 / UNDP DSA calculator & e-TA workflow): $35<br/>• **Cloud Storage** (Encrypted DFA passport vault & boarding passes - 200 GB): $5<br/>• **Gemini 2.5 Flash Vision** (Automated COA travel receipt OCR & itemization): $20 | $535 | **$60** | **₱3,510** |
| **System 08: Lingkod-Kawani (DTR)**<br/>*HR / Attendance Management* | • **Cloud Run** (Biometric clock TCP listener, geofence validator & CSC Form 48 PDF generator): $45<br/>• **Cloud Storage** (Monthly signed DTR PDFs & leave attachments - 300 GB): $7 | $510 | **$52** | **₱3,042** |

#### Tier 3: Specialized Department Systems

| System # & Name | Primary GCP Resources & Workload Drivers | Standalone Monthly (USD) | UGNAYAN Marginal Monthly (USD) | UGNAYAN Marginal Monthly (PHP) |
| :--- | :--- | :---: | :---: | :---: |
| **System 09: Target-Kongreso**<br/>*Planning, Monitoring & Evaluation* | • **Cloud Run** (SPMS OPCR/IPCR rating engine & MFO tracker): $25<br/>• **Cloud Storage** (Performance portfolios & MOV uploads - 150 GB): $4 | $435 | **$29** | **₱1,697** |
| **System 10: Asset-Track (PPE)**<br/>*Inventory Management System* | • **Cloud Run** (RFID/Barcode mobile scan API & COA depreciation worker): $30<br/>• **Cloud Storage** (PAR/ICS signed receipts & asset photos - 200 GB): $5 | $440 | **$35** | **₱2,048** |
| **System 11: Kongreso Academy**<br/>*Learning Management System (LMS)* | • **Cloud Run** (SCORM/xAPI runtime & certificate PDF signer): $30<br/>• **Cloud Storage + Cloud CDN** (1 TB HD training videos & courseware egress): $65 | $520 | **$95** | **₱5,558** |

#### Tier 4: Cross-Cutting Intelligence & AI Capabilities

| System # & Name | Primary GCP Resources & Workload Drivers | Standalone Monthly (USD) | UGNAYAN Marginal Monthly (USD) | UGNAYAN Marginal Monthly (PHP) |
| :--- | :--- | :---: | :---: | :---: |
| **System 12: Command Center**<br/>*Executive Live Dashboard* | • **Cloud Run** (WebSocket live telemetry broadcaster for Speaker/SG wallboards): $35<br/>• **Timescale/Postgres Telemetry Partition** (Included in Shared DB): $0 | $460 | **$35** | **₱2,048** |
| **System 13: Lingkod-Dinig AI**<br/>*AI-Assisted Transcription System* | • **Google Cloud Speech-to-Text V2 (Chirp 2 Taglish)**: 300 hrs/mo (18,000 mins @ $0.016/min): **$288**<br/>• **Gemini 2.5 Pro** (Automated Committee Minutes, Action Items & Journal Drafting): **$62**<br/>• **Cloud Run GPU/CPU Audio Diarization & WaveSurfer Editor API**: **$45**<br/>• **Cloud Storage** (1.5 TB raw multi-track audio recordings): **$35** | $920 | **$430** | **₱25,155** |
| **System 14: HRep Insights**<br/>*Reporting & Analytics Platform* | • **BigQuery Data Lakehouse** (1 TB active storage + 6 TB/mo analytical query scans): **$42**<br/>• **Cloud Datastream CDC** (Real-time Postgres-to-BigQuery replication): **$24**<br/>• **Looker Studio Pro / Metabase Container on Cloud Run**: **$20** | $540 | **$86** | **₱5,031** |
| **TOTAL PORTFOLIO (14 SYSTEMS)** | **Complete UGNAYAN Digital Transformation Ecosystem (`asia-southeast1`)** | **$10,850 / mo** | **$2,845 / mo** | **₱166,433 / mo** |

---

### 5. Master Bill of Materials (BOM) — Singapore Region (`asia-southeast1`)

This SKU-level Bill of Materials represents the consolidated **Google Cloud Singapore (`asia-southeast1`)** resources required to run all 14 UGNAYAN systems at full production capacity:

| GCP Service Family | Specific SKU / Configuration (`asia-southeast1`) | Unit Pricing (`asia-southeast1`) | Provisioned Quantity | Monthly On-Demand (USD) | Monthly 1-Yr CUD (USD) | Monthly 1-Yr CUD (PHP) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Cloud SQL for PostgreSQL** | Enterprise Edition, High Availability (Regional Multi-Zone), `db-custom-8-32768` (8 vCPU, 32 GB RAM) | $85.26/vCPU + $14.45/GB RAM | 1 Primary HA Cluster | $1,144.48 | $812.58 | ₱47,536 |
| **Cloud SQL Storage & Backups** | Regional PD-SSD Storage + Automated PITR Backups | $0.34/GB SSD + $0.095/GB Backup | 280 GB SSD + 280 GB Backup | $121.80 | $121.80 | ₱7,125 |
| **Cloud Run (Compute)** | Consolidated Microservices (14 Modules + API Gateway + Workers) | $0.000024/vCPU-s, $0.0000025/GiB-s | ~22M vCPU-sec + 28M GiB-sec | $598.00 | $448.50 | ₱26,237 |
| **Memorystore for Redis** | Standard Tier High Availability (M2 - 2 GB Capacity, Multi-Zone failover) | $0.190 / GB / hour | 2 GB HA Cluster | $138.70 | $110.96 | ₱6,491 |
| **Cloud Storage (Standard)** | Active Hot Storage (Bills, Attachments, DTRs, Audio Masters, Videos) | $0.023 / GB / month | 4,000 GB (4 TB) | $92.00 | $92.00 | ₱5,382 |
| **Cloud Storage (Nearline)** | Infrequently Accessed Committee Files & Prior Session Documents | $0.013 / GB / month | 3,000 GB (3 TB) | $39.00 | $39.00 | ₱2,282 |
| **Cloud Storage (Archive WORM)** | National Archives (NAP) Permanent Historical Records (System 03) | $0.0025 / GB / month | 5,000 GB (5 TB) | $12.50 | $12.50 | ₱731 |
| **Cloud Speech-to-Text V2** | **Chirp 2** Universal Speech Model (Taglish Plenary & Committee Hearings) | $0.016 / minute | 18,000 minutes (300 hours/mo) | $288.00 | $288.00 | ₱16,848 |
| **Vertex AI — Gemini 2.5 Flash** | Multimodal OCR (Receipts/Housedocs), ADK Triage & Taglish Search | $0.15/1M In, $0.60/1M Out | 180M Input + 45M Output Tokens | $54.00 | $54.00 | ₱3,159 |
| **Vertex AI — Gemini 2.5 Pro** | Committee Minutes Synthesis, Bill Legal Diffing & Executive Briefs | $1.25/1M In, $10.00/1M Out | 32M Input + 6M Output Tokens | $100.00 | $100.00 | ₱5,850 |
| **BigQuery & Datastream** | Enterprise Lakehouse Storage (1 TB), Query Scans (6 TB), CDC Stream | $0.023/GB Storage, $6/TB Scan | 1 TB Storage + 6 TB Scans + CDC | $66.00 | $66.00 | ₱3,861 |
| **Networking & Cloud Armor** | Global External HTTPS Load Balancer, Cloud Armor WAF, Cloud CDN Egress | $18 LB base + WAF rules + Egress | 1 Global LB + 500 GB CDN Egress | $98.00 | $98.00 | ₱5,733 |
| **Observability & Security** | Cloud Logging (200 GiB), Cloud Pub/Sub Event Mesh, Secret Manager, IAP | $0.50/GiB Logs (first 50 GiB free) | 200 GiB Logs + 25 Secrets + IAP | $92.52 | $46.66 | ₱2,730 |
| **GRAND TOTAL** | **All 14 UGNAYAN Systems in Google Cloud Singapore (`asia-southeast1`)** | — | — | **$2,845.00** | **$2,290.00** | **₱133,965** |

---

### 6. Phased 24-Month Rollout Budget (Phase 1 to Phase 4)

Because the 14 systems are deployed across four progressive 6-month phases ([00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md](file:///usr/local/google/home/markea/Desktop/hor/00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md)), the House of Representatives **does not need to pay the full $2,845/month on Day 1**. Cloud infrastructure scales proportionally as new systems go live:

```
   Monthly GCP Spend (USD - On-Demand vs 1-Year CUD)
   $3,000 ┼───────────────────────────────────────────────────────────  $2,845 (On-Demand)
   $2,500 ┼───────────────────────────────────────────  $2,210 ───────  $2,290 (1-Yr CUD)
   $2,000 ┼───────────────────────────  $1,680 ───────────────────────
   $1,500 ┼───────────  $1,120 ───────────────────────────────────────
   $1,000 ┼───────────────────────────────────────────────────────────
          └───────────────┴───────────────┴───────────────┴───────────
            Phase 1 (M1-6)  Phase 2 (M7-12) Phase 3 (M13-18) Phase 4 (M19-24)
```

| Implementation Tranche | Active Systems in Production | Database & Compute Sizing | Monthly Cost (USD On-Demand) | Monthly Cost (PHP On-Demand) | 6-Month Tranche Total (PHP) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Phase 1: Quick Wins**<br/>*(Months 1–6)* | • **System 05:** e-Request Portal<br/>• **System 06:** Batasan Pass (VAMS)<br/>• **System 07:** Lakbay-Kongreso Travel<br/>• **System 13:** Lingkod-Dinig AI Transcription | • Cloud SQL `db-custom-4-16384` HA (4 vCPU, 16GB)<br/>• 4 Cloud Run Services + Chirp 2 AI Speech | **$1,120 / mo** | **₱65,520 / mo** | **₱393,120** |
| **Phase 2: Core Platforms**<br/>*(Months 7–12)* | *Phase 1 Systems PLUS:*<br/>• **System 02:** Enterprise DMS (Housedocs)<br/>• **System 04:** Kumberso-Sked Calendar<br/>• **System 11:** Kongreso Academy LMS | • Upgrade DB to `db-custom-6-24576` HA<br/>• Add 4 TB GCS Document & Video Storage | **$1,680 / mo** | **₱98,280 / mo** | **₱589,680** |
| **Phase 3: Operational Suite**<br/>*(Months 13–18)* | *Phase 1 & 2 Systems PLUS:*<br/>• **System 03:** Records Mgmt (RMS/NAP)<br/>• **System 08:** Lingkod-Kawani HR/DTR<br/>• **System 10:** Asset-Track PPE Inventory<br/>• **System 12:** Executive Command Center | • Upgrade DB to `db-custom-8-32768` HA<br/>• Add GCS Archive WORM Tier (5 TB) + Redis HA | **$2,210 / mo** | **₱129,285 / mo** | **₱775,710** |
| **Phase 4: Legislative Core & BI**<br/>*(Months 19–24)* | *All 14 Systems Live:*<br/>• **System 01:** Batas-Bayan Legislative Ops<br/>• **System 09:** Target-Kongreso PM&E<br/>• **System 14:** HRep Insights BigQuery BI | • Full Enterprise Fabric + BigQuery CDC Lakehouse + Plenary WebSocket Clusters | **$2,845 / mo**<br/>*(\$2,290 w/ CUD)* | **₱166,433 / mo**<br/>*(₱133,965 w/ CUD)* | **₱998,598**<br/>*(₱803,790 w/ CUD)* |
| **TOTAL 24-MONTH PROGRAM CLOUD BUDGET** | **Complete 2-Year Digital Transformation Rollout** | — | **Avg: $1,964/mo** | **Avg: ₱114,880/mo** | **₱2,757,108 Total**<br/>*(~₱2.45M with CUDs)* |

---

### 7. HRep FinOps & Cost-Optimization Strategies

To ensure maximum fiscal responsibility and compliance with Commission on Audit (COA) value-for-money guidelines, ICTS will implement five automated FinOps guardrails:

1. **Zero-Infrastructure Day-1 Transcription via Google Workspace (`System 13`):**
   - For hybrid committee hearings hosted on Google Meet, Secretariat staff will activate **Google Meet with Gemini Notes ("Take notes for me")**. This generates automated transcripts and meeting summaries directly into Google Docs at **$0 incremental GCP Speech-to-Text API cost**, reserving paid **Chirp 2 API** minutes strictly for in-person Plenary debates and specialized Taglish audio feeds.
2. **Gemini 2.5 Flash Multimodal Vision over Legacy Document AI (`Systems 02 & 07`):**
   - Traditional OCR/Form Parsers charge $15 to $65 per 1,000 pages. By utilizing **Gemini 2.5 Flash Multimodal Vision** ($0.15 / 1M input tokens), parsing a scanned COA travel receipt or legacy Housedocs memo costs **$0.0004 per page**—delivering a **97% cost reduction** on document digitization.
3. **Session-Aware Cloud Run Scale-to-Zero (`All 14 Systems`):**
   - Congress follows a structured legislative calendar (Plenary sessions Monday–Wednesday afternoons; Committee hearings mornings; Congressional Recesses). Cloud Scheduler will automatically adjust Cloud Run `min_instance_count` from `2` during active session hours to `0` or `1` during nights, weekends, and recess periods—cutting compute billing by **~45%**.
4. **Cloud Storage Autoclass & Statutory WORM Lifecycle (`Systems 02, 03, 06`):**
   - Visitor selfies and gate logs in `Batasan Pass (System 06)` automatically purge after 30 days via GCS Lifecycle rules (enforcing RA 10173 Data Privacy minimization and saving storage costs).
   - Committee recordings and archival bills automatically transition from Standard ($0.023/GB) $\rightarrow$ Nearline ($0.013/GB) after 90 days $\rightarrow$ Archive WORM ($0.0025/GB) after 1 year, cutting long-term storage costs by **89%**.
5. **1-Year / 3-Year Committed Use Discounts (CUDs) on Cloud SQL & Cloud Run:**
   - Once Phase 2 stabilizes, HRep ICTS should lock in a **1-Year Flexible Spend CUD** for Cloud SQL and Cloud Run in `asia-southeast1`, capturing an immediate **28% to 37% statutory discount** without hardware lock-in.

---

### 8. Federated 15-System Architecture BOM (1 Super-App Hub + 14 Standalone Dedicated-Database Systems)

For government procurement scenarios (RA 9184 / DBM ISSP) where the House of Representatives prefers **each of the 14 use-cases to be its own completely independent system** (with its own dedicated Cloud SQL PostgreSQL instance, dedicated Cloud Run microservice, dedicated Cloud Storage bucket, and dedicated AI quota) managed and interconnected by **`SYS-00: UGNAYAN Super-App Hub`**, the complete 15-system Bill of Materials is detailed below.

*(Full granular 67-SKU breakdown exported in [32D_UGNAYAN_FEDERATED_15_SYSTEM_SKU_BOM_SINGAPORE.csv](file:///usr/local/google/home/markea/Desktop/hor/32D_UGNAYAN_FEDERATED_15_SYSTEM_SKU_BOM_SINGAPORE.csv) and summary in [32E_UGNAYAN_FEDERATED_SYSTEMS_SUMMARY.csv](file:///usr/local/google/home/markea/Desktop/hor/32E_UGNAYAN_FEDERATED_SYSTEMS_SUMMARY.csv)).*

| System ID | System Name | Dedicated Compute | Dedicated Database | Dedicated Storage | AI, Cache & Network | Monthly On-Demand (USD) | Monthly 1-Yr CUD (USD) | Monthly 1-Yr CUD (PHP) | Annual 1-Yr CUD (PHP) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`SYS-00`** | **UGNAYAN Super-App Hub** *(Control Plane, IAP SSO, WAF, Universal Action Center, Pub/Sub Mesh)* | $68.00 | $322.40 *(Postgres HA)* | $0.00 | $320.50 *(LB/WAF/Redis HA/PubSub/Gemini)* | **$710.90** | **$585.28** | **₱34,239** | **₱410,867** |
| **`SYS-01`** | **Batas-Bayan (LODS)** *(Legislative Operations & Plenary Real-Time Roll-Call Voting)* | $68.00 | $322.40 *(Postgres HA)* | $11.50 *(500 GB)* | $68.27 *(Redis M1 + Gemini 2.5 Pro)* | **$470.17** | **$365.14** | **₱21,361** | **₱256,328** |
| **`SYS-02`** | **Housedocs (DMS)** *(Enterprise Document Mgmt, OCR & pgvector Semantic Search)* | $45.00 | $344.15 *(Postgres HA + pgvector)* | $108.00 *(3TB Std + 3TB Nearline)* | $18.00 *(Gemini 2.5 Flash OCR)* | **$515.15** | **$423.02** | **₱24,747** | **₱296,960** |
| **`SYS-03`** | **HRep Archives (RMS)** *(Records Mgmt & National Archives WORM Preservation)* | $22.00 | $82.98 *(Postgres Zonal)* | $12.50 *(5 TB Archive WORM)* | $0.00 | **$117.48** | **$91.76** | **₱5,368** | **₱64,416** |
| **`SYS-04`** | **Kumberso-Sked** *(Shared Calendar, Room Reservations & Hearing Conflict Engine)* | $25.00 | $77.68 *(Postgres Zonal)* | $1.15 *(50 GB)* | $0.00 | **$103.83** | **$77.36** | **₱4,526** | **₱54,307** |
| **`SYS-05`** | **HRep e-Request Portal** *(Online Service Requests across 12 Secretariat Offices)* | $55.00 | $313.70 *(Postgres HA)* | $5.75 *(250 GB)* | $6.75 *(Gemini Flash ADK Triage)* | **$381.20** | **$286.57** | **₱16,764** | **₱201,172** |
| **`SYS-06`** | **Batasan Pass (VAMS)** *(Visitor Access Control, Gate Scanners & Emergency Muster)* | $60.00 | $305.00 *(Postgres HA)* | $3.45 *(150 GB w/ 30d DPA purge)* | $26.00 *(SMS/Email Pass Gateway)* | **$394.45** | **$298.57** | **₱17,466** | **₱209,596** |
| **`SYS-07`** | **Lakbay-Kongreso (TMS)** *(Travel Authorities, EO 77 Per Diems & COA Liquidation)* | $38.00 | $161.20 *(Postgres HA)* | $4.60 *(200 GB CMEK Vault)* | $9.30 *(Gemini Flash Receipt OCR)* | **$213.10** | **$163.16** | **₱9,545** | **₱114,538** |
| **`SYS-08`** | **Lingkod-Kawani (DTR)** *(Biometric/Geofenced Attendance & CSC Form 48 Ledger)* | $45.00 | $322.40 *(Postgres HA)* | $6.90 *(300 GB Signed DTRs)* | $0.00 | **$374.30** | **$282.17** | **₱16,507** | **₱198,083** |
| **`SYS-09`** | **Target-Kongreso (SPMS)** *(Planning, M&E, OPCR/IPCR Ratings & MFO Tracking)* | $25.00 | $80.33 *(Postgres Zonal)* | $3.45 *(150 GB MOVs)* | $0.00 | **$108.78** | **$82.31** | **₱4,815** | **₱57,782** |
| **`SYS-10`** | **Asset-Track (PPE)** *(Property, Plant & Equipment, RFID Scans & Depreciation)* | $30.00 | $82.98 *(Postgres Zonal)* | $4.60 *(200 GB PAR/ICS)* | $0.00 | **$117.58** | **$89.86** | **₱5,257** | **₱63,082** |
| **`SYS-11`** | **Kongreso Academy (LMS)** *(Staff Capacity Building & Video Streaming Courseware)* | $30.00 | $80.33 *(Postgres Zonal)* | $65.00 *(1 TB Video + Cloud CDN)* | $0.00 | **$175.33** | **$147.61** | **₱8,635** | **₱103,622** |
| **`SYS-12`** | **Command Center** *(Speaker & SecGen Live Complex Telemetry Wallboard)* | $35.00 | $82.98 *(Postgres Zonal)* | $0.00 | $35.77 *(Dedicated Redis M1 Stream)* | **$153.75** | **$117.63** | **₱6,881** | **₱82,576** |
| **`SYS-13`** | **Lingkod-Dinig AI** *(Plenary & Committee Taglish Transcription & Minutes Synthesis)* | $45.00 | $174.25 *(Postgres HA)* | $34.50 *(1.5 TB Audio Masters)* | $355.50 *(Chirp 2 STT $288 + Gemini Pro)* | **$609.25** | **$557.56** | **₱32,617** | **₱391,407** |
| **`SYS-14`** | **HRep Insights (BI)** *(BigQuery Enterprise Lakehouse & Cross-System CDC Analytics)* | $25.00 | $0.00 *(Serverless BigQuery)* | $23.00 *(1 TB BigQuery Marts)* | $81.00 *(6 TB Query Scans + Datastream CDC)* | **$129.00** | **$122.75** | **₱7,181** | **₱86,171** |
| **TOTAL** | **15 Federated Systems (1 Super-App Control Plane + 14 Dedicated Systems)** | **$616.00** | **$3,052.53** | **$284.45** | **$921.09** | **$4,574.27 / mo** | **$3,690.75 / mo** | **₱215,909 / mo** | **₱2,590,907 / yr** |

