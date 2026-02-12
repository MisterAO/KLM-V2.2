# MARS Coordination Protocol

> **Multi-Agent RAG System - Coordination Standards**  
> **Version:** 1.0.0  
> **Last Updated:** 2026-02-11  
> **Status:** DRAFT (Path A Implementation)

---

## 🎯 Purpose

This document defines how agents coordinate in the **MARS (Multi-Agent RAG System)** ecosystem, enabling:
- Autonomous agent-to-agent communication
- Self-organizing task execution
- Critique loops for quality assurance
- Memory persistence across sessions

---

## 🏗️ MARS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MARS ORCHESTRATION LAYER                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   MEMORY     │◄──►│   CRITIQUE    │◄──►│  EXECUTION   │  │
│  │   STORE      │    │    ENGINE     │    │   ENGINE     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AGENT SWARM (9 Agents)                  │   │
│  │  Molt │ OpenCode │ Guardian │ Historian │ PM-Agent │   │
│  │  Technician │ Analyst │ BizDev │ Creative           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Registry

| ID | Name | Role | Status | MARS Ready |
|----|------|------|--------|------------|
| AGT-001 | Molt | Production Manager | ACTIVE | ✅ Phase 2 |
| AGT-002 | OpenCode | Lead Engineer | ACTIVE | ✅ Phase 2 |
| AGT-003 | Guardian | Security/Quality | PLANNED | ⏳ Path A |
| AGT-004 | Technician | DevOps/Infra | PLANNED | ⏳ Path A |
| AGT-005 | Historian | Documentation | ACTIVE | ✅ Phase 2 |
| AGT-006 | PM-Agent | Chief of Staff | ACTIVE | ✅ Path B |
| AGT-007 | Analyst | Metrics/Cost | PLANNED | ⏳ Path A |
| AGT-008 | BizDev | Business/Finance | ACTIVE | ✅ Phase 2 |
| AGT-009 | Creative | Creative/Prompt | ACTIVE | ✅ Phase 2 |

**Legend:**
- ✅ Ready for MARS
- ⏳ Planned for Path A
- 🚧 In development

---

## 📋 Coordination Patterns

### Pattern 1: Direct Handoff (Path B & A)

**Use When:** One agent needs another's expertise

```
Agent A: "[HANDOFF] Need help with [task]"
          ↓
Agent B: "[ACK] Taking over [task]"
          ↓
Agent B: "[COMPLETE] [Deliverable]"
          ↓
Agent A: "[RESUME] Continuing with [context]"
```

**Example:**
```
Molt: "[HANDOFF] Need API for song upload @opencode"
       ↓
OpenCode: "[ACK] Building POST /api/songs/upload"
       ↓
OpenCode: "[COMPLETE] Endpoint ready: backend/src/api/songs.py:89"
       ↓
Molt: "[RESUME] Integrating upload into content pipeline"
```

### Pattern 2: Parallel Execution (Path A)

**Use When:** Tasks can be worked simultaneously

```
Orchestrator: "[PARALLEL] Tasks: [A], [B], [C]"
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 Agent A   Agent B   Agent C
    │         │         │
    └─────────┼─────────┘
              ▼
Orchestrator: "[MERGE] All tasks complete"
```

**Example:**
```
Orchestrator: "[PARALLEL] Feature X development"
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
OpenCode   Historian  Guardian
(Code)     (Docs)     (Review)
    │         │         │
    └─────────┼─────────┘
              ▼
Orchestrator: "[MERGE] Feature X ready for deploy"
```

### Pattern 3: Critique Loop (Path A)

**Use When:** Quality assurance is needed

```
Agent: Creates artifact
       ↓
Critic: Reviews against criteria
       ↓
       ┌─────────┐
       │ Pass?   │
       └────┬────┘
    ┌──────┼──────┐
    ▼      ▼      ▼
  YES    REVISE   REJECT
    │      │       │
    ▼      ▼       ▼
Store  Iterate  Escalate
```

**MARS Score Thresholds:**
- **0.0-0.5:** REJECT - Critical issues
- **0.5-0.7:** REVISE - Major issues
- **0.7-0.9:** ACCEPT - Minor issues
- **0.9-1.0:** APPROVE - Production ready

---

## 🧠 Memory Management

### Memory Types

| Type | Storage | Purpose | Retention |
|------|---------|---------|-----------|
| **Working** | Redis | Current task state | Session |
| **Short-term** | PostgreSQL | Recent decisions | 30 days |
| **Long-term** | ChromaDB | Project knowledge | Permanent |
| **Episodic** | File/Markdown | Session logs | Permanent |

### Memory Schema

```yaml
memory_store:
  agents:
    [agent_id]:
      working_memory: {}      # Current context
      decisions: []           # Decision history
      critiques_received: []  # Feedback history
      patterns: []            # Learned patterns
      
  system:
    project_context: {}       # RAG source
    architecture_decisions: []
    sop_versions: {}
    
  sessions:
    [session_id]:
      summary: ""
      decisions: []
      artifacts: []
      
  critiques:
    [artifact_id]:
      history: []
      improvement_log: []
```

### Memory Retrieval

**Before any agent action:**
1. Query working memory for current context
2. Retrieve relevant long-term memories
3. Check for similar past decisions
4. Load applicable SOPs

**Prompt Template:**
```
System: "Before responding, retrieve context from:
  1. Working memory: [current_task]
  2. Similar decisions: [past_similar]
  3. Project architecture: [relevant_docs]
  4. Agent history: [agent_patterns]"
```

---

## 🔄 Self-Improvement Loop

### Learning Mechanisms

| Mechanism | Trigger | Action |
|-----------|---------|--------|
| **Pattern Learning** | Repeated critiques | Update best practices |
| **Error Learning** | Failures | Add to "what not to do" |
| **Context Learning** | New patterns | Expand memory store |
| **Efficiency Learning** | Token usage | Optimize prompts |
| **Critique Learning** | Feedback received | Adjust behavior |

### Improvement Workflow

```
1. Agent performs action
         ↓
2. Track outcome (success/failure)
         ↓
3. Calculate metrics (time, quality, cost)
         ↓
4. Pattern analysis
   - What worked?
   - What failed?
   - What could improve?
         ↓
5. Decision
   ├── Update prompt template
   ├── Update memory store
   ├── Update SOP (if significant)
   └── Flag for human review (if major)
         ↓
6. Apply changes
   - Next action uses improved approach
   - Memory persists for future sessions
```

---

## 📊 MARS Metrics

### Agent Performance KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task Completion Rate | > 95% | % completed without escalation |
| MARS Score Average | > 0.85 | Quality threshold |
| Context Restoration | < 2 min | Time to resume session |
| Parallel Work % | > 80% | Tasks done in parallel |
| Human Touchpoints | < 1/task | Manual interventions |
| Self-Improvement Events | > 10/week | Learning occurrences |

### Success Tracking

**Daily:**
- Tasks completed per agent
- MARS scores
- Critique iterations

**Weekly:**
- Pattern analysis
- SOP update suggestions
- Performance trends

**Monthly:**
- Agent capability review
- MARS effectiveness
- Path A roadmap progress

---

## 🚀 Implementation Status

### Phase 1: Memory Infrastructure ⏳
- [ ] Deploy ChromaDB
- [ ] Deploy Redis
- [ ] Create memory schemas
- [ ] Build RAG integration

### Phase 2: Critique Engine ⏳
- [ ] Define critique criteria
- [ ] Build scoring algorithm
- [ ] Create critique loops
- [ ] Test with real artifacts

### Phase 3: Autonomous Orchestration ⏳
- [ ] Task parser
- [ ] Dependency mapper
- [ ] Agent matcher
- [ ] Orchestrator engine

### Phase 4: Self-Improvement ⏳
- [ ] Outcome tracking
- [ ] Pattern analysis
- [ ] Learning mechanisms
- [ ] SOP auto-update

### Phase 5: Full Integration ⏳
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] V3 readiness

---

## 📞 Coordination Commands

### Discord Commands (Path B)

```
!opencode [task]     - Delegate to OpenCode
!molt [task]         - Delegate to Molt
!creative [task]     - Delegate to Creative
!bizdev [task]       - Delegate to BizDev
!historian [task]    - Delegate to Historian
!agents              - List all agents
!status              - Show agent status
!eco                 - Switch to fast mode
!premium             - Switch to best quality
```

### MARS Commands (Path A - Future)

```
@mars [goal]         - MARS interprets and routes
@mars critique [id]  - Request critique
@mars parallel [tasks] - Execute in parallel
@mars status         - Show MARS metrics
```

---

## 🔗 Quick References

### Agent SOPs
- [AGT-001: Molt](./AGENT-MOLT.md)
- [AGT-002: OpenCode](./AGENT-OPENCODE.md)
- [AGT-005: Historian](./AGENT-HISTORIAN.md)
- [AGT-008: BizDev](./AGENT-BIZDEV.md)
- [AGT-009: Creative](./AGENT-CREATIVE.md)

### Related Documents
- [AGENT_REGISTRY.md](../AGENT_REGISTRY.md) - Full agent catalog
- [COORDINATION_PROTOCOL.md](./COORDINATION_PROTOCOL.md) - Basic coordination
- [PATH_A_FULL_MARS_ROADMAP.md](../../60-Resources/PLAYBOOK/PATH_A_FULL_MARS_ROADMAP.md) - Implementation plan
- [AGENTS.md](../../AGENTS.md) - Agent operational guide

---

## 📝 Changelog

### v1.0.0 - 2026-02-11
- Initial MARS coordination protocol
- Defined agent interaction patterns
- Documented memory management
- Outlined self-improvement workflow
- Created implementation roadmap

---

**Next Review:** 2026-02-18  
**Owner:** OpenCode (AGT-002)  
**Path:** A - Full MARS

---

*"Agents that critique each other produce better results than agents working alone."*
