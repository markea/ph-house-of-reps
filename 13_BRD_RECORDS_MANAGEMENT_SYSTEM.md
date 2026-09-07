# Business Requirements Document (BRD)
## System 03: Records Management System (RMS / HRep Archives & Retention)
### UGNAYAN Super App - Institutional Archival Module

**Document Reference:** HREP-UGNAYAN-BRD-2026-013  
**Target Organization:** House of Representatives of the Philippines (HRep) Secretariat  
**Primary Department Owners:** Legislative Information Resources Management Dept. (LIRMD), Archives and Records Management Section, Office of the Secretary General  
**Date:** September 2026  
**Status:** Approved for Core Engineering  

---

### 1. Executive Summary & Statutory Problem

The **Records Management System (RMS / HRep Archives)** is responsible for the formal legal custody, declassification, retention scheduling, and transfer of historical Congressional records to the **National Archives of the Philippines (NAP)** pursuant to **Republic Act No. 9470 (National Archives of the Philippines Act of 2007)** and **COA Circular 2012-001**.

#### Current Pain Points:
1. **Deteriorating Physical Archives:** Bound volumes of historical legislative journals, original handwritten committee minutes, and enrolled bills from previous Congresses face environmental deterioration in physical vaults.
2. **Manual Disposition & Disposal Authorizations:** Periodic disposal of non-current administrative records requires tedious paper inventories submitted to NAP and COA.
3. **Declassification Bottlenecks:** Executive session records and confidential committee testimonies lack a structured, audit-logged workflow for statutory 25-year or 50-year declassification reviews.

---

### 2. User Personas & Stakeholder Matrix

| Persona Code | Role & Title | Department | Core Responsibility & Needs |
| :--- | :--- | :--- | :--- |
| **PER-RMS-01** | Chief Archivist | LIRMD / Archives Section | Manages accessioning, preservation metadata (Dublin Core / EAD), physical box/shelf location tracking, and NAP disposition approvals. |
| **PER-RMS-02** | Committee Records Custodian | Committee Affairs (CAD) | Transfers closed committee records at the end of each 3-year Congress to the central institutional archives. |
| **PER-RMS-03** | Legal & Parliamentary Historian | CPBRD / Research Staff | Searches declassified transcripts, historical treaties, and landmark Republic Act debates across all Philippine Congresses (1st to 20th Congress). |

---

### 3. Core Functional Requirements

```mermaid
flowchart LR
    A[Active Documents DMS] -->|Congress Adjournment Sine Die| B[Archival Transfer & Accessioning]
    B --> C[NAP Retention Schedule Rule Engine]
    C --> D[Physical Vault Shelf / Box Locator & Digital Vault]
    D --> E[Declassification Review Workflow]
    E --> F[Public Historical Archive & NAP Transfer]
```

#### FR-RMS-01: Congress Sine Die Archival Transfer Engine
- **Description:** Automated bulk accessioning of all bills, committee reports, audio transcripts, and resolutions upon the official adjournment *Sine Die* of each Congress.
- **Rules:** Generates Archival Transfer Manifests with cryptographic SHA-256 integrity checksums ensuring no records have been altered post-adjournment.

#### FR-RMS-02: NAP-Compliant Records Disposition Schedule (RDS)
- **Description:** Pre-configured retention schedules for all government record classes:
  - *Permanent:* Enrolled Bills, Republic Acts, Plenary Journals, Treaties.
  - *10 Years:* General Vouchers, Audit Observations, Travel Authorities.
  - *5 Years:* Routine visitor logs, internal memoranda, gate passes.
- **Rules:** Automated notification to Chief Archivist when records reach maturity for disposal, generating the official NAP Form 1 (Request for Authority to Dispose Records).

#### FR-RMS-03: Declassification Review & Freedom of Information (FOI) Vault
- **Description:** Workflow for declassifying executive session records upon petition or statutory time lapse.
- **Rules:** Requires dual authorization by the Secretary General and Committee Chairperson before converting restricted records to public search index.
