# TECHNICAL DESIGN DOCUMENT (TDD)
## Lingkod-Dinig AI: AI-Assisted Legislative Transcription & Parliamentary Minutes Intelligence System
### High-Performance Audio Processing, Acoustic Diarization, Multi-Model Speech-to-Text, and Audio-Synced Stenographer Web Workbench

**Document Reference:** HREP-TDD-S13-2026-v1.0  
**System Code:** UGNAYAN-SYS-13  
**Classification:** Internal Restricted / Confidential Processing Architecture  
**Target Deployment:** Hybrid Cloud (Google Cloud Vertex AI Speech-to-Text Chirp 2 + On-Premises Air-Gapped GPU Node for Executive Sessions)  

---

### Table of Contents
1. [Architecture Overview & Hybrid Topology](#1-architecture-overview--hybrid-topology)
2. [Audio Ingestion, Splitting & Preprocessing Pipeline](#2-audio-ingestion-splitting--preprocessing-pipeline)
3. [Acoustic Diarization & Multi-Model Speech-to-Text Engines](#3-acoustic-diarization--multi-model-speech-to-text-engines)
4. [Legislative LLM Intelligence & Parliamentary Summarization](#4-legislative-llm-intelligence--parliamentary-summarization)
5. [Interactive Audio-Synced Stenographer Workbench](#5-interactive-audio-synced-stenographer-workbench)
6. [Data Architecture & Database Schema](#6-data-architecture--database-schema)
7. [RESTful & WebSocket API Specifications](#7-restful--websocket-api-specifications)
8. [Executive Session Air-Gapping & Security Architecture](#8-executive-session-air-gapping--security-architecture)
9. [UGNAYAN Super App Integration Architecture](#9-ugnayan-super-app-integration-architecture)

---

### 1. Architecture Overview & Hybrid Topology

Lingkod-Dinig AI (System 13) provides an enterprise-grade automated speech-to-text, acoustic diarization, and parliamentary minutes generation pipeline for all House plenary sessions and committee hearings.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                AUDIO & VIDEO INGESTION SOURCES                                  │
├────────────────────────────────┬───────────────────────────────┬────────────────────────────────┤
│ 1. Plenary Hall Broadcast Feeds│ 2. Committee Hybrid Streams   │ 3. Offline Stenographer Uploads│
│    (SDI / Dante Audio Over IP) │    (Google Meet Notes API)    │    (MP3, WAV, M4A, MP4, MKV)   │
└────────────────┬───────────────┴───────────────┬───────────────┴────────────────┬───────────────┘
                 │                               │                                │
                 ▼                               ▼                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            FASTAPI AUDIO INGESTION & PIPELINE GATEWAY                           │
│  - Chunking Engine (FFmpeg, 16kHz mono FLAC)                                                    │
│  - Voice Activity Detection (Silero VAD)                                                        │
│  - Routing Logic: Public / Regular Hearing vs. Classified Executive Session                     │
└────────────────────────────────┬───────────────────────────────┬────────────────────────────────┘
                                 │                               │
                [Standard / Public Proceedings]     [Executive / Classified Sessions]
                                 │                               │
                                 ▼                               ▼
┌──────────────────────────────────────────────┐ ┌──────────────────────────────────────────────┐
│        CLOUD PIPELINE (GCP VERTEX AI)        │ │        AIR-GAPPED ON-PREM GPU WORKER         │
│  - Google Cloud Speech-to-Text (Chirp 2)     │ │  - Self-Hosted Whisper Large-v3 (FP16)       │
│  - PyAnnote 3.1 Diarization Container        │ │  - Local PyAnnote Speaker Diarization        │
│  - Gemini 1.5 Pro Parliamentary Summarizer   │ │  - Local Gemma 2 27B Quantized Summarizer    │
│  - Cloud Storage Audio Bucket (Encrypted)    │ │  - Isolated ZFS Encrypted Storage Node       │
└──────────────────────┬───────────────────────┘ └──────────────────────┬───────────────────────┘
                       │                                                │
                       └───────────────────────┬────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             TRANSCRIPT POST-PROCESSING & EMBEDDINGS                             │
│  - Philippine Parliamentary Vocabulary & Honorifics Post-Processor                             │
│  - Vertex AI Embeddings (text-embedding-004) -> pgvector Semantic Search Index                 │
└──────────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                      STENOGRAPHER WORKBENCH & SUPER APP INTEGRATION                             │
│  - Audio-Synced Interactive Editor (WaveSurfer.js + Web HID Foot Pedal Driver)                  │
│  - Push Draft Minutes to LODS (System 01) & RMS (System 03)                                     │
│  - Universal Action Center Alerts via Cloud Pub/Sub                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Audio Ingestion, Splitting & Preprocessing Pipeline

#### 2.1 Audio Ingestion Specifications
- **Supported Codecs & Containers:** PCM WAV, FLAC, AAC, MP3, Opus, Ogg, MP4, MOV, MKV.
- **Normalization Pipeline:**
  - FFmpeg converts raw audio to `16,000 Hz, 16-bit, Single-Channel (Mono) FLAC`.
  - Dynamic Range Compression and High-Pass Filter (80 Hz cut-off) to remove ambient air conditioning rumble in hearing rooms.
- **Chunking Strategy:**
  - Audio files > 30 MB or longer than 15 minutes are chunked into 10-minute overlapping segments (1.5-second overlap at VAD-detected silence boundaries) to prevent cut-off words.

```python
# audio_processor.py
import subprocess
import os

def normalize_audio(input_path: str, output_path: str) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-af", "highpass=f=80, loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "flac",
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

---

### 3. Acoustic Diarization & Multi-Model Speech-to-Text Engines

#### 3.1 Model Orchestration
1. **Google Cloud Chirp 2 / Speech-to-Text V2:**
   - Primary cloud engine for public hearings and plenary sessions.
   - Configured with `fil-PH` and `en-PH` dual-language adaptation and legislative custom vocabulary.
2. **PyAnnote 3.1 Speaker Diarization:**
   - Computes voice embeddings for every vocal turn and matches against the **HRep Lawmaker Voiceprint Registry** (5-second enrolled reference vectors of 300+ House Members).
3. **Philippine Legislative Lexicon & Spell-Normalization Engine:**
   - Ingests customized regex and dictionary rules mapping phonetically confused phrases to official terms (e.g., "Fiscalizer", "Bicam", "Substitute Bill", "Interpellate", "Contempt", "BARMM").

---

### 4. Legislative LLM Intelligence & Parliamentary Summarization

Once raw transcripts are assembled and aligned with speaker turns, the platform invokes Gemini 1.5 Pro to synthesize structured parliamentary minutes:

```json
{
  "session_id": "COMM-APPROP-2026-03-12-01",
  "presiding_officer": "Rep. Elizaldy Co",
  "agenda_items_discussed": [
    {
      "bill_number": "HB00102",
      "topic": "FY 2027 DPWH Infrastructure Allocations",
      "motions": [
        {"mover": "Rep. Sandro Marcos", "motion": "Approval of Committee Report No. 42", "result": "Carried"}
      ],
      "key_interpellations": [
        {"interpellator": "Rep. Raoul Manuel", "respondent": "DPWH Secretary", "summary": "Clarification on flood control projects in Region III."}
      ]
    }
  ],
  "action_items": [
    {"assignee": "CAD Committee Secretary", "action": "Submit finalized clean copy to Bills and Index Service by 5:00 PM tomorrow.", "deadline": "2026-03-13T17:00:00Z"}
  ]
}
```

---

### 5. Interactive Audio-Synced Stenographer Workbench

- **Audio Waveform Visualization:** Integrated WaveSurfer.js rendering interactive waveform with speaker color tags.
- **Bi-directional Time Synchronization:** Clicking any word in the transcript jumps audio playback directly to that millisecond; playing audio highlights current words in real-time.
- **Hardware Foot Pedal Support:** Native Web HID API binding for standard Infinity IN-USB-2 and Olympus RS31H foot pedals (Play, Pause, Rewind 3s, Fast-Forward).

---

### 6. Data Architecture & Database Schema

```sql
CREATE TABLE transcription_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_code VARCHAR(100) UNIQUE NOT NULL,
    session_title VARCHAR(255) NOT NULL,
    hearing_type VARCHAR(50) NOT NULL CHECK (hearing_type IN ('PLENARY', 'COMMITTEE', 'EXECUTIVE_SESSION', 'BICAM')),
    committee_id UUID REFERENCES departments(id),
    audio_file_path VARCHAR(500) NOT NULL,
    audio_duration_seconds INTEGER NOT NULL,
    classification VARCHAR(50) DEFAULT 'PUBLIC' CHECK (classification IN ('PUBLIC', 'CONFIDENTIAL', 'SECRET_EXECUTIVE')),
    processing_status VARCHAR(50) DEFAULT 'PENDING' CHECK (processing_status IN ('PENDING', 'PROCESSING', 'READY_FOR_REVIEW', 'VERIFIED', 'PUBLISHED')),
    word_error_rate_estimate NUMERIC(5,2),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE transcript_turns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES transcription_sessions(id) ON DELETE CASCADE,
    turn_sequence INTEGER NOT NULL,
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    speaker_id UUID REFERENCES users(id),
    speaker_label VARCHAR(100) NOT NULL,
    confidence_score NUMERIC(4,3),
    raw_text TEXT NOT NULL,
    edited_text TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE parliamentary_minutes_summary (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES transcription_sessions(id) ON DELETE CASCADE,
    executive_summary TEXT NOT NULL,
    structured_json JSONB NOT NULL,
    motions_count INTEGER DEFAULT 0,
    action_items_count INTEGER DEFAULT 0,
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### 7. RESTful & WebSocket API Specifications

#### 7.1 Endpoints
- `POST /api/v1/transcription/upload`: Upload raw audio/video and trigger automated transcription pipeline.
- `GET /api/v1/transcription/{session_id}`: Retrieve session metadata, audio stream URL, and transcription turns.
- `PATCH /api/v1/transcription/turns/{turn_id}`: Update edited transcript text and speaker tag.
- `POST /api/v1/transcription/{session_id}/generate-minutes`: Trigger Gemini parliamentary minutes synthesis.
- `GET /api/v1/transcription/{session_id}/export`: Export transcript in PDF, DOCX, or Congressional Record XML.

#### 7.2 WebSocket Streaming
- `WS /api/v1/transcription/live/{session_id}`: Real-time broadcast of live transcription words during ongoing hearings.

---

### 8. Executive Session Air-Gapping & Security Architecture

1. **Zero Egress Routing:** When `classification == 'SECRET_EXECUTIVE'`, the API Gateway isolates the payload strictly to on-premise Kubernetes worker pods containing local Whisper v3 and local Gemma 2.
2. **Data Erasure:** Temporary audio slices in memory are overwritten with random bytes upon task completion. Audio files are encrypted at rest using AES-256 with keys stored in an on-premises Hardware Security Module (HSM).

---

### 9. UGNAYAN Super App Integration Architecture

1. **Legislative Operations System (System 01):** Verified transcripts and approved minutes automatically sync into the legislative history of associated bills.
2. **Document Management System (System 02) & Records (System 03):** Final approved Congressional Records are cataloged for permanent archival with cryptographic checksums.
3. **Universal Action Center:** Pub/Sub notifications alert Committee Secretaries and Plenary Directors when transcription drafts are ready for sign-off.
