# n8n Workflows

> **Purpose:** Automation workflows for KLM V2 content generation
> **Framework:** n8n (despite Bible recommendation for Prefect - see DEVIATIONS.md)
> **Status:** Phase 5 - Foundation Setup

---

## Quick Start

1. **Install n8n:**
```bash
npm install n8n -g
# or
docker run -it --rm -p 5678:5678 n8nio/n8n
```

2. **Start n8n:**
```bash
n8n start
# or
docker run -it --rm -p 5678:5678 -v ~/.n8n:/root/.n8n n8nio/n8n
```

3. **Access:** http://localhost:5678

4. **Import workflows:** Import JSON files from `workflows/` directory

---

## Workflows

| Workflow | File | Purpose | Status |
|----------|------|---------|--------|
| **Content Ingestion** | `content-ingestion.json` | YouTube → Database | Planned |
| **Quality Check** | `quality-gate.json` | MARS validation | Planned |
| **Visual Generation** | `visual-gen.json` | ComfyUI automation | Planned |
| **Audio Mastering** | `audio-master.json` | EQ & producer tag | Planned |
| **Distribution** | `distribution.json` | Publish to platforms | Planned |

---

## Brand Enforcement

All workflows must enforce brand identity:

### Colors (Must Use)

- **Mekong Gold:** `#EBCB00`
- **Deep Teal:** `#374C57`
- **Electric Magenta:** `#E20263`
- **Stone Grey:** `#A29E98`

### Quality Thresholds

- **MARS Score:** Must be ≥ 0.7 before publishing
- **Cultural Check:** Must pass Historian validation
- **Translation:** Must use standard Khmer romanization

### Prohibited

- ❌ Khmer Rouge imagery
- ❌ Political content
- ❌ Cultural appropriation

---

## Directory Structure

```
n8n/
├── workflows/
│   ├── content-ingestion.json
│   ├── quality-gate.json
│   ├── visual-gen.json
│   ├── audio-master.json
│   └── distribution.json
├── scripts/
│   ├── import-workflows.sh
│   └── export-workflows.sh
└── README.md
```

---

## Integration Points

| Service | Purpose | Connection |
|---------|---------|------------|
| **YouTube** | Source content | yt-dlp for downloads |
| **Gemini API** | AI analysis | Content generation |
| **ComfyUI** | Visual generation | Local API |
| **Supabase** | Database | PostgreSQL |
| **ChromaDB** | Vector search | RAG system |
| **Fourthwall** | Merch | Product creation |

---

## Naming Conventions

- Workflows: ` kebab-case.json`
- Variables: `KLM_VARIABLE_NAME`
- Credentials: Named descriptively

---

## Development Guidelines

1. **Test locally** before deployment
2. **Document** each workflow's purpose
3. **Use sub-nodes** for complex logic
4. **Error handling** on all API calls
5. **Logging** for debugging

---

## Deployment

### Development
```bash
n8n start
```

### Production
```bash
export N8N_ENCRYPTION_KEY=your-key
n8n start --production
```

See `30-Implementation/docker-compose.yml` for container setup.

---

## References

| Document | Location | Purpose |
|----------|----------|---------|
| Brand Identity | `60-Resources/PLAYBOOK/08-BRAND_IDENTITY.md` | Visual/audio specs |
| Bible (Full) | Chat History (2026-02-11) | Complete specs |
| Deviation Log | `DEVIATIONS.md` | n8n vs Prefect conflict |
