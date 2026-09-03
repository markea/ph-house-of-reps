# ❓ Frequently Asked Questions (FAQ)
## HRep Secretariat Digital Transformation Program (UGNAYAN)

This document collates commonly asked questions regarding the technical architecture, security posture, authentication framework, deployment strategies, and AI capabilities across the **House of Representatives (HRep)** digital transformation deliverables.

---

## 📑 Table of Contents
1. [Cloud Identity, Authentication & IAP](#1-cloud-identity-authentication--iap)
2. [Local Testing vs. Cloud Production](#2-local-testing-vs-cloud-production)
3. [Security, Integrity & RA 10173 Compliance](#3-security-integrity--ra-10173-compliance)
4. [ADK AI Agent & Quality Evaluation](#4-adk-ai-agent--quality-evaluation)
5. [Statutory Compliance & SLA Enforcement (RA 11032)](#5-statutory-compliance--sla-enforcement-ra-11032)
6. [Git Repository & Version Rollback](#6-git-repository--version-rollback)

---

## 1. Cloud Identity, Authentication & IAP

### Q1.1: If we deploy with Google Identity-Aware Proxy (IAP), does it inherit the GCP / Google Workspace identities of our users?
**Yes, completely.** 
* When Congressional staff access the application URL, Google IAP intercepts the traffic and prompts them to authenticate using their official `@hrep.gov.ph` Google Workspace / Cloud Identity account.
* Once authenticated and authorized via GCP IAM, IAP generates a cryptographically signed JSON Web Token (`X-Goog-IAP-JWT-Assertion`).
* The application backend automatically extracts their verified email, name, and department. 

### Q1.2: Do users need to register or remember separate passwords in the application?
**No.** The application maintains a Zero-Password model:
* No passwords or credential hashes are stored in the application database.
* This eliminates password management overhead and neutralizes the risk of password data leaks.

### Q1.3: What if staff already use Microsoft Azure AD / Windows Active Directory?
Google Cloud Identity supports **SAML 2.0 and OpenID Connect Federation**. HRep IT can federate Google Cloud Identity with Microsoft Azure AD / Active Directory. Staff will automatically log into the e-Request portal using their existing single sign-on (SSO) credentials without needing a new account.

### Q1.4: What happens when an employee or congressional staff member leaves the House?
Access revocation is **instant and centralized**:
* When HRep IT disables or suspends the employee's `@hrep.gov.ph` account in Google Workspace / Active Directory, their access to the e-Request Portal is severed immediately across all devices with zero manual database administration.

---

## 2. Local Testing vs. Cloud Production

### Q2.1: Can I still run and test the application locally without any cloud credentials?
**Yes, 100%.** 
* The codebase uses an automated dual-mode execution strategy driven by the `APP_ENV` environment variable (`local` vs. `production`).
* By default (`APP_ENV=local`), the app boots up on `localhost:8080` with zero external dependencies, using an embedded SQLite database, a mock staff user, local file uploads (`./uploads`), and a lightning-fast heuristic AI assistant.

### Q2.2: How does the application switch between Local and Google Cloud environments?
Through environment configuration:
* **Localhost (`APP_ENV=local`):** Uses SQLite / local Docker Postgres, local disk storage, and mock authentication.
* **Production (`APP_ENV=production`):** Connects to Cloud SQL for PostgreSQL (via connection pooling), streams files to Google Cloud Storage (GCS) with signed URLs, and enforces cryptographic IAP JWT verification.

---

## 3. Security, Integrity & RA 10173 Compliance

### Q3.1: Are there any backdoors, hidden accounts, or telemetry phone-home calls in the codebase?
**No, absolutely not.**
* The codebase is open, transparent, and version-tracked in Git.
* There are no hardcoded master passwords, hidden admin bypasses, or external telemetry tracking calls.
* All database queries use parameterized ORM statements to prevent SQL injection, and file uploads are restricted by whitelist (`.pdf`, `.docx`, `.png`, etc.) and renamed with randomized UUIDs to prevent directory traversal attacks.

### Q3.2: How does the system comply with the Philippine Data Privacy Act of 2012 (RA 10173)?
* **Data Encryption:** All sensitive personal information (PII) is encrypted at rest using AES-256 and in transit via TLS 1.3.
* **Access Control:** Role-Based Access Control (RBAC) ensures only assigned approvers, dispatchers, and requesters see ticket details.
* **Data Retention Schedules:** Cloud Storage lifecycle rules automatically purge old attachments in accordance with Commission on Audit (COA) / National Archives of the Philippines (NAP) retention limits (3 years).

---

## 4. ADK AI Agent & Quality Evaluation

### Q4.1: What is the ADK Framework and what does the AI Agent do?
The **Agent Development Kit (ADK)** is Google's framework for building intelligent, tool-using AI agents. 
* In the e-Request Portal, the **HRep Service Triage Agent** allows staff to describe their problem in plain conversational language (e.g., *"I need an official van for 4 staff to go to the Senate tomorrow at 9 AM"*).
* The agent automatically classifies the intent into the correct Core 5 service (Motor Pool, EPFD, ICTS, OSAA, LAD), extracts structured parameters (Destination, Passenger Count, Room Number), and pre-populates the dynamic form.

### Q4.2: Does the AI Agent understand Taglish / Filipino phrasing?
**Yes.** The agent is tuned to recognize common conversational Taglish terms used in legislative offices (e.g., *"Pahiram po ng van"*, *"Bumubuga ng init yung aircon sa South Wing"*, *"Paki-ayos po ng printer"*).

### Q4.3: How do we evaluate the quality and accuracy of the AI Agent?
The application includes a built-in **Agent Quality & Eval Flywheel Benchmark Suite**:
* **CLI Benchmark Runner:** Run `PYTHONPATH=. python eval/eval_agent.py` to evaluate the agent against a 14-scenario ground-truth test dataset.
* **Web UI Dashboard:** Navigate to the **"Agent Quality & Eval Flywheel"** tab at [http://localhost:8080](http://localhost:8080) to inspect real-time metrics (100% Intent Accuracy, 100% Entity Recall, <1ms latency).

---

## 5. Statutory Compliance & SLA Enforcement (RA 11032)

### Q5.1: How does the system enforce Republic Act No. 11032 (Ease of Doing Business)?
* Every service catalog item has a predefined statutory SLA based on working hours (Monday–Thursday 7:00 AM–6:00 PM, excluding holidays).
* The portal displays live countdown timers, issues automated escalation warnings at 75% elapsed SLA, and triggers statutory auto-advancement at 100% threshold pursuant to RA 11032 Section 10.

### Q5.2: How do digital approvals and executive sign-offs work?
* Approvers must log in with their authenticated credentials to review requisitions.
* Executing an approval generates an immutable cryptographic SHA-256 digital stamp (`SHA256-AUTHENTICATED-APPROVER-NAME-TIMESTAMP`) attached to the audit trail for non-repudiation during internal and COA audits.

---

## 6. Git Repository & Version Rollback

### Q6.1: Where is the complete project code and documentation stored?
The repository is hosted privately on GitHub:
🔗 **[https://github.com/markea/ph-house-of-reps](https://github.com/markea/ph-house-of-reps)**

### Q6.2: Can we roll back or revert changes if needed?
**Yes, instantly.** Every milestone is committed to Git with clear commit messages. You can revert any specific commit or reset the entire codebase back to any previous state using standard Git commands (`git revert` or `git reset --hard`).

---

## 7. Antigravity Slash Commands & Agentic Lifecycle Guide

### Q7.1: What are Antigravity slash commands and how do they accelerate project delivery?
Antigravity slash commands are specialized shortcuts in the chat interface that trigger specialized agent behaviors, interactive interview modes, structured planning artifacts, or multi-agent collaboration across the solution lifecycle:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           ANTIGRAVITY AGENTIC WORKFLOW LIFECYCLE                                │
├──────────────────────────────┬──────────────────────────────────────────────────────────────────┤
│ Slash Command                │ Lifecycle Stage & Purpose                                        │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 🎯 `/goal`                   │ **Ideation & Autonomous Execution:** Runs deep, long-running     │
│                              │ tasks (e.g. overnight) and ensures the agent is extra thorough   │
│                              │ until the objective is fully achieved without stopping early.    │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 🎙️ `/grill-me`               │ **Requirements Alignment & Interview:** Proactively interviews  │
│                              │ the user through an interactive question tree to resolve design  │
│                              │ decisions, statutory trade-offs, and user preferences.           │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 📋 `/plan`                   │ **Technical Planning & Safety Gate:** Researches the codebase    │
│                              │ and creates an implementation plan artifact for user review      │
│                              │ before touching any code or making modifications.                │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 🦉 `/owl`                    │ **Deep Reasoning & Multi-Perspective Architecture:** Engages in │
│                              │ rigorous analysis, evaluating edge cases, security postures,     │
│                              │ and alternative technical strategies for complex projects.       │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 🌐 `/browser`                │ **Live Web Research & Investigation:** Navigates live web pages, │
│                              │ parses online statutory circulars, documentation, or portals.    │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 👥 `/teamwork-preview`       │ **Multi-Agent Orchestration:** Deploys a coordinated team of     │
│                              │ autonomous subagents working simultaneously across tasks.        │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ ⏰ `/schedule`               │ **Continuous Automation & Cron:** Schedules recurring background │
│                              │ checks or one-time timers to monitor deployments or builds.      │
├──────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ 🧠 `/learn`                  │ **Knowledge Persistence:** Records user preferences, project     │
│                              │ setup nuances, or corrections so the agent retains them forever. │
└──────────────────────────────┴──────────────────────────────────────────────────────────────────┘
```

### Q7.2: What is the recommended sequence of slash commands for a new system?
1. **Explore & Define:** Use `/goal` or `/owl` to synthesize high-level institutional requirements.
2. **Align on Decisions:** Use `/grill-me` to lock in key operational, security, and statutory choices.
3. **Plan Safely:** Use `/plan` to review codebase gaps and draft an implementation artifact.
4. **Research Standards:** Use `/browser` to look up relevant COA circulars, DICT guidelines, or API docs.
5. **Continuous Quality:** Use `/learn` and `/schedule` to retain custom workflows and monitor health.

