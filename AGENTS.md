# 🤖 AGENTS.md

> **Operational guide for AI agents working on AOKhmer**
> **Version:** 2.2.0
> **Last Updated:** 2026-02-12
> **Status:** PRODUCTION

---

## 🎯 Quick Start

**I am:** OpenCode (AGT-002) - Lead Engineer
**My Domain:** Code, Infrastructure, Database, Git, Security
**What I do:** Build features, fix bugs, deploy systems
**My SOP:** `40-SOPs/AGENTS/AGENT-OPENCODE.md`

**Before starting work, read:**
1. This file
2. My SOP (`40-SOPs/AGENTS/AGENT-OPENCODE.md`)
3. Relevant technical SOPs in `40-SOPs/Phase-2-God-Tier/`

---

## 📁 Project Structure

```
AOKhmer/
├── 00-START_HERE/          # Entry point documentation
├── 10-Foundations/         # Core philosophy & principles
│   ├── SYSTEM_PHILOSOPHY.md    # Four Axioms
│   └── AGENT_HANDSHAKE.md      # Role definitions
├── 20-Architecture/        # System diagrams & design
│   └── diagrams/
├── 30-Implementation/      # Deployment configs
│   ├── scripts/
│   ├── kubernetes/
│   └── docker-compose.yml
├── 40-SOPs/               # Standard Operating Procedures
│   ├── AGENT_REGISTRY.md      # All agents
│   ├── SOP_INDEX.md          # All SOPs
│   ├── AGENTS/               # Agent-specific SOPs
│   └── Phase-2-God-Tier/     # Technical SOPs
├── 50-Operations/         # Runbooks & monitoring
├── 60-Resources/          # Templates & assets
├── 70-Training/           # Best practices & guides
│   └── best-practices/
│       ├── CODE_STYLE.md
│       └── SECURITY.md
│
├── 80-Sessions/           # Session logs & audit trail
│   ├── INDEX.md              # Session dashboard
│   ├── TEMPLATES/            # Session log templates
│   └── 2026-02/              # Monthly session folders
│
├── 90-Project-Board/      # Kanban board & task tracking
│   ├── README.md             # Board overview
│   └── 01-High-Backlog/      # Task columns
│
├── backend/               # Python backend (NEW)
│   ├── src/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── models/       # Pydantic/SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   ├── workers/      # Background tasks
│   │   └── utils/        # Helpers
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── migrations/       # Database migrations
│   └── scripts/          # Utility scripts
│
├── frontend/             # FlutterFlow frontend reference
│   ├── docs/
│   └── assets/
│
├── DEVIATIONS.md         # SOP deviations log
└── AGENTS.md            # This file
```

---

## 📝 Session Logging & Knowledge Management

### Mandatory: Log Every Session

OpenCode MUST log every development session for V3 knowledge preservation:

#### The Learning Series Purpose

> "Every decision, every problem solved, every feature built should be documented as a learning series for future developers."

**Future developers should be able to:**
- Read our journey and understand HOW we built this
- Understand WHY we made certain decisions
- Learn WHAT problems we faced and HOW we solved them
- Onboard faster by reading our story

#### What to Document (As We Work)

| Document | When | Why |
|----------|------|-----|
| **PLAYBOOK** | Feature progress | Technical "how-to" for future devs |
| **JOURNAL** | Daily journey | Story of our development process |
| **DECISION_LOG** | Every decision | Rationale for choices made |
| **ROADBLOCKS** | Problem solved | Solutions to common issues |
| **TIPS_TRICKS** | Lessons learned | Non-obvious insights |

#### Session Structure
```
80-Sessions/
├── INDEX.md                    # Master session index
├── KNOWLEDGE_MANAGEMENT.md      # This guide
├── TEMPLATES/
│   └── SESSION_TEMPLATE.md      # Copy to session files
└── YYYY-MM/
    └── YYYY-MM-DD_session-name/
        ├── SUMMARY.md          # Executive overview
        ├── FULL_LOG.md         # Complete conversation log
        ├── DECISIONS.md        # Key decisions + rationale
        ├── COMMITS.md          # Git commits + context
        ├── METRICS.md          # KPIs
        └── CHAT_EXPORT.md      # Full chat export ⭐
```

#### Quick Start Session Logging

```bash
# 1. Create session folder
mkdir -p 80-Sessions/2026-02/2026-02-11_feature-name/

# 2. Copy template to all files
cp 80-Sessions/TEMPLATES/SESSION_TEMPLATE.md 80-Sessions/2026-02/2026-02-11_feature-name/SUMMARY.md
cp 80-Sessions/TEMPLATES/SESSION_TEMPLATE.md 80-Sessions/2026-02/2026-02-11_feature-name/FULL_LOG.md
cp 80-Sessions/TEMPLATES/SESSION_TEMPLATE.md 80-Sessions/2026-02/2026-02-11_feature-name/DECISIONS.md
cp 80-Sessions/TEMPLATES/SESSION_TEMPLATE.md 80-Sessions/2026-02/2026-02-11_feature-name/COMMITS.md
cp 80-Sessions/TEMPLATES/SESSION_TEMPLATE.md 80-Sessions/2026-02/2026-02-11_feature-name/METRICS.md

# 3. Export chat to export_chat/
cp export_chat/CHAT_EXPORT_TEMPLATE.md export_chat/YYYY-MM-DD_[session-name]-export.md
```

#### Session Export (Required)

**Every session must export the full chat to:**
- `export_chat/YYYY-MM-DD_[session-name]-export.md`
- `80-Sessions/YYYY-MM/YYYY-MM-DD_session-name/CHAT_EXPORT.md`

**Why:**
- V3 knowledge preservation
- Complete conversation context
- Future developers can read full discussions
- Audit trail for decisions

#### End of Session Checklist
- [ ] Complete all 5 session files
- [ ] Add session link to `80-Sessions/INDEX.md`
- [ ] Export chat to `export_chat/` ⭐ REQUIRED
- [ ] Copy export to session folder ⭐ REQUIRED
- [ ] Update `90-Project-Board/SPRINT_TRACKER.md`
- [ ] Update `60-Resources/PLAYBOOK/` if new patterns
- [ ] Update `DEVIATIONS.md` if any SOP deviations

#### Documentation Updates Required

| Document | When to Update |
|----------|----------------|
| `60-Resources/PLAYBOOK/02-DECISION_LOG.md` | New architecture decisions |
| `60-Resources/PLAYBOOK/03-ROADBLOCKS.md` | New problems + solutions |
| `60-Resources/PLAYBOOK/04-COMMANDS.md` | New commands discovered |
| `60-Resources/PLAYBOOK/07-TIPS_TRICKS.md` | New insights |
| `90-Project-Board/SPRINT_TRACKER.md` | Task completion |
| `DEVIATIONS.md` | SOP deviations |

---

## ⚙️ Build/Lint/Test Commands

### Python Development
```bash
# Setup (one time)
pip install -e ".[dev]"

# Development server
uvicorn src.main:app --reload

# Code quality
black backend/src              # Format code
isort backend/src              # Sort imports
ruff check backend/src         # Lint code
mypy backend/src               # Type checking

# Testing
pytest backend/tests           # Run all tests
pytest backend/tests -v        # Verbose output
pytest backend/tests/unit      # Run only unit tests
pytest backend/tests -k "test_name"  # Run specific test
pytest --cov=backend/src       # Run with coverage

# Full check (runs in pre-commit)
black --check backend/src
isort --check-only backend/src
ruff check backend/src
mypy backend/src
pytest backend/tests
```

### LCI (Lightning Code Index)
```bash
# Verify LCI setup
npx lci status

# Initial indexing warm-up (v0.4.0)
npx lci list
npx lci search "guardian_loop"

# MCP server (stdio)
npx lci mcp

# Core tools
npx lci search <query>   # Semantic code search
npx lci grep <pattern>   # Fast text search
npx lci def <symbol>     # Symbol definition
npx lci refs <symbol>    # Symbol references
npx lci tree <function>  # Call hierarchy
```

### CodeSentinel (Codebase Change Tracking)
```bash
# Generate a codebase change report for handoffs/PR context
python scripts/codebase_tracker.py

# Outputs
# - 90-Project-Board/DASHBOARD_DATA/codebase_change_report.md
# - 90-Project-Board/DASHBOARD_DATA/codebase_change_summary.json
```

---

## 🖥️ IDE Workflow (VS Code)

We use **VS Code** with structured AI autonomy to maintain SOP compliance while enabling rapid development.

### Quick Start

1. **Install VS Code Extensions** (when prompted)
   - Python
   - Pylance
   - Black Formatter
   - Ruff
   - isort
   - GitLens
   - (Optional) GitHub Copilot

2. **Open Project in VS Code**
   ```bash
   code .
   ```

3. **IDE Will Auto-Configure:**
   - Virtual environment (venv/)
   - Python interpreter
   - Format on save (Black)
   - Lint on save (Ruff)
   - Type checking (mypy)

### AI Autonomy with Guardrails

**What AI Can Do Autonomously:**
- ✅ Suggest code completions
- ✅ Generate docstrings
- ✅ Refactor code
- ✅ Fix linting errors
- ✅ Auto-format on save

**What Requires Human/Agent Approval:**
- ⚠️ Creating new files (must update Kanban)
- ⚠️ Installing packages (must update pyproject.toml)
- ⚠️ Git commits (pre-commit hooks enforce SOPs)
- ⚠️ Database schema changes (requires migration)

### VS Code Tasks (Ctrl+Shift+P → Run Task)

**Setup:**
- `Setup: Install Dependencies` - Install all packages
- `Check Virtual Environment` - Verify venv exists

**Development:**
- `Server: Start FastAPI` - Run development server
- `Database: Start Supabase` - Start local database
- `Database: Run Migrations` - Apply migrations

**Quality:**
- `Format: Black` - Format code
- `Format: isort` - Sort imports
- `Lint: Ruff` - Check code quality
- `Type Check: mypy` - Verify types
- `Test: Run All` - Run test suite
- `Pre-commit: Run All Checks` - Full SOP check

**Git:**
- `Git: Create Feature Branch` - Start new feature
- `SOP: Check Compliance` - Verify SOP adherence

### Debugging (F5)

**Launch Configurations:**
- `Python: FastAPI (Uvicorn)` - Debug API server
- `Python: Current File` - Debug single file
- `Python: Pytest Current File` - Debug tests
- `Python: Pytest All Tests` - Debug all tests

### AI Tracking in IDE

**All AI Actions Are Logged:**
1. IDE settings include agent metadata:
   ```json
   "aokhmer.agent.id": "AGT-002",
   "aokhmer.sop.compliance": "strict",
   "aokhmer.session.logging": "enabled"
   ```

2. Each session captures:
   - Files created/modified by AI
   - Suggestions accepted/rejected
   - Time spent on tasks
   - Link to Kanban task

3. Pre-commit hooks ensure:
   - All code follows SOPs
   - Tests pass before commit
   - No secrets leaked

### Package Installation (Auto-Tracked)

**Method 1: Let IDE Auto-Install**
1. Type import statement: `import numpy as np`
2. IDE suggests installation
3. Approve installation
4. IDE automatically:
   - Installs to venv
   - Adds to `pyproject.toml`
   - Runs `pip install -e ".[dev]"`
   - Logs installation in session

**Method 2: Manual (Recommended)**
```bash
# Add to pyproject.toml dependencies
# Then run:
pip install -e ".[dev]"
```

**Tracking:**
- All package changes logged in session
- pyproject.toml commits show what was added
- Lock files track exact versions

### SOP Compliance in IDE

**Visual Indicators:**
- 🟢 Clean: No warnings/errors
- 🟡 Warning: TODO/FIXME comments
- 🔴 Error: Pre-commit will fail

**Enforced Rules:**
- Format on save (Black, line 88)
- Import sorting (isort)
- Type hints required (mypy strict)
- No direct commits to main
- Pre-commit hooks must pass

**Session Logging:**
- IDE tracks file changes
- Links to Kanban tasks
- Captures AI interactions
- Logs SOP compliance %

---

### Supabase (Local)
```bash
# Start Supabase
supabase start

# Database operations
supabase db reset              # Reset local database
supabase db diff               # Show pending migrations
supabase migration up          # Run migrations
supabase migration new <name>  # Create new migration

# Studio access
# http://localhost:54323 (Studio)
# http://localhost:54321 (API)
```

### Git Workflow
```bash
# Start new work item (baseline -> feature branch)
git checkout v2.1
git pull
git checkout -b feature/brief-description

# Alternative branch types
git checkout -b bugfix/brief-description
git checkout -b hotfix/brief-description

# Install hooks (one-time)
pre-commit install
pre-commit install --hook-type commit-msg
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/install_git_hooks.ps1

# Commit changes (pre-commit hooks enforce SOPs)
git add .
git commit -m "feat(scope): description | docs updated"

# Push and create PR
git push -u origin feature/description
# Create PR via GitHub UI

# After PR approved
git checkout v2.1
git pull
```

---

## 🧬 Agentic Version Control & Sync Rules (Vibe-Coding)

**1. Atomic Feature Branching**

- **Action**: For every new feature, refactor, or "vibe," you must first create a new branch from `v2.1`.
- **Command**: `git checkout -b feature/brief-description`.
- **Goal**: Isolate experiments so they don't corrupt the main "clean build" baseline.

**2. The "Twin-Commit" Requirement**

- **Action**: You are prohibited from committing code without updating the corresponding documentation.
- **Validation**: Every code/config commit must include changes to both source code and relevant `.md` files.
- **Message Format**: `feat(scope): brief description | docs updated`.

**3. Automatic Post-Commit Indexing**

- **Action**: After every successful commit, you must trigger a Code-Index refresh (LCI).
- **Goal**: Ensures internal search reflects the current state of the files.

**4. Pull Request (PR) Handover**

- **Action**: When a task is "done," do not merge locally. Open a PR and provide a "Vibe Summary".
- **Goal**: Enables architectural review before integration.

**Canonical SOP:** `40-SOPs/WORKFLOWS/WORKFLOW_AGENTIC_GIT_DOC_SYNC.md`

---

## 📝 Code Style Guidelines

### Python
- **Formatter:** Black (line length 88)
- **Import sorter:** isort (black profile)
- **Linter:** ruff
- **Type checker:** mypy (strict mode)

**Key Rules:**
```python
# ✅ DO: Use type hints
def process_song(song_id: str) -> dict[str, Any]:
    ...

# ✅ DO: Google-style docstrings
def create_user(email: str, password: str) -> User:
    """Create a new user.

    Args:
        email: User's email address
        password: Plain text password (will be hashed)

    Returns:
        Created user object

    Raises:
        ValueError: If email already exists
    """
    ...

# ❌ DON'T: Skip type hints
def bad_function(data):  # Missing types
    ...
```

### Naming Conventions
- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions/Variables:** `snake_case`
- **Constants:** `UPPER_CASE`
- **Private:** `_leading_underscore`
- **Test files:** `test_*.py`

### Error Handling
```python
# ✅ DO: Specific exceptions with context
try:
    user = await db.get_user(user_id)
except UserNotFoundError:
    logger.warning(f"User {user_id} not found")
    raise HTTPException(status_code=404, detail="User not found")
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Internal error")

# ❌ DON'T: Bare except or too broad
try:
    do_something()
except:  # Too broad!
    pass
```

---

## 🚨 Critical Rules

**AUTOMATIC DOCUMENTATION UPDATES:**
- ✅ When new patterns emerge → Update `60-Resources/PLAYBOOK/`
- ✅ When new tools discovered → Update `60-Resources/PLAYBOOK/04-COMMANDS.md`
- ✅ When new insights gained → Update `60-Resources/PLAYBOOK/07-TIPS_TRICKS.md`
- ✅ When problems solved → Update `60-Resources/PLAYBOOK/03-ROADBLOCKS.md`
- ✅ When new templates created → Update relevant PLAYBOOK section
- ✅ When Kanban tasks created/completed → Update `90-Project-Board/`
- ✅ **When SOP created/updated → Version control + git tracking**
- ✅ **SOP Version: Update header, changelog, and metadata**
- ✅ **Git: Create branch, commit with "sop:" prefix, PR review**

**BLOCKING (Pre-commit will fail):**
- ❌ Never commit `.env` files
- ❌ Never commit secrets/keys
- ❌ Never commit files >10MB
- ❌ Never push directly to `main`

**MANDATORY:**
- ✅ Always use feature branches
- ✅ All code must pass lint/type checks
- ✅ All tests must pass
- ✅ Document SOP deviations in `DEVIATIONS.md`

**ENFORCED BY PRE-COMMIT HOOKS:**
- Secrets detection
- Large file detection
- Python syntax validation
- Branch naming convention warnings

---

## 📚 Key SOPs

**My SOP (OpenCode):**
- `40-SOPs/AGENTS/AGENT-OPENCODE.md`

**Technical SOPs:**
- `01-Security-Master.md` - Security procedures
- `02-Self-Healing.md` - Monitoring & recovery
- `05-Database-Optimization.md` - Database best practices
- `06-CI-CD-Pipeline.md` - Deployment procedures
- `07-Testing-Framework.md` - Testing standards

**All SOPs:**
- `40-SOPs/SOP_INDEX.md` - Complete index
- `40-SOPs/AGENTS/COORDINATION_PROTOCOL.md` - Agent communication
- `40-SOPs/AGENTS/MULTI_AGENT_CHAT_PROTOCOL.md` - Real-time updates & end-of-day review, self-improvement

---

## 📝 Session Logging

**Every development session is logged in `80-Sessions/`:**

### What's Logged
- **SUMMARY.md** - Executive overview with decisions
- **FULL_LOG.md** - Complete (redacted) conversation
- **DECISIONS.md** - Key decisions with rationale
- **COMMITS.md** - All git commits with context
- **METRICS.md** - Framework adherence stats
- **LESSONS.md** - Process improvements

### For Each Session
- Date, duration, agent (AGT-002)
- SOP compliance percentage
- Deviations documented
- Blockers and resolutions
- Next actions

### Access
- [Session Index](80-Sessions/INDEX.md) - All sessions
- [Latest Session](80-Sessions/2026-02/2026-02-11_project-initialization/) - Today

### Redaction Rules
- ✅ API keys → `[REDACTED-API-KEY]`
- ✅ Passwords → `[REDACTED-PASSWORD]`
- ✅ Personal paths → `[REDACTED-PATH]`
- ✅ Keep: File structures, commands, decisions

**Purpose:** Audit trail, v3 planning, knowledge base, onboarding material

---

## 🚀 MARS: Multi-Agent RAG System

> **Path A: Full Autonomous Agent Coordination**

### What is MARS?

**MARS = Multi-Agent RAG System** - Agents don't just work; they critique each other, learn from mistakes, and self-improve.

### Path B (Current) vs Path A (MARS)

| Feature | Path B (Lightweight) | Path A (Full MARS) |
|---------|---------------------|---------------------|
| **Coordination** | PM-Agent routes manually | Agents self-organize |
| **Critique** | Post-review by humans | Agent-to-agent critique loops |
| **Learning** | Manual SOP updates | Self-improving from critiques |
| **Memory** | Session logs + handoffs | Persistent shared context |
| **Autonomy** | Human approves each step | Auto-approve within thresholds |

### Current Status: Path B Active

We are currently on **Path B** with:
- ✅ 14 Active Agents (C-Suite + Operations + Specialists)
- ✅ Discord-based coordination
- ✅ Codebase-aware agents (Phase 2 complete)
- ✅ Structured handoffs
- ✅ Session logging

### Path A Roadmap

**Phase 1: Memory Infrastructure** (Week 1)
- Deploy ChromaDB + Redis for persistent memory
- Build RAG integration for context retrieval
- Create memory schemas for agent learning

**Phase 2: Critique Engine** (Week 1-2)
- Agent-to-agent critique loops
- Automated quality scoring
- MARS Score: 0.0-1.0 (0.9+ = production ready)

**Phase 3: Autonomous Orchestration** (Week 2)
- Self-coordination without human routing
- Parallel task execution
- Dependency mapping

**Phase 4: Self-Improvement** (Week 2-3)
- Agents learn from critiques
- Automatic SOP updates
- Pattern recognition

**Phase 5: Full Integration** (Week 3)
- Everything works autonomously
- Minimal human touchpoints
- 5-10x speed improvement

### MARS Agent Ecosystem

```
┌───────────────────────────────────────────────────────────────────────┐
│                    MARS ORCHESTRATION                                  │
├───────────────────────────────────────────────────────────────────────┤
│  C-SUITE (Strategic Decision-Making)                                  │
│  ├─ AGT-000: CEO           │ Strategic vision, final authority        │
│  ├─ AGT-006: Chief of Staff│ Operations, coordination, escalation     │
│  └─ AGT-011: Strategist    │ Efficiency optimization, cost analysis   │
├───────────────────────────────────────────────────────────────────────┤
│  OPERATIONS (Core Execution)                                           │
│  ├─ AGT-001: Molt          │ Content, Users, Operations              │
│  ├─ AGT-002: OpenCode      │ Code, Infrastructure, Database         │
│  ├─ AGT-003: Guardian      │ Security, Quality, Compliance           │
│  ├─ AGT-005: Historian     │ Documentation, Knowledge, Sessions       │
│  ├─ AGT-007: Documenter    │ Docs sync, README updates, output fmt   │
│  └─ AGT-013: Consultant    │ Gap analysis, risk assessment           │
├───────────────────────────────────────────────────────────────────────┤
│  SPECIALISTS (Domain Experts)                                          │
│  ├─ AGT-014: n8n Expert    │ Workflow automation, triggers           │
│  ├─ AGT-015: Prefect Expert│ Orchestration, flows, retries            │
│  ├─ AGT-004: Stakeholder   │ External comms, user advocacy           │
│  ├─ AGT-012: Memory Keeper │ RAG, context, vector store              │
│  └─ AGT-016: Vibe Monitor  │ Pattern detection, anomalies            │
└───────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────────────────────────┐
│                    MARS ORCHESTRATION                    │
├─────────────────────────────────────────────────────────┤
│  AGT-001: Molt         │ Content, Users, Operations     │
│  AGT-002: OpenCode     │ Code, Infrastructure          │
│  AGT-003: Guardian     │ Security, Quality (Planned)   │
│  AGT-004: Technician   │ DevOps, Monitoring (Planned)  │
│  AGT-005: Historian    │ Documentation, Knowledge      │
│  AGT-006: PM-Agent     │ Coordination (Path B only)    │
│  AGT-007: Analyst      │ Metrics, Cost (Planned)       │
│  AGT-008: BizDev       │ Business, Finance             │
│  AGT-009: Creative     │ Creative, Prompt Engineering  │
│  AGT-010: CodeSentinel │ Codebase change tracking      │
└─────────────────────────────────────────────────────────┘
```

### Agent Interaction Patterns

**Pattern 1: Direct Handoff**
```
Molt: "Need API endpoint for song search"
       ↓
OpenCode: "Building /api/songs/search"
           ↓
Molt: "Thanks, implementing on my side"
```

**Pattern 2: Parallel Work**
```
OpenCode: Building feature
Historian: Documenting feature (parallel)
           ↓
Both: Sync via #🔗-handoffs channel
```

**Pattern 3: Critique Loop (Path A)**
```
OpenCode: Creates PR
           ↓
Guardian: Auto-review (critique engine)
           ↓
OpenCode: Addresses critiques
           ↓
Guardian: Approves (MARS Score 0.95)
           ↓
Merged
```

### Self-Improvement Workflow (Path A)

```
1. Agent Action → 2. Outcome Tracking → 3. Pattern Analysis
                                              ↓
4. Memory Store ← 6. Apply Changes ← 5. Decision
```

**Learning Mechanisms:**
- **Pattern Learning:** From repeated critiques
- **Error Learning:** From failures
- **Context Learning:** New patterns → memory store
- **Efficiency Learning:** Optimize token usage
- **Critique Learning:** Adjust behavior from feedback

### MARS Success Metrics

| Metric | Target |
|--------|--------|
| Context restoration | 2 min (from 30 min) |
| Parallel work | 80% (from 40%) |
| Human touchpoints | 1 per task (from 5+) |
| MARS Score average | 0.85+ |
| Self-improvement events | 10+ per week |

---

## 🔄 Decision Matrix

**I (OpenCode) handle:**
- ✅ Writing new features
- ✅ Bug fixes & debugging
- ✅ Database schema changes
- ✅ Infrastructure (Docker, K8s)
- ✅ Security implementation
- ✅ Code reviews

**I escalate to Molt (AGT-001):**
- ➡️ Content processing
- ➡️ User support
- ➡️ Cost optimization
- ➡️ Feature prioritization

**I consult Guardian (AGT-003):**
- 🔒 Security architecture
- 🔒 Security incidents

---

## 🐛 Common Issues

**Pre-commit failing?**
```bash
# Bypass ONLY if emergency (not recommended)
git commit --no-verify

# Better: Fix the issues first
black backend/src
ruff check --fix backend/src
```

**Need to track tasks?**
- Check the [Kanban Board](90-Project-Board/README.md) for current status
- Update task status when starting/completing work
- Link commits to tasks when possible

**Type checking errors?**
```bash
# Check specific file
mypy backend/src/specific_file.py

# Check with verbose output
mypy backend/src --show-error-codes
```

**Test failing?**
```bash
# Run specific test
pytest backend/tests/unit/test_file.py::test_function -v

# Run with debug output
pytest backend/tests -v --tb=long
```

---

## 📞 Escalation

**When to escalate to humans:**
- Data loss potential
- Security breach
- Financial impact > $100
- System downtime > 10 minutes
- Novel failure not in SOPs
- Unclear requirements

**How to escalate:**
1. Document in `DEVIATIONS.md`
2. Mention in commit message: `ESCALATION: See DEVIATIONS.md`
3. Notify human team lead

---

## ✨ Success Metrics

**Target KPIs:**
- Feature delivery: < 1 week
- Bug resolution: < 4 hours
- Test coverage: > 80%
- Deployment success: > 98%
- SOP adherence: 100%

---

## 🤖 Model Routing Protocol

### The Architect & The Builder Strategy

This dual-model approach optimizes for both **reasoning depth** and **execution cost**:

| Phase | Model | Throughput | Cost/M Input | Best For |
|-------|-------|------------|--------------|----------|
| **Plan (Architect)** | MiniMax M2.1 | 27.0 tok/s | $0.27 | Logic depth, architectural analysis, cross-file dependency mapping |
| **Build (Builder)** | Qwen3 Coder Next | 78.0 tok/s | $0.07 | High-speed execution, bulk file writes, documentation sync |
| **Audit (Reviewer)** | Qwen3 Coder Next | 78.0 tok/s | $0.07 | Final reconciliation, cross-file validation, changelog updates |

### When to Use Each Model

**MiniMax M2.1 (Architect Mode):**
- Cross-file refactoring requiring dependency analysis
- Architecture redesign or schema changes
- Complex feature design with multiple components
- Tasks where logic errors would be costly to fix later

**Qwen3 Coder Next (Builder Mode):**
- Direct implementation of well-defined tasks
- Bulk file writes and modifications
- Documentation updates and synchronization
- Final audit and reconciliation tasks

### Cost Optimization

Using MiniMax for planning + Qwen for execution is **~4x cheaper** than using MiniMax for both phases:

| Workflow | Total Cost (per session) | Use Case |
|----------|--------------------------|----------|
| MiniMax → Qwen | $0.27 (plan) + $0.07 (build) | Refactoring, architecture changes |
| Qwen direct | $0.07 | Simple bugs, documentation, small features |
| MiniMax only | $0.27+ | Quick planning queries only |

### Workflow Templates

**Template A: Refactoring/Cross-File Changes**
```
1. MiniMax M2.1: Analyze dependencies → Create "Refactor Manifest"
2. Human: Review manifest
3. Qwen3 Coder Next: Execute changes → Update docs → Final audit
```

**Template B: Quick Build**
```
1. Qwen3 Coder Next: Direct implementation
2. Qwen3 Coder Next: Self-audit (verify documentation sync)
```

### Model Selection Quick Reference

| Task Type | Recommended Model | Rationale |
|-----------|-------------------|-----------|
| Refactoring >3 files | MiniMax → Qwen | Avoid logic errors in complex changes |
| Database schema change | MiniMax → Qwen | Migration safety critical |
| New feature (complex) | MiniMax → Qwen | Design first, build second |
| Simple bug fix | Qwen direct | Low risk, fast execution |
| Documentation update | Qwen direct | High throughput, low cost |
| Performance tuning | MiniMax (analysis) → Qwen | Identify bottlenecks first |

---

*"Build it right. Build it once. Build it to scale."*
