# 🏛️ HRep e-Request Portal (System 05)

The **HRep e-Request Portal** is an enterprise-grade digital requisition and workflow management system built for the **House of Representatives of the Philippines (HRep)** under the **UGNAYAN Secretariat Digital Transformation Program**.

It digitalizes the "Core 5" administrative services across the Batasan Complex, eliminating physical paper routing, enforcing statutory turnaround times under Republic Act No. 11032 (Ease of Doing Business), and providing intelligent request triage through an **Agent Development Kit (ADK)** AI assistant.

---

## 🌟 Key Features

1. **"Core 5" Service Catalog:**
   - 🚐 **ADMIN:** Motor Pool Official Vehicle & Driver Dispatch
   - ❄️ **EPFD:** Building & Air-Conditioning Maintenance Job Orders
   - 💻 **ICTS:** ICT Equipment Loans & Technical Support
   - 🪪 **OSAA:** Official ID Badge Issuance & Replacement
   - ⚖️ **LAD:** Legal Contract & Agreement Review
2. **Dynamic JSON-Schema Form Engine:** Form fields and validation rules are rendered dynamically from PostgreSQL `JSONB` schemas, allowing non-developers to extend forms without database migrations.
3. **Executive Approval Workbench:** Directors and Chiefs of Staff can review and digitally sign tickets with an immutable cryptographic timestamped audit stamp (`SHA-256`).
4. **ADK AI Service Triage Agent:** Congressional staff can type plain English/Taglish descriptions (e.g. *"I need a van for 4 people to the Senate tomorrow"*), and the ADK Agent classifies the category, extracts entities, and pre-fills the requisition form.
5. **Dual-Mode Environment Toggle:** Automatically defaults to a zero-configuration localhost environment with mock authentication and seeded data, and seamlessly switches to Google Cloud production (IAP + Cloud Run + Cloud SQL) via environment variables.

---

## 🏗️ High-Level Architecture

```
                      +-------------------------------------------------+
                      |              GOOGLE CLOUD PRODUCTION            |
                      |                                                 |
                      |  +-------------------------------------------+  |
                      |  |   Google Identity-Aware Proxy (IAP)       |  |
                      |  |   (HRep Single Sign-On / Zero Trust)      |  |
                      |  +---------------------+---------------------+  |
                      |                        |                        |
                      |                        v                        |
                      |  +-------------------------------------------+  |
                      |  |   Google Cloud Run                        |  |
                      |  |   (FastAPI Backend + Modern Frontend)     |  |
                      |  +----+------------------+-----------------+--+  |
                      |       |                  |                 |    |
                      |       v                  v                 v    |
                      |  +---------+      +-------------+   +---------+ |
                      |  |Cloud SQL|      |Cloud Storage|   | ADK AI  | |
                      |  |(Postgres|      | (Encrypted  |   | Agent   | |
                      |  |  JSONB) |      | Attachments)|   | Platform| |
                      |  +---------+      +-------------+   +---------+ |
                      +-------------------------------------------------+
                                               ▲
                             SAME CODEBASE     │  APP_ENV=production
                           --------------------+----------------------
                             APP_ENV=local     │
                                               ▼
                      +-------------------------------------------------+
                      |             LOCAL TESTING (LOCALHOST)           |
                      |                                                 |
                      |  +-------------------------------------------+  |
                      |  |  FastAPI App (localhost:8080)             |  |
                      |  |  • Mock Auth Middleware (Auto-Login)      |  |
                      |  |  • Local SQLite / Docker PostgreSQL       |  |
                      |  |  • Local Volume Attachments (./uploads)   |  |
                      |  |  • ADK Heuristic Rule Engine (Zero-Config)|  |
                      |  +-------------------------------------------+  |
                      +-------------------------------------------------+
```

---

## 🚀 Quickstart: Running on Localhost

The system is designed to run locally with zero cloud dependencies. It automatically creates the SQLite database and seeds the "Core 5" catalogs, sample tickets, and test users on first launch.

### Option A: Python Virtual Environment (Instant Run)

1. **Navigate to the directory:**
   ```bash
   cd /usr/local/google/home/markea/Desktop/hor/e-requests
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application:**
   ```bash
   python -m app.main
   ```

5. **Open your browser:**
   Navigate to [http://localhost:8080](http://localhost:8080) to interact with the portal, submit requests, approve tickets, and test the ADK AI Agent!

---

### Option B: Local Multi-Container Docker Compose

To test with a local PostgreSQL 15 database matching production behavior:

```bash
cd /usr/local/google/home/markea/Desktop/hor/e-requests
docker-compose up --build
```

Access the portal at [http://localhost:8080](http://localhost:8080).

---

## ☁️ Deploying to Google Cloud (Production)

### Prerequisites
- Google Cloud SDK (`gcloud`) installed and authenticated.
- A GCP project with Cloud Run, Cloud SQL, Secret Manager, and IAP APIs enabled.

### 1. Build and Push Container to Artifact Registry
```bash
# Set your GCP Project ID
export PROJECT_ID="your-hrep-gcp-project-id"
export REGION="asia-southeast1" # Manila / Singapore

# Create Artifact Registry Repository (if not existing)
gcloud artifacts repositories create hrep-repo \
    --repository-format=docker \
    --location=$REGION

# Build and push the image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/hrep-repo/erequests-app:latest .
```

### 2. Deploy Cloud SQL for PostgreSQL
```bash
gcloud sql instances create hrep-erequests-db \
    --database-version=POSTGRES_15 \
    --cpu=2 \
    --memory=7680MB \
    --region=$REGION \
    --availability-type=REGIONAL
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy hrep-erequests-service \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/hrep-repo/erequests-app:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars="APP_ENV=production,AUTH_MODE=iap,STORAGE_TYPE=gcs,GCS_BUCKET_NAME=hrep-erequests-attachments" \
    --add-cloudsql-instances=$PROJECT_ID:$REGION:hrep-erequests-db
```

### 4. Enable Identity-Aware Proxy (IAP) for Zero Trust
1. In the Google Cloud Console, navigate to **Security** > **Identity-Aware Proxy**.
2. Configure the OAuth Consent Screen with your HRep Google Workspace domain (`hrep.gov.ph`).
3. Add backend routing to the Cloud Run service, granting the `IAP-secured Web App User` role to authorized Congressional staff and personnel groups.

---

## 📁 Repository Structure

```
e-requests/
├── Dockerfile                  # Container definition for Cloud Run
├── docker-compose.yml          # Local multi-container development stack
├── requirements.txt            # Python dependencies (FastAPI, SQLAlchemy, etc.)
├── .env.example                # Configuration template
├── README.md                   # System documentation & deployment guide
└── app/
    ├── __init__.py
    ├── main.py                 # FastAPI entrypoint & router assembly
    ├── config.py               # Environment configuration (Local vs Prod)
    ├── database.py             # SQLAlchemy session & engine manager
    ├── models.py               # Database ORM models (JSONB support)
    ├── schemas.py              # Pydantic data schemas
    ├── seed_data.py            # Localhost auto-seeder for Core 5 services
    ├── agent/
    │   ├── __init__.py
    │   └── triage_agent.py     # ADK-compliant AI Service Triage Agent
    ├── routers/
    │   ├── __init__.py
    │   ├── auth.py             # Auth router (Mock for local, IAP for prod)
    │   ├── services.py         # Service catalog & JSON schema endpoints
    │   ├── requests.py         # Request submission, approval & CSAT endpoints
    │   └── agent.py            # AI Triage conversational API
    └── static/
        ├── index.html          # Responsive Web UI (Tailwind CSS)
        └── app.js              # Dynamic JSON Schema form renderer & state
```

---

## 🔒 Security & Data Privacy Compliance
- **RA 10173 (Data Privacy Act of 2012):** Sensitive requester data is encrypted at rest using AES-256 and in transit via TLS 1.3.
- **RA 11032 (Ease of Doing Business):** All service catalogs enforce real-time statutory SLA countdown clocks.
- **Non-Repudiation:** Approvals execute cryptographic hashing on approver identity, position, and action timestamp.
