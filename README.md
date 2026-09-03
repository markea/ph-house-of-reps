# UGNAYAN: HREP SECRETARIAT DIGITAL TRANSFORMATION PROGRAM
## Technical Advisory & Requirements Architecture Workspace

**Client:** House of Representatives of the Philippines (HRep) Secretariat  
**Program:** UGNAYAN Digital Transformation Program  
**Prepared by:** Technical Consulting & Solutions Architecture Team  
**Date:** September 2026  
**Workspace Path:** `/usr/local/google/home/markea/Desktop/hor`  

---

### Executive Overview

This workspace contains the complete technical analysis, prioritization framework, and formal **Business Requirements Documents (BRDs)** developed for the **House of Representatives (HRep) Secretariat** under the **UGNAYAN Digital Transformation Program**.

The HRep Secretariat provides essential administrative, legal, technical, and operational machinery for the 315+ Members of the Philippine House of Representatives. Currently, operations are constrained by fragmented legacy tools (e.g., custom *Housedocs*, on-premise *Globodox*, disparate Google Drives, and physical paper folders), manual multi-office routing slips, heavy legislative transcription backlogs, travel clearance/liquidation bottlenecks, and physical perimeter access queues at the Batasan Pambansa complex.

This deliverables package synthesizes the **14 Common Systems**, evaluates their interdependencies, prioritizes all 14 systems in a multi-factor decision matrix, and delivers production-ready enterprise BRDs for the highest-value systems.

#### Strategic Architecture Insight: Leveraging Google Workspace for Quick-Win AI Transcription
A pivotal insight in this roadmap is that **System 13 (AI-Assisted Transcription)** does not require building an expensive custom deep-learning pipeline from day one for hybrid committee hearings. Instead, HRep can achieve an **immediate, zero-code quick win** by utilizing **Google Meet with Gemini Notes ("Take notes for me")** in Google Workspace. This delivers instant automated transcription, speaker notes, attendee lists, and action items directly into Google Docs.

By solving committee transcription immediately with Google Workspace, HRep can focus custom software development resources on three transformative administrative and security platforms:
1. **System 05: HRep e-Request Portal** (Eliminating paper routing slips across 12 offices)
2. **System 07: Lakbay-Kongreso Travel Management System** (Automating EO 77 per diems, resolving COA liquidation liabilities, and tracking diplomatic passports)
3. **System 06: Batasan Pass / VAMS** (Modernizing physical gate access and real-time emergency headcount)

---

### Workspace Deliverables Directory

| File Name | Document Title | Description & Scope |
| :--- | :--- | :--- |
| [00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md](file:///usr/local/google/home/markea/Desktop/hor/00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md) | **Strategic Assessment & Master Prioritization Matrix** | Institutional landscape analysis (15 offices), deconstruction of all 14 systems, mathematical prioritization scoring, 24-month phased roadmap, inter-office linkage architecture, and GAD compliance. |
| [01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md) | **BRD: HRep e-Request Portal (System 05)** | Full enterprise BRD for the unified administrative service catalog. Eliminates paper routing slips across 12 offices for motor pool, ICT loans, ID issuance, building maintenance, and contract reviews. |
| [02_BRD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/02_BRD_AI_ASSISTED_TRANSCRIPTION_SYSTEM.md) | **BRD: Lingkod-Dinig AI Transcription (System 13)** | Full enterprise BRD for specialized plenary and committee transcription, Taglish code-switching, stenographer audio-synced editor, and air-gapped Executive Session processing (augmented by Google Meet Gemini Notes). |
| [03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md) | **BRD: Batasan Pass / VAMS (System 06)** | Full enterprise BRD for digital perimeter security. Features guest pre-registration, sponsor endorsements, rotating dynamic QR-code credentials, handheld gate scanners, and real-time emergency headcount muster. |
| [04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md) | **BRD: Lakbay-Kongreso Travel Management System (System 07)** | Full enterprise BRD for official local and foreign travel: automated EO 77 & UNDP per diem calculator, online Travel Authorities, DFA diplomatic passport vault, mobile receipt/boarding pass COA liquidation, and IPAD bilateral archives. |
| [05_TDD_ONLINE_SERVICE_REQUEST_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/05_TDD_ONLINE_SERVICE_REQUEST_SYSTEM.md) | **Technical Design Document (TDD): HRep e-Request Portal** | Comprehensive technical architecture document detailing dual-mode execution (Localhost vs. Google Cloud Production), PostgreSQL JSONB dynamic schema, Zero-Trust IAP security, and ADK AI Agent design. |
| [06_PRODUCTION_DEPLOYMENT_PLAN_E_REQUESTS.md](file:///usr/local/google/home/markea/Desktop/hor/06_PRODUCTION_DEPLOYMENT_PLAN_E_REQUESTS.md) | **Production Deployment & Remediation Plan** | Production hardening plan covering Cloud Run concurrency, Cloud SQL pooling, cryptographic IAP token verification, Alembic migrations, and Terraform IaC manifests. |
| [07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md](file:///usr/local/google/home/markea/Desktop/hor/07_FAQ_FREQUENTLY_ASKED_QUESTIONS.md) | **Frequently Asked Questions (FAQ)** | Comprehensive FAQ covering Google IAP identity inheritance, local/cloud toggles, RA 10173 data privacy compliance, ADK AI evaluation, and Git rollback safety. |
| [e-requests/](file:///usr/local/google/home/markea/Desktop/hor/e-requests/) | **Full-Stack e-Request Application & ADK Eval Suite** | Working Python/FastAPI application with dynamic JSON-Schema form builder, live SLA tracking, cryptographic digital signing, ADK AI Triage Agent, benchmark evaluation suite, and Terraform scripts. |
| [README.md](file:///usr/local/google/home/markea/Desktop/hor/README.md) | **Master Workspace Index & Executive Briefing** | Navigation hub, executive summary, ranking comparison table, and recommended immediate next steps for the HRep IT steering committee. |

---

### Summary of the High-Value Phase 1 Systems

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             HIGH-VALUE PHASE 1 SYSTEMS                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. HRep e-Request Portal (System 05 | Tier 1: Foundational Systems)                     │
│    • Target Problem: Paper routing slips, lost forms, desk delays across 12 offices.    │
│    • Solution: Unified digital catalog, multi-tier digital workflows, SLA tracking.     │
│    • Implementation: 8-10 Weeks to Production MVP.                                      │
│    • Strategic Value: Immediate daily relief for 3,000+ staff and 315+ Member offices.  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. Lakbay-Kongreso Travel Management System (System 07 | Tier 2: Service Platform)      │
│    • Target Problem: Multi-office paper TA routing, error-prone EO 77 per diem math,    │
│      unliquidated cash advances causing COA Audit Observation Memoranda (AOMs).         │
│    • Solution: Digital Travel Authorities, automated EO 77/UNDP per diem calculator,    │
│      DFA diplomatic passport tracking, and mobile boarding pass/receipt COA liquidation.│
│    • Implementation: 8-10 Weeks to Production MVP.                                      │
│    • Strategic Value: Massive financial governance win, protects lawmakers and finance. │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. Batasan Pass / VAMS (System 06 | Tier 2: Service Platform Systems)                   │
│    • Target Problem: Long gate lines, manual logbooks, zero emergency headcount.        │
│    • Solution: Web pre-registration, rotating QR-passes, gate scanners, muster report. │
│    • Implementation: 8-10 Weeks to Production MVP.                                      │
│    • Strategic Value: Sub-3s gate ingress, OSAA watchlist enforcement, modern welcome. │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ *  Google Workspace Gemini Notes Fast-Track (System 13 Augmentation)                    │
│    • Immediate COTS Quick Win: Enable Google Meet with Gemini Notes for all hybrid      │
│      committee hearings, generating instant notes and transcripts with ZERO code dev!   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Comprehensive Ranking of All 14 Systems

Every system in the UGNAYAN program has been scored using a weighted multi-factor decision model ($30\%$ Value/Impact, $25\%$ Feasibility/Speed, $20\%$ Independence/Low Dependencies, $15\%$ Tech/AI Demonstration, $10\%$ Ease of Change Management):

```
Rank  Score  System Name & Code                                    Deployment Phase
────  ─────  ──────────────────────────────────────────────────  ───────────────────────────
 01   4.74   System 13: AI-Assisted Transcription (Lingkod-Dinig) Phase 1 (Google Meet COTS + Bespoke)
 02   4.64   System 05: Online Service / Request Portal (e-Request)Phase 1: Quick Wins (M1-M3)
 03   4.58   System 06: Visitor / Access Management (Batasan Pass) Phase 1: Quick Wins (M1-M3)
 04   4.57   System 07: Travel Management System (Lakbay-Kongreso) Phase 1: High-Value (M1-M3)
 05   4.21   System 04: Shared Calendar & Scheduling              Phase 2: Core Platforms (M3-M6)
 06   4.13   System 11: Learning Management System (LMS)          Phase 2: Core Platforms (M3-M6)
 07   3.86   System 02: Document Management System (DMS)          Phase 2: Core Platforms (M4-M9)
 08   3.70   System 08: HR / Attendance Management (DTR)          Phase 3: Operations (M7-M12)
 09   3.67   System 12: Live Dashboard / Monitoring               Phase 3: Operations (M9-M14)
 10   3.61   System 10: Inventory Management System (PPE)         Phase 3: Operations (M8-M13)
 11   3.56   System 14: Reporting & Analytics                     Phase 4: Legislative & BI (M14-M24)
 12   3.48   System 03: Records Management System (RMS)           Phase 3: Operations (M8-M14)
 13   3.36   System 01: Legislative Operations Digital System     Phase 4: Legislative & BI (M12-M24)
 14   3.33   System 09: Planning, Monitoring & Evaluation (M&E)   Phase 4: Legislative & BI (M12-M18)
```

*(Detailed scoring rationale and criteria breakdowns are documented in [00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md](file:///usr/local/google/home/markea/Desktop/hor/00_UGNAYAN_EXECUTIVE_SUMMARY_AND_PRIORITIZATION_MATRIX.md)).*

---

### Institutional Alignment & Statutory Compliance

All specifications in this repository comply with national laws and civil service regulations governing Philippine public administration:
1. **Executive Order No. 77 (s. 2019):** Strict statutory rates and rules for official local Daily Travel Allowances (DTA Clusters I, II, III) and foreign Daily Subsistence Allowances (UNDP DSA).
2. **COA Circular No. 2012-001 & Circular No. 2023-004:** Mandatory 30-day (local) and 60-day (foreign) liquidation enforcement, automated liquidation packets, and prevention of duplicate cash advances.
3. **Republic Act No. 10173 (Data Privacy Act of 2012):** Strict data minimization, TLS 1.3/AES-256 encryption, role-based access, and automated 30-day log purging for visitor records.
4. **Republic Act No. 11032 (Ease of Doing Business Act):** Enforced statutory SLAs (3-day simple, 7-day complex) with automated escalation triggers in service and travel workflows.
5. **Republic Act No. 9710 (Magna Carta of Women) & GAD Standards:** Sex-disaggregated metrics tracking, accessible facilities/transport booking, and gender-inclusive forms.
6. **Batas Pambansa Blg. 344 & WCAG 2.1 AA:** Full accessibility compliance for wheelchair users at self-service kiosks and screen-reader compatibility for digital web forms.

---

### Recommended Immediate Actions for HRep IT Leadership

1. **Enable Google Meet with Gemini Notes in Google Workspace:** Provide immediate training to Committee Affairs (CAD) committee secretaries to enable "Take notes for me" in Google Meet for hybrid hearings, eliminating the hearing transcription backlog instantly.
2. **Convene Stakeholder Walkthroughs for the Triad of Custom Systems:**
   - Meet with **ADMIN & EPFD** on the e-Request Service Catalog ([01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/01_BRD_ONLINE_SERVICE_REQUEST_SYSTEM.md)).
   - Meet with **OSAA** on Batasan Pass perimeter scanners and kiosks ([03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/03_BRD_VISITOR_ACCESS_MANAGEMENT_SYSTEM.md)).
   - Meet with **FINANCE, IPAD, and COA** on Lakbay-Kongreso travel clearances and liquidations ([04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md](file:///usr/local/google/home/markea/Desktop/hor/04_BRD_TRAVEL_MANAGEMENT_SYSTEM.md)).
3. **Stand Up Shared Architecture Infrastructure:** Deploy the unified Keycloak SSO (integrated with HRep Active Directory) and Kong API Gateway to serve as the secure foundation for all three systems.
