# Prefect Flows

> **Purpose:** Python-native workflow orchestration (future migration from n8n)
> **Framework:** Prefect 3.x
> **Status:** FOUNDATION SETUP - Not active, prepared for migration
> **Migration Trigger:** When n8n workflow count > 10 or songs > 1000

---

## Quick Start (For Future Use)

```bash
# Install Prefect
pip install prefect

# Start Prefect server (UI)
prefect server start

# Run a flow locally
python flows/night_shift.py
```

---

## Directory Structure

```
prefect/
├── flows/
│   ├── __init__.py
│   ├── night_shift.py         # Batch processing (50+ songs)
│   ├── content_ingestion.py    # YouTube → Database
│   ├── quality_gate.py        # MARS validation
│   ├── aokhmer_generation.py  # AI song creation
│   └── distribution.py        # Publishing automation
├── deployments/
│   ├── ingestion_deployment.yaml
│   └── nightly_deployment.yaml
├── tasks/
│   ├── __init__.py
│   ├── youtube_tasks.py
│   ├── whisper_tasks.py
│   ├── gemini_tasks.py
│   ├── comfyui_tasks.py
│   └── chromadb_tasks.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
└── README.md
```

---

## Flows

| Flow | File | Purpose | Status |
|------|------|---------|--------|
| **Night Shift** | `flows/night_shift.py` | Batch processing (50+ songs) | Template |
| **Content Ingestion** | `flows/content_ingestion.py` | YouTube → Database | Template |
| **Quality Gate** | `flows/quality_gate.py` | MARS validation | Template |
| **AOKhmer Generation** | `flows/aokhmer_generation.py` | Visual content | Template |
| **Distribution** | `flows/distribution.py` | Publishing | Template |

---

## Why Prefect (Future)

| Aspect | n8n (Current) | Prefect (Future) |
|--------|---------------|-----------------|
| Scale | < 10 workflows | 10+ workflows |
| Volume | < 1000 songs | 1000+ songs |
| Complexity | Simple automations | Complex dependencies |
| Version Control | JSON files | Python code |
| Testing | Manual | Unit tests |
| Deployment | n8n instance | Cloud-native |

---

## Migration Checklist

When ready to migrate from n8n:

- [ ] Flow count exceeds 10 workflows
- [ ] Monthly songs processed > 1000
- [ ] Complex dependency chains needed
- [ ] Team collaboration required
- [ ] Cloud deployment needed

---

## Current Status

**DO NOT USE** - Prefect is set up as a template only.

**Current Automation:** Use n8n (`30-Implementation/n8n/`)

**Why:**
- n8n is sufficient for current scale
- User comfortable with n8n visual workflow
- Prefect adds unnecessary complexity for POC

---

## Integration Points

| Service | n8n Connection | Prefect Connection |
|---------|----------------|-------------------|
| YouTube | HTTP Request | Prefect YouTube Task |
| Gemini API | HTTP Request | Prefect Gemini Task |
| ComfyUI | HTTP Request | Prefect ComfyUI Task |
| Supabase | Postgres Node | Prefect SQL Task |
| ChromaDB | HTTP Request | Prefect Vector Task |

---

## Example Flow Structure

```python
# flows/content_ingestion.py
from prefect import flow, task
from typing import Dict, List

@task(retries=2, retry_delay_seconds=60)
def download_youtube_audio(video_id: str) -> str:
    """Download audio from YouTube."""
    # Implementation
    return audio_path

@task(retries=3)
def transcribe_audio(audio_path: str) -> Dict:
    """Transcribe using Whisper."""
    # Implementation
    return transcript

@task
def analyze_with_gemini(transcript: Dict) -> Dict:
    """Generate analysis with Gemini."""
    # Implementation
    return analysis

@flow(name="Content Ingestion")
def content_ingestion_flow(video_urls: List[str]) -> List[Dict]:
    """Main ingestion flow."""
    results = []
    for url in video_urls:
        audio = download_youtube_audio(url)
        transcript = transcribe_audio(audio)
        analysis = analyze_with_gemini(transcript)
        results.append(analysis)
    return results

if __name__ == "__main__":
    content_ingestion_flow(["https://youtube.com/watch?v=..."])
```

---

## n8n → Prefect Mapping

| n8n Node | Prefect Equivalent |
|-----------|-------------------|
| Manual Trigger | Prefect Flow |
| HTTP Request | @task decorated function |
| If/Filter | prefect.blocks.logic.Filter |
| Slack | prefect.notifications.Slack |
| PostgreSQL | prefect_sqlalchemy |
| Function | @task decorated function |

---

## References

| Document | Location | Purpose |
|----------|----------|---------|
| n8n Workflows | `30-Implementation/n8n/` | Current automation |
| Brand Identity | `60-Resources/PLAYBOOK/08-BRAND_IDENTITY.md` | Quality specs |
| Bible (Full) | Chat History (2026-02-11) | Complete specs |

---

## Notes

- Prefect is set up but NOT ACTIVE
- Keep n8n as primary until migration trigger
- When migrating, port one flow at a time
- Test each flow before deprecating n8n equivalent
