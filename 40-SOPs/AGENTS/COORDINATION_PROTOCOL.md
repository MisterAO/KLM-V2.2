# 🤝 Agent Coordination Protocol

> **Lightweight communication standard for AI agent coordination  
> **Version:** 1.0.0  
> **Status:** ACTIVE  
> **Last Updated:** 2026-02-11

---

## 🎯 Purpose

This protocol defines how AI agents communicate and coordinate to prevent fragmentation and maintain coherence across the KLM V2 ecosystem.

---

## 📡 Communication Channels

### 1. Shared State (Primary)

**Location:** `90-Project-Board/SPRINT_TRACKER.md`

All agents read/write to Sprint Tracker as single source of truth.

### 2. Session Logs (Secondary)

**Location:** `80-Sessions/`

Agents document work in their session folders. All agents can reference.

### 3. Direct Messages (Urgent)

**Format:** `[AGENT] → [RECEIVER]: [message]`

Used for urgent coordination or handoffs.

---

## 📋 Message Standards

### Message Format

```
[FROM_AGENT] → [TO_AGENT]: [CONTEXT] | [REQUEST/STATUS] | [DEADLINE]
```

### Message Types

| Type | Example | Priority |
|------|---------|----------|
| **Delegation** | PM → OPENCODE: New feature | High |
| **Completion** | OPENCODE → PM: Task done | Normal |
| **Handoff** | OPENCODE → HISTORIAN: Docs needed | Normal |
| **Blocker** | ANY → PM: Blocked by X | High |
| **Alert** | PM → ALL: Fragmentation detected | High |

### Message Examples

```markdown
# Delegation
OPENCODE → PM-AGENT: Feature request received | API endpoint for lyrics export | Friday

# Completion
HISTORIAN → PM-AGENT: Documentation updated | FAQ section complete | N/A

# Handoff
MOLT → OPENCODE: Content processed | 10 lyrics ready for Gemini | ASAP

# Blocker
OPENCODE → PM-AGENT: Docker not running | Cannot start Supabase | Blocked

# Alert
PM-AGENT → ALL: Fragmentation detected | API work + Docs work overlapping | Review
```

---

## 🔄 Coordination Checkpoints

### Daily Standup (Start of Session)

**Who:** PM-Agent initiates  
**When:** Every session start  
**Purpose:** Align daily priorities

**Format:**
```markdown
## Daily Standup: YYYY-MM-DD

**OPENCODE:**
- Yesterday: [completed]
- Today: [planned]
- Blockers: [none/listed]

**MOLT:**
- Yesterday: [completed]
- Today: [planned]
- Blockers: [none/listed]

**HISTORIAN:**
- Yesterday: [completed]
- Today: [planned]
- Blockers: [none/listed]

**Coordination Notes:**
- [Cross-agent dependencies]
- [Fragmentation risks]
```

### Session End (End of Session)

**Who:** All agents  
**When:** Every session end  
**Purpose:** Log completion, report status

**Format:**
```markdown
## Session End Report

**Agent:** [NAME]
**Session:** [ID]
**Duration:** [X hours]

**Completed:**
- [Task 1]
- [Task 2]

**Session Files:**
- [x] SUMMARY.md
- [x] FULL_LOG.md
- [x] DECISIONS.md
- [x] COMMITS.md
- [x] METRICS.md

**Delegation Needed:**
- [Task 1] → [Agent]
- [Task 2] → [Agent]

**Blockers:**
- [None / Listed]
```

### Handoff (Task Transition)

**Who:** Transferring agent
**When:** Task requires another agent
**Purpose:** Transfer context

**Format:**
```markdown
## Handoff: [TASK NAME]

**From:** [AGENT]
**To:** [AGENT]
**Date:** YYYY-MM-DD

### Context
[What was done - 2-3 sentences]

### Remaining Work
- [ ] Task 1
- [ ] Task 2

### Critical Information
1. [Key detail 1]
2. [Key detail 2]

### Dependencies
- [None / List dependencies]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Test Instructions
```bash
[Commands to verify completion]
```
```

### Quick Handoff (For Simple Tasks)

```markdown
## Quick Handoff

**From:** OPENCODE → HISTORIAN
**Task:** Document new API endpoint
**Status:** Code complete, needs docs
**Location:** `backend/src/api/songs.py`
**Notes:** Follow existing patterns in API_DOCUMENTATION.md
```

### Blocker Escalation (Issue Detection)

**Who:** Any agent  
**When:** Blocked > 15 minutes  
**Purpose:** Resolve blockers

**Format:**
```markdown
## Blocker Escalation

**Agent:** [NAME]
**Task:** [Task ID/Name]
**Blocked Since:** [Time]

**Issue:**
[Description of blocker]

**Tried:**
- [Solution 1 - failed]
- [Solution 2 - failed]

**Recommended Resolution:**
[What should happen next]

**Escalated To:** PM-Agent
```

---

## ⚠️ Fragmentation Detection

### Fragmentation Signs

| Sign | Example |
|------|---------|
| **Related tasks, different agents** | OPENCODE building API + HISTORIAN documenting API |
| **Duplicate work** | Two agents solving same problem |
| **Context gaps** | Information not shared between agents |
| **Drift** | Docs don't match code, code doesn't match docs |

### Fragmentation Response

1. **PM-Agent detects** via Sprint Tracker review
2. **Alert sent** to affected agents
3. **Consolidation decision:**
   - Merge into single task
   - Coordinate parallel work
   - Accept if truly independent
4. **Prevent future** via dependencies

---

## 📊 Coordination Metrics

| Metric | Target | Measure |
|--------|--------|---------|
| **Cross-Agent Awareness** | 100% | All agents know what others doing |
| **Fragmentation Incidents** | <1/week | Count per week |
| **Handoff Success Rate** | 100% | No context lost |
| **Blocker Resolution Time** | <4 hours | Time to unblock |
| **Session Compliance** | 100% | All files completed |

---

## 🎯 Agent Responsibilities

### PM-Agent (Coordinator)
- Initiate daily standups
- Detect fragmentation
- Route delegations
- Track all tasks
- Report to human

### OpenCode (Engineer)
- Report session completion
- Flag fragmentation risks
- Request docs handoffs
- Escalate blockers

### Molt (Content)
- Report content processing status
- Request code/infrastructure support
- Coordinate with Historian on docs
- Escalate blockers

### Historian (Docs)
- Document all decisions
- Review session logs
- Update knowledge base
- Flag documentation drift

---

## 🔗 Integration with PM-Agent SOP

This protocol works with PM-Agent workflows:

| Workflow | Protocol Element |
|----------|-----------------|
| Delegation | Message: Delegation |
| Fragmentation Prevention | Checkpoints + Detection |
| Session Logging | Session End report |
| Refactoring | Fragmentation detection |
| Daily Coordination | Daily standup |

---

## 📝 Quick Reference

### Message Cheat Sheet

```markdown
# Ask PM-Agent for delegation
→ PM-AGENT: [context] | Need task assigned | [deadline]

# Tell PM-Agent task done
→ PM-AGENT: [task] | Complete | N/A

# Handoff to another agent
→ [AGENT]: [context] | Please continue | [details]

# Report blocker
→ PM-AGENT: [task] | Blocked by [issue] | [tried solutions]

# Alert of fragmentation
→ PM-AGENT: [issue] | Fragmentation detected | [agents involved]
```

### Escalation Path

```
AGENT BLOCKED
     │
     ▼
  PM-AGENT
     │
├────┴────┐
│         │
Resolve  Escalate
     │     │
     ▼     ▼
  FIX   HUMAN
```

---

*Part of PM-Agent (AGT-006) Chief of Staff operations*
