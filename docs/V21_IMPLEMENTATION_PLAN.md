# V2.1 Implementation Plan: Balanced Self-Healing + Self-Improvement

## Executive Summary

**Goal:** Create an agent ecosystem that operates autonomously with minimal human intervention, learns from every interaction, and continuously improves.

**Key Systems:**
- **Lightning Code Index (LCI)**: Semantic code understanding for all AI tools
- **MARS**: Persistent memory, orchestration, and self-improvement
- **Integration**: Unified context that enables both self-healing and learning

**Timeline:** 4 weeks
**Effort:** ~20 hours of implementation
**Outcome:** Agents that understand code, remember lessons, fix issues, and improve over time

---

## Phase 1: Foundation (Week 1) - IN PROGRESS

**Theme:** Install infrastructure that enables both self-healing and self-improvement

### 1.1 Code Index Installation (COMPLETED with Alternative)

**Package Used:** `@standardbeagle/lci` v0.4.0  
**Reason:** `@modelcontextprotocol/server-code-index` does not exist

**Installation:**
```bash
npm init -y
npm install @standardbeagle/lci --save-dev
```

**Commands Available:**
```bash
npm run code:index     # Run initial indexing
npm run code:watch     # Watch for changes
npm run code:status    # Check index status
```

**Direct Commands:**
```bash
lci search <query>     # Semantic code search
lci grep <pattern>     # Fast text search
lci def <symbol>       # Find symbol definition
lci refs <symbol>      # Find symbol references
lci tree <function>    # Call hierarchy
lci mcp                # Start MCP server
lci server             # Start persistent server
lci status             # Index status
```

### 1.2 Configuration (IN PROGRESS)

**File:** `.lci.kdl`

**Structure:**
```kdl
[index]
include = [
    "**/*.py",
    "**/*.md",
    "**/*.sql",
    "AGENTS.md",
    "docs/**/*.md",
    "40-SOPs/**/*.md",
    "90-Project-Board/**/*.md",
    "80-Sessions/**/*.md",
    "backend/**/*.py",
    "migrations/**/*.sql"
]
exclude = [
    "node_modules/**",
    ".git/**",
    "__pycache__/**",
    "*.pyc",
    "assets/**",
    "export_chat/**",
    "80-Sessions/**/*-export.md"
]

[embedding]
model = "all-MiniLM-L6-v2"
chunkSize = 2000
overlap = 200

[mcp]
transport = "stdio"
tools = ["search", "find_symbol", "get_context", "list_files"]
```

### 1.3 OpenCode MCP Configuration (PENDING)

**File:** `.opencode/mcp_config.json`

**Structure:**
```json
{
  "version": "1.0",
  "servers": {
    "lci": {
      "command": "npx",
      "args": ["lci", "mcp"],
      "transport": "stdio",
      "enabled": true
    }
  },
  "defaultTools": {
    "lci": ["search", "find_symbol", "get_context", "list_files"]
  }
}
```

### 1.4 MARS-MCP Bridge Architecture (PENDING)

**Purpose:** Unified context API for MARS agents

**Structure:**
```
backend/src/mars/integrations/
├── mcp_client.py          # LCI MCP client wrapper
├── unified_context.py     # Unified context API
└── __init__.py
```

---

## Phase 2: Self-Healing Enhancement (Week 2)

**Theme:** Tests fail → Agents fix with code understanding + historical context

### 2.1 Enhanced Guardian Loop with LCI

**File:** `backend/src/mars/guardian_loop.py`

**Enhancements:**
- Query LCI for similar code patterns
- Cross-reference with MARS memory
- Generate context-aware fixes

### 2.2 Self-Healing Workflow Integration

**File:** `backend/src/mars/self_healing/pipeline.py`

**Process:**
1. Error detected → LCI query for similar patterns
2. MARS memory for historical fixes
3. Guardian generates fix candidates
4. Sandbox validates fix
5. Success → Index fixed code
6. Failure → Escalate + learn

### 2.3 Self-Healing SOP

**Document:** `40-SOPs/Phase-2-God-Tier/SELF_HEALING.md`

---

## Phase 3: Self-Improvement Engine (Week 3)

**Theme:** Agents learn from critiques, prompts improve over time

### 3.1 Prompt Improvement System

**Files:**
- `backend/src/mars/self_improvement/prompt_analyzer.py`
- `backend/src/mars/self_improvement/prompt_optimizer.py`

**Process:**
1. Analyze prompt success rates
2. Query LCI for best practices
3. Generate optimized prompts
4. Apply improvements

### 3.2 Learning from Critiques Loop

**File:** `backend/src/mars/self_improvement/critique_learning.py`

**Process:**
1. Guardian critique recorded
2. LCI extracts pattern
3. MARS stores learning
4. Prompts updated

### 3.3 MARS Score Tracking

**File:** `backend/src/mars/self_improvement/metrics.py`

**Metrics:**
- Success rates over time
- Self-healing success rate
- Prompt optimization impact
- Autonomy level progression

---

## Phase 4: V3 Intelligence (Week 4+)

**Theme:** Accumulated memory enables true autonomy

### 4.1 Memory Accumulation Strategy

| Memory Type | Storage | Duration |
|-------------|---------|----------|
| Working | Redis | Current session |
| Short-Term | Supabase | 7 days |
| Long-Term | Supabase + ChromaDB | 30+ days |
| Episodic | Supabase | Major events |

### 4.2 Agent Autonomy Levels

| Level | Description | Human Intervention |
|-------|-------------|-------------------|
| L1 | Follows prompts exactly | Daily review |
| L2 | Makes decisions with context | Weekly review |
| L3 | Self-heals independently | Monthly review |
| L4 | Self-improves autonomously | Quarterly review |
| L5 | Fully autonomous | Annual review |

**Target:** All agents reach L3 by Week 4, L4 by Month 2

### 4.3 V3 Success Criteria

| Criteria | Target | Measurement |
|----------|--------|-------------|
| Self-Healing Rate | >80% | Healed / Total failures |
| Prompt Improvement | >10% | Success rate improvement |
| Code Quality Score | >0.9 | Average MARS score |
| Human Intervention | <5% | Escalated / Total tasks |
| Memory Utilization | >70% | Memory accessed / total |

---

## Integration Points

### System Connections

| From | To | Purpose |
|------|-----|---------|
| LCI | MARS MCP Bridge | Code understanding |
| MCP Bridge | Self-Healing | Context-aware fixes |
| Self-Healing | MARS Memory | Store lessons learned |
| MARS Memory | Prompt Optimizer | Improve prompts |
| Prompt Optimizer | Agents | Better performance |
| Agents | LCI | Index new code |
| Agents | MARS Memory | Store decisions |

### Data Flow

```
Week 1: LCI indexes codebase
   → MCP Bridge available
   
Week 2: Agents use MCP Bridge for decisions
   → Self-Healing active
   
Week 3: First self-healing events
   → Lessons stored in MARS Memory
   
Week 4+: Full V3 intelligence
   → Minimal human intervention needed
```

---

## Key Deliverables by Week

| Week | Deliverables | Tests |
|------|--------------|-------|
| 1 | LCI installed, MCP configured, Bridge started | Agents can query LCI |
| 2 | Enhanced Guardian, Self-Healing Pipeline | Fixes generate with context |
| 3 | Prompt Analyzer, Prompt Optimizer | Prompts improve over time |
| 4+ | Metrics Dashboard, Autonomy levels | Agents reach L3 |

---

## Rollback Plan

If any component causes issues:

1. **LCI issues:** Disable in `.opencode/mcp_config.json`
2. **MCP Bridge:** Comment out imports in MARS modules
3. **Self-Healing:** Disable in configuration
4. **Prompt Optimization:** Revert to original prompts

---

## Documentation Updates Required

| Document | Update |
|----------|--------|
| `AGENTS.md` | Add LCI tools section |
| `40-SOPs/AGENTS/AGENT-OPENCODE.md` | Add self-healing process |
| `60-Resources/PLAYBOOK/04-COMMANDS.md` | Add LCI commands |
| `DEVIATIONS.md` | Document package change |

---

## Session History

| Session | Date | Focus | Status |
|---------|------|-------|--------|
| SES-20260212-001 | 2026-02-12 | Week 1 Foundation | IN PROGRESS |

---

## Notes for Future Sessions

1. `@modelcontextprotocol/server-code-index` does not exist - use `@standardbeagle/lci`
2. LCI provides full MCP stdio transport support
3. KDL configuration format is straightforward
4. All required MCP tools are available
5. Installation was seamless (1 package, 0 vulnerabilities)

---

**Document Version:** 1.1  
**Last Updated:** 2026-02-12  
**Next Review:** After Week 1 completion