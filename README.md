# CivicOS — Government Scheme Discovery Platform

> **"One place to discover, understand, and access the government benefits you're entitled to."**

AI-powered platform that searches live government sources, checks your eligibility using deterministic rules, and explains exactly why you match — or what's missing. Built with AWS open-source technologies, zero cloud cost.

![Built with](https://img.shields.io/badge/Built%20with-AWS%20Open%20Source-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Cost](https://img.shields.io/badge/Cost-$0-brightgreen)

---

## Technology → Role Map

Every required technology has a real, load-bearing job:

| Requirement | Technology | Its Job in CivicOS |
|---|---|---|
| **Agents and AI** | Strands Agents SDK | Orchestrator + sub-agents (Profile, Scheme, Document, Recommendation). Owns reasoning, tool calling, agent-as-tools pattern |
| **Agents and AI** | PartyRock | Used for prototyping conversational flows before building agents |
| **Containers** | Finch | Builds and runs all containers (`finch compose`) |
| **Kubernetes** | EKS Distro | Kubernetes manifests target the same distro as AWS EKS |
| **On-Prem** | EKS Anywhere | Air-gapped government deployment — same manifests, zero cloud |
| **Serverless** | SAM CLI | Defines S3 upload bucket, SQS processing queue, Lambda functions |
| **Serverless** | LocalStack | Runs SAM stack locally with `samlocal` — zero AWS account |
| **Isolation** | Firecracker | Document OCR/extraction in throwaway microVMs |
| **Search** | OpenSearch | Knowledge/cache layer — hybrid keyword + vector search for discovered schemes |
| **Authorization** | Cedar | Policy-decision point gating every agent tool call. Fail-closed. |
| **Data** | MongoDB | User data only (profiles, conversations, saved schemes). Never scheme data. |
| **Frontend** | React + Vite + Tailwind v4 | Premium UI with verified/unverified trust signals, eligibility breakdown |
| **LLM** | Ollama (local) | Free, local model for Build It track. Swap to Bedrock for Ship It. |

---

## Architecture

```
┌──────────────────────────────────┐
│  React + Vite + Tailwind v4       │
│  Premium UI with trust signals    │
└───────────────┬──────────────────┘
                │ REST / SSE
┌───────────────▼──────────────────┐
│   Orchestrator — FastAPI          │
│   Strands Agent + Cedar policies  │
└───┬──────────┬──────────┬────────┘
    │          │          │
┌───▼────┐ ┌──▼───┐ ┌───▼──────┐
│Profile │ │Scheme│ │Document  │
│Agent   │ │Agent │ │Agent     │
└────────┘ └──┬───┘ └──────────┘
              │
    ┌─────────┼──────────┐
    ▼         ▼          ▼
  Tavily   OpenSearch  Eligibility
  Search   (cache)     Engine (Python)
    │
    ▼
  Gov URL Validator → Fetch & Parse → Extract
```

### Key Principles
- **Never hardcode schemes** — discovered at request time via live search
- **LLM extracts, never decides** — eligibility is deterministic (Python engine)
- **"You appear to meet the published criteria"** — never "you are eligible"
- **Verified sources only** — `.gov.in` / `.nic.in` domains, with trust badges

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker or Finch
- Ollama (`ollama pull llama3.1`)

### 1. Clone & Configure
```bash
git clone https://github.com/your-username/civicos.git
cd civicos
cp .env.example .env
# Add your TAVILY_API_KEY (free at tavily.com)
```

### 2. Start Infrastructure
```bash
# Using Docker Compose (or `finch compose`)
docker compose -f docker-compose.dev.yml up -d
```

### 3. Start Eligibility Engine
```bash
cd backend/eligibility-engine
pip install -r requirements.txt
python main.py
```

### 4. Start Orchestrator
```bash
cd backend/orchestrator
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit **http://localhost:3000**

---

## Project Structure

```
civicos/
├── frontend/                 # React + Vite + Tailwind v4
├── backend/
│   ├── orchestrator/         # FastAPI + Strands Agents SDK
│   │   └── app/
│   │       ├── agents/       # Orchestrator, Profile, Scheme, Document, Recommendation
│   │       ├── tools/        # Search, Retriever, Extractor, Eligibility Client
│   │       ├── api/          # REST endpoints
│   │       ├── models/       # Pydantic schemas
│   │       ├── services/     # LLM, dedup, caching
│   │       └── db/           # MongoDB
│   ├── eligibility-engine/   # Deterministic rules (Python, replaces Java)
│   ├── policies/             # Cedar authorization policies
│   ├── search-index/         # OpenSearch mappings
│   └── document-sandbox/     # Firecracker microVM config
└── infra/
    ├── sam/                  # SAM CLI templates + Lambda functions
    ├── eks-distro/           # Kubernetes manifests
    ├── eks-anywhere/         # Air-gapped deployment config
    └── localstack/           # LocalStack config
```

---

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /chat` | Conversational turn |
| `POST /profile/extract` | Structured profile from text |
| `POST /schemes/search` | Live search → retrieve → extract → cache |
| `POST /schemes/check-eligibility` | Deterministic eligibility evaluation |
| `GET /schemes/{id}` | Scheme detail |
| `POST /schemes/save` | Save to user account |
| `POST /documents/upload` | Document upload → sandbox |

---

## Deployment Options

| Scenario | How | Code Changes |
|---|---|---|
| **Local Dev (Build It)** | `docker compose up` + Ollama | None |
| **Cloud (Ship It)** | EKS + Bedrock | `MODEL_PROVIDER=bedrock` |
| **Air-Gapped Gov** | EKS Anywhere on-prem | None |

---

## License

MIT

---

**Built with ❤️ for social impact — WeMakeDevs × AWS First Commit Hackathon**
