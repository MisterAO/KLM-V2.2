# KLM V2.2 - Multi-Agent RAG System for Khmer Language Learning

> **Version:** 2.2.0
> **Status:** Phase 0-4 Complete | Ready for Backend Coding
> **Last Updated:** 2026-02-12

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/MisterAO/KLM-V2.2.git
cd KLM-V2.2

# 2. Setup environment
cp .env.v2.2.example .env
# Edit .env with your API keys

# 3. Start services (see ENVIRONMENT_SETUP.md)
```

---

## What's Inside

| Component | Status | Description |
|-----------|--------|-------------|
| **14 Agents** | ✅ Ready | Dify configurations for full ecosystem |
| **Prefect Flows** | ✅ 4 flows | Ingestion, self-healing, night-shift |
| **n8n Workflows** | ✅ 5 workflows | Automation and triggers |
| **CI/CD Pipeline** | ✅ Ready | GitHub Actions + deployment scripts |
| **Agent SOPs** | ✅ 14 SOPs | Complete operational guides |
| **Backend** | 🔄 Structure | Ready for ingestion workflow coding |

---

## Project Structure

```
KLM-V2.2/
├── README.md                    ← You are here
├── AGENTS.md                    ← Agent operational guide
├── PROJECT_MAP.md               ← Architecture overview
├── docs/
│   └── CI_CD_ARCHITECTURE.md    ← CI/CD documentation
├── scripts/
│   └── deploy.sh                ← Deployment scripts
├── backend/                     ← Python backend (coding starts here)
├── 30-Implementation/
│   ├── dify/agents/            ← 14 agent configurations
│   ├── prefect/flows/          ← Prefect orchestration
│   └── n8n/workflows/         ← n8n automation
├── 40-SOPs/
│   └── AGENTS/                 ← Agent SOPs
├── 90-Project-Board/           ← Project tracking
└── V22_PHASE*_COMPLETION_*.md ← Phase documentation
```

---

## Agent Ecosystem (14 Agents)

### C-Suite
- **AGT-000 CEO** - Strategic vision, final authority
- **AGT-006 Chief of Staff** - Operations, coordination
- **AGT-011 Strategist** - Efficiency optimization

### Operations
- **AGT-001 Molt** - Content, Users, Operations
- **AGT-002 OpenCode** - Code, Infrastructure, Database
- **AGT-003 Guardian** - Security, Quality, Compliance
- **AGT-005 Historian** - Documentation, Knowledge
- **AGT-007 Documenter** - Docs sync, output format
- **AGT-013 Consultant** - Gap analysis, risk assessment

### Specialists
- **AGT-014 n8n Expert** - Workflow automation
- **AGT-015 Prefect Expert** - Orchestration, flows
- **AGT-004 Stakeholder Liaison** - External communications
- **AGT-012 Memory Keeper** - RAG, context, vector store
- **AGT-016 Vibe Monitor** - Pattern detection

---

## Next Steps

1. **Begin Backend Coding** - Ingestion workflow
2. **Phase 5** - Parallel Execution Upgrade (planned)
3. **Phase 6** - Documentation & Launch (planned)
4. **Phase 7** - Training & v3 Prep (planned)

---

## Documentation

- [AGENTS.md](AGENTS.md) - Agent operational guide
- [PROJECT_MAP.md](PROJECT_MAP.md) - Architecture overview
- [docs/CI_CD_ARCHITECTURE.md](docs/CI_CD_ARCHITECTURE.md) - CI/CD docs
- [40-SOPs/AGENTS/](40-SOPs/AGENTS/) - Agent SOPs

---

*Khmer Language Learning Made Intelligent*
