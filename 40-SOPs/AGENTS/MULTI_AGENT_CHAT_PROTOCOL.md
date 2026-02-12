# Multi-Agent Chat Protocol

> **Real-time agent coordination during chat sessions**
> **Version:** 1.9.0
> **Status:** ACTIVE
> **Last Updated:** 2026-02-11

---

## 📝 SOP Version Control

### Version Header Template

Every SOP must have this header:

```markdown
# [SOP Name]

> **Purpose:** [Brief description]
> **SOP ID:** [CATEGORY-NUMBER]
> **Version:** X.Y.Z
> **Classification:** [INTERNAL/PUBLIC/SENSITIVE]
> **Status:** [DRAFT/ACTIVE/DEPRECATED]
> **Last Updated:** YYYY-MM-DD
> **Review Cycle:** [Weekly/Monthly/Quarterly]
```

### Version Numbering

```
VERSION = MAJOR.MINOR.PATCH

MAJOR (X.0.0):
- Breaking changes to workflow
- New agent added
- Major structural changes

MINOR (X.Y.0):
- New workflow added
- New handoff type
- New trigger added
- Significant update to existing content

PATCH (X.Y.Z):
- Typo fixes
- Clarifications
- Minor formatting
- Link updates
```

### SOP ID System

| Category | ID Prefix | Examples |
|----------|-----------|----------|
| Agent SOPs | AGENT-[NAME] | AGENT-OPENCODE, AGENT-MOLT |
| Protocol | PROTOCOL-[NAME] | PROTOCOL-COORDINATION, PROTOCOL-CHAT |
| Workflow | WORKFLOW-[NAME] | WORKFLOW-ENDOFDAY |
| Technical | TECH-[NAME] | TECH-SECURITY, TECH-DATABASE |
| Diagram | DIAGRAM-[NAME] | DIAGRAM-AGENT-WORKFLOW |

### Version Control Workflow

```
┌─────────────────────────────────────────────────────────────┐
│               SOP VERSION CONTROL WORKFLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CREATE/EDIT SOP                                         │
│     → Update Version (MAJOR/MINOR/PATCH)                    │
│     → Update "Last Updated" date                           │
│     → Update "Status" (DRAFT → ACTIVE)                     │
│                                                             │
│  2. GIT TRACKING                                            │
│     → Create branch: docs/sop-[name]-vX.Y.Z                 │
│     → Commit: "sop: [name] vX.Y.Z - [changes]"             │
│     → PR for review                                        │
│                                                             │
│  3. DISTRIBUTION                                            │
│     → Merge to main when ACTIVE                            │
│     → Tag: vX.Y.Z                                          │
│     → Notify affected agents                                │
│                                                             │
│  4. DEPRECATION                                            │
│     → Status: DEPRECATED                                   │
│     → Add "Deprecated By:" [SOP ID]                         │
│     → Add "Replacement:" [New SOP ID]                       │
│     → Keep for 6 months for transition                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### SOP Changelog Format

Every SOP must include:

```markdown
---

## 🔄 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| X.Y.Z | YYYY-MM-DD | Agent | Description |
| X.Y.0 | YYYY-MM-DD | Agent | Description |
| 1.0.0 | YYYY-MM-DD | Agent | Initial creation |

---

## 📋 SOP Metadata

| Field | Value |
|-------|-------|
| **SOP ID** | PROTOCOL-CHAT |
| **Current Version** | 1.9.0 |
| **Status** | ACTIVE |
| **Review Cycle** | Monthly |
| **Last Reviewed** | 2026-02-11 |
| **Next Review** | 2026-03-11 |
| **Owner** | PM-Agent (AGT-006) |
| **Distribution** | All agents |

---

## ✅ SOP Compliance Checklist

- [ ] Version number updated
- [ ] Last Updated date current
- [ ] Changelog maintained
- [ ] Status is accurate
- [ ] All links working
- [ ] Cross-references verified
- [ ] Git branch created
- [ ] PR reviewed
- [ ] Agents notified
```

### When Creating New SOP

```markdown
# [SOP Name]

> **Purpose:** [2-3 sentences]
> **SOP ID:** [CATEGORY-NUMBER]
> **Version:** 1.0.0
> **Status:** DRAFT
> **Last Updated:** YYYY-MM-DD

---

## 🔄 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Agent] | Initial creation |

---

[CONTENT]

---

## 📋 SOP Metadata

| Field | Value |
|-------|-------|
| **SOP ID** | [CATEGORY-NUMBER] |
| **Current Version** | 1.0.0 |
| **Status** | DRAFT |
| **Review Cycle** | [Weekly/Monthly/Quarterly] |
| **Owner** | [Agent] |
| **Distribution** | [Who needs this] |

---

*Template created: YYYY-MM-DD*
```

### PM-Agent SOP Tracking

```markdown
## 📋 SOP Registry (Maintained by PM-Agent)

| SOP ID | Name | Version | Status | Last Updated | Owner |
|--------|------|---------|--------|--------------|-------|
| AGENT-OPENCODE | OpenCode SOP | 2.0.0 | ACTIVE | 2026-02-11 | OpenCode |
| AGENT-MOLT | Molt SOP | 2.0.0 | ACTIVE | 2026-02-11 | Molt |
| PROTOCOL-COORDINATION | Coordination Protocol | 1.0.0 | ACTIVE | 2026-02-11 | PM-Agent |
| PROTOCOL-CHAT | Chat Protocol | 1.9.0 | ACTIVE | 2026-02-11 | PM-Agent |
| DIAGRAM-WORKFLOW | Agent Workflow Visualization | 1.0.0 | ACTIVE | 2026-02-11 | PM-Agent |

**SOP Health:**
- Active: X
- Draft: Y
- Deprecated: Z
- Compliance: X%
```

### Git Commit Message Format

For SOP changes:

```
sop: [sop-id] vX.Y.Z - [brief description]

- Detailed changes (optional)
- [Agent]
```

Examples:
```
sop: PROTOCOL-CHAT v1.9.0 - added version control workflow
sop: AGENT-OPENCODE v2.1.0 - added end-of-day checklist
sop: DIAGRAM-WORKFLOW v1.0.0 - initial creation
```

### End-of-Day SOP Check

```markdown
## 📋 SOP Version Check

| SOP | Current Version | Latest Version | Needs Update? |
|-----|-----------------|----------------|---------------|
| [SOP] | X.Y.Z | X.Y.Z | ✅/❌ |

**Changes This Week:**
- [SOP] updated to vX.Y.Z
- [SOP] created at v1.0.0
- [SOP] deprecated (vX.Y.Z → DEPRECATED)
```

---

---

## 🎯 Purpose

Enable all active agents to:
1. **Listen in** on chat sessions
2. **Know their update responsibilities** at all times
3. **Communicate frequently** with clear handoffs
4. **Ensure documentation cohesion** across all systems
5. **Document learning series** for future developers

**Visual Guide:** [AGENT_WORKFLOW_VISUALIZATION.md](./../../20-Architecture/diagrams/agent-workflow/AGENT_WORKFLOW_VISUALIZATION.md) - Complete workflow diagrams and handoffs

---

## 📖 Learning Series Integration

**Every chat session builds the learning series for future developers:**

| Document | What We Capture | Why It Matters |
|----------|----------------|----------------|
| **PLAYBOOK** | Technical how-to guides | "How did they build this?" |
| **JOURNAL** | Development journey | "What was their process?" |
| **DECISION_LOG** | Rationale for choices | "Why did they choose X?" |
| **ROADBLOCKS** | Problems + solutions | "I have the same error!" |
| **TIPS_TRICKS** | Non-obvious insights | "I wish I knew this earlier" |

**PM-Agent ensures:** "As we chat, we document for future devs."

---

## 👥 Active Agents

| Agent | Role | Active | Listen In |
|-------|------|--------|-----------|
| **Molt** (AGT-001) | Production Manager | ✅ Yes | All sessions |
| **OpenCode** (AGT-002) | Lead Engineer | ✅ Yes | All sessions |
| **Historian** (AGT-005) | Documentation | ✅ Yes | All sessions |
| **PM-Agent** (AGT-006) | Chief of Staff | ✅ Yes | All sessions |

---

## 📡 Chat Session Participation

### Rule: All Agents Listen by Default

Every chat message is visible to ALL agents. No siloed communication.

### Participation Levels

| Message Type | Who Responds | Who Listens |
|-------------|--------------|-------------|
| **Code question** | OpenCode | All |
| **Content question** | Molt | All |
| **Documentation** | Historian | All |
| **Prioritization** | PM-Agent | All |
| **Coordination** | Any | All |

### Agent Presence Declaration

At session start, each agent declares presence:

```markdown
## Session Start - YYYY-MM-DD

**Agents Present:**
- ✅ **OpenCode** - Ready for code/infrastructure
- ✅ **Molt** - Ready for content/processing
- ✅ **Historian** - Ready for documentation
- ✅ **PM-Agent** - Ready for coordination

**Session Focus:** [[TOPIC]]
**Duration:** ~X hours
```

---

## 📋 Update Responsibilities Matrix

### Who Updates What

| Discovery/Event | Primary Agent | Secondary | Update Location |
|----------------|--------------|-----------|-----------------|
| New code pattern | OpenCode | Historian | `60-Resources/PLAYBOOK/` |
| New command/tool | Any agent | OpenCode | `60-Resources/PLAYBOOK/04-COMMANDS.md` |
| New insight/tip | Any agent | PM-Agent | `60-Resources/PLAYBOOK/07-TIPS_TRICKS.md` |
| Problem solved | Any agent | PM-Agent | `60-Resources/PLAYBOOK/03-ROADBLOCKS.md` |
| Architecture decision | OpenCode | PM-Agent | `60-Resources/PLAYBOOK/` |
| Documentation gap | Historian | Any | `70-Training/knowledge_base/` |
| Task completed | Owner agent | PM-Agent | `90-Project-Board/SPRINT_TRACKER.md` |
| New session logged | Owner agent | All | `80-Sessions/INDEX.md` |
| Blocker found | Any agent | PM-Agent | `60-Resources/PLAYBOOK/03-ROADBLOCKS.md` |
| Tech stack change | OpenCode | PM-Agent | `60-Resources/PLAYBOOK/` |

### Update Cadence

| Event | When to Update | Urgency |
|-------|----------------|---------|
| **Session decision** | Immediately | High |
| **New pattern discovered** | Within 30 min | Medium |
| **Task completion** | End of session | Low |
| **Blocker identified** | Immediately | High |
| **Tool discovery** | Within session | Medium |

---

## 📚 Documentation Cohesion Protocol

### The 6 Documentation Pillars

| Pillar | Location | Owner | Sync Frequency | PM-Agent Check |
|--------|----------|-------|-----------------|-----------------|
| **SOPs** | `40-SOPs/` | Agent who changes | On change | Daily |
| **Version Control** | `.git/` | OpenCode | Every commit | Daily |
| **Playbook** | `60-Resources/PLAYBOOK/` | OpenCode | Per session | Daily |
| **Journal** | `70-Training/journal/` | Human + Molt | Daily | Weekly |
| **Kanban** | `90-Project-Board/` | PM-Agent | Per task | Daily |
| **Dashboard** | `PROJECT_DASHBOARD.md` | PM-Agent | Weekly | Weekly |

### Documentation Sync Rules

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DOC SYNC DEPENDENCIES                             │
├─────────────────────┬───────────────────────────────────────────────┤
│ SOPs Change         │ → Update PLAYBOOK → Update INDEX.md          │
│                     │ → Update Kanban → Notify PM-Agent             │
├─────────────────────┼───────────────────────────────────────────────┤
│ Playbook Change     │ → Update SOPs if needed → Update INDEX.md    │
│                     │ → Update Kanban → Update Dashboard            │
├─────────────────────┼───────────────────────────────────────────────┤
│ Kanban Task Done    │ → Update Dashboard → Update Journal          │
│                     │ → Update Sprint Tracker → Update INDEX.md     │
├─────────────────────┼───────────────────────────────────────────────┤
│ Git Branch Created  │ → Update Kanban → Update Session Log         │
│                     │ → Update Dashboard → Update Sprint Tracker    │
├─────────────────────┼───────────────────────────────────────────────┤
│ Session Complete    │ → Update INDEX.md → Update Kanban            │
│                     │ → Update Dashboard → Update Journal          │
│                     │ → Update Playbook (if patterns)               │
└─────────────────────┴───────────────────────────────────────────────┘
```

### Documentation Ownership Matrix

| Document | Primary Owner | Secondary | Update Trigger |
|----------|--------------|-----------|----------------|
| `AGENTS.md` | PM-Agent | OpenCode | Agent changes |
| `AGENT_REGISTRY.md` | PM-Agent | OpenCode | Agent add/remove |
| `AGENT-*.md` SOPs | Agent Owner | PM-Agent | Workflow change |
| `PLAYBOOK/*.md` | OpenCode | PM-Agent | New pattern |
| `80-Sessions/*.md` | Session Owner | PM-Agent | Session complete |
| `90-Project-Board/*.md` | PM-Agent | Agent change |
| `PROJECT_DASHBOARD Owner | Task.md` | PM-Agent | OpenCode | Weekly |
| `70-Training/journal/*.md` | Human | Molt | Daily |
| `.git/` version tags | OpenCode | PM-Agent | Release |
| `DEVIATIONS.md` | PM-Agent | OpenCode | Any deviation |

### Cross-Reference Requirements

| Update | Must Also Update | Within |
|--------|------------------|--------|
| New SOP section | PLAYBOOK + INDEX.md + Kanban | 30 min |
| New Playbook section | SOPs if procedural + INDEX.md | 30 min |
| Kanban task moved | Dashboard + Sprint Tracker | 15 min |
| Git branch created | Kanban + Session Log | 10 min |
| Session completed | INDEX.md + Dashboard + Kanban | End of session |
| New agent added | AGENTS.md + AGENT_REGISTRY.md + INDEX.md | Immediately |
| Deviation logged | INDEX.md + PLAYBOOK + Kanban | 15 min |

---

## 📖 Continuous Learning Documentation

### The "Learning Series" Purpose

**Why we document as we work:**

> "Future developers should be able to read our journey and understand HOW we built this, WHY we made certain decisions, and WHAT problems we solved along the way."

### Documentation as Storytelling

| Document | Purpose | Audience | Timing |
|----------|---------|----------|--------|
| **PLAYBOOK** | Technical "how-to" guide | Future developers | As features are built |
| **JOURNAL** | Story of our journey | New devs + future selves | Daily, as decisions happen |
| **DECISION_LOG** | Rationale for choices | Architects + reviewers | At every decision point |
| **ROADBLOCKS** | Problems + solutions | Debuggers + learners | When issues are solved |

### Continuous Update Triggers

| Chat Event | Update | Purpose |
|------------|--------|---------|
| Feature started | PLAYBOOK + JOURNAL | "Today we're building X..." |
| Decision made | DECISION_LOG + JOURNAL | "We chose Y because..." |
| Problem solved | ROADBLOCKS + JOURNAL | "Issue Z was fixed by..." |
| Pattern discovered | PLAYBOOK + TIPS_TRICKS | "Here's a better way to..." |
| Refactoring done | PLAYBOOK + JOURNAL | "We improved X by..." |
| Lesson learned | JOURNAL + TIPS_TRICKS | "Next time, do this instead..." |

### PM-Agent Continuous Monitoring

PM-Agent ensures PLAYBOOK and JOURNAL are updated AS WE CHAT:

```markdown
## 📖 Documentation Check

**Feature:** [[Current feature being discussed]]

**Has this been documented?**
- [ ] PLAYBOOK updated with progress
- [ ] JOURNAL entry made for today's journey
- [ ] DECISION_LOG has the rationale (if decision made)
- [ ] ROADBLOCKS updated (if problem solved)

**Reminder to [[Agent]]:**
"While we work on [[feature]], should I update [[document]]?"
```

### Agent Continuous Update Prompts

Agents should proactively offer updates:

```markdown
[UPDATE] OpenCode: Making decision on [[X]]
→ Decision: [[What we chose]]
→ Rationale: [[Why]]
→ PLAYBOOK: Adding to DECISION_LOG
→ JOURNAL: Will note this decision point

[UPDATE] Molt: Just solved [[problem]]
→ Solution: [[How we fixed it]]
→ PLAYBOOK: Adding to ROADBLOCKS
→ JOURNAL: Documenting the troubleshooting journey
```

### The Learning Series Framework

Every PLAYBOOK entry should tell a story:

```markdown
## [[Feature/Pattern Name]]

### The Problem
[[What we were trying to solve]]

### The Journey
[[Step-by-step of how we approached it]]
- Step 1: [[What we tried first]]
- Step 2: [[What we learned]]
- Step 3: [[How we adjusted]]

### The Decision
[[Why we chose this approach over alternatives]]
- Option A: [[Why not]]
- Option B: [[Why not]]
- Our Choice: [[Why yes]]

### The Solution
[[The final implementation]]

### The Lesson
[[What we learned for next time]]

### Code Example
[[Copy-paste ready code]]

### Related
- [[Related patterns]]
- [[Related decisions]]
- [[Related problems]]
```

### PM-Agent End-of-Day Documentation Check

```markdown
## 📖 End-of-Day Documentation Check

**Today's Progress Documented?**

| Document | Updated Today? | Entry Count |
|----------|---------------|-------------|
| PLAYBOOK | ✅/❌ | [[N]] |
| JOURNAL | ✅/❌ | [[N]] |
| DECISION_LOG | ✅/❌ | [[N]] |
| ROADBLOCKS | ✅/❌ | [[N]] |
| TIPS_TRICKS | ✅/❌ | [[N]] |

**Learning Series Completeness:**
- [ ] Feature progress captured
- [ ] Decisions explained
- [ ] Problems documented
- [ ] Solutions shared
- [ ] Lessons recorded

**For Future Developers:**
- [ ] Clear "how-to" written?
- [ ] Rationale explained?
- [ ] Code examples provided?
- [ ] Related resources linked?
```

### Continuous Documentation Cadence

```
DURING CHAT SESSION
      │
      ├─→ Decision made → Update DECISION_LOG + JOURNAL
      │
      ├─→ Problem solved → Update ROADBLOCKS + JOURNAL
      │
      ├─→ Pattern learned → Update PLAYBOOK + TIPS_TRICKS
      │
      ├─→ Feature progress → Update PLAYBOOK + JOURNAL
      │
      └─→ PM-Agent monitors: "[UPDATE] Should I document [[X]]?"

EVERY 15 MIN → Session Pulse includes documentation check
END OF DAY → Full documentation audit + learning series review
```

---

### PM-Agent Documentation Cohesion Check

PM-Agent MUST verify these synchronizations daily:

```markdown
## 📚 Documentation Cohesion Check - [[DATE]]

### 1. SOPs Sync Status

| SOP Changed | PLAYBOOK Updated | INDEX.md Updated | Kanban Updated |
|-------------|------------------|------------------|----------------|
| [[SOP]] | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found:**
- [[Issue]] → [[Agent to fix]]

### 2. Playbook Sync Status

| Section Changed | SOPs Synced | INDEX.md Updated | Dashboard Updated |
|-----------------|-------------|------------------|-------------------|
| [[Section]] | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found:**
- [[Issue]] → [[Agent to fix]]

### 3. Kanban + Dashboard Sync

| Task Status | Dashboard Updated | Sprint Tracker Updated | INDEX Updated |
|-------------|-------------------|------------------------|----------------|
| [[Task]] | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found:**
- [[Issue]] → [[Agent to fix]]

### 4. Git + Session Sync

| Branch Created | Kanban Updated | Session Logged | INDEX Updated |
|----------------|----------------|----------------|----------------|
| [[Branch]] | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found:**
- [[Issue]] → [[Agent to fix]]

### 5. Deviation Tracking

| Deviation | DEVIATIONS.md | Related Docs Updated | Owner Notified |
|-----------|---------------|---------------------|----------------|
| [[Dev]] | ✅/❌ | ✅/❌ | ✅/❌ |

**Issues Found:**
- [[Issue]] → [[Agent to fix]]

---

## Cohesion Score: [[X]]/[[Y]] Items Synced

---

## 💬 Communication Format

### Message Prefix System

```
[UPDATE]  - Status update, no response needed
[REQUEST] - Needs response from specific agent
[ALERT]   - Urgent, all agents attention
[HANDOFF] - Transfer to another agent
[QUESTION]- Seeking clarification
[DECISION]- Final determination made
[NOTE]    - Information only
```

### Examples

```markdown
[UPDATE] OpenCode: New multi-agent template library created
→ Location: 60-Resources/PLAYBOOK/multi-agent-templates/
→ Files: 10 templates added
→ Next: PM-Agent to update REGISTRY

[REQUEST] Historian: Need docs updated for templates
→ OpenCode: Can you share template list?
→ PM-Agent: Add to sprint tracker?

[ALERT] OpenCode: Docker not running, Supabase inaccessible
→ PM-Agent: Coordinate workaround
→ Molt: Pause content processing

[HANDOFF] OpenCode → Historian: PLAYBOOK updated
→ 10 new templates documented
→ Review: 60-Resources/PLAYBOOK/multi-agent-templates/

[DECISION] PM-Agent: Use session branching over Docker
→ Rationale: Simpler for POC, less overhead
→ Review: AGENTS.md updated

[REMINDER] PM-Agent: Kanban task not updated
→ "Hey, I noticed [[Task]] is still in progress. Should I move it?"
```

---

## 🔄 Frequent Update Cadence

### During Active Session (Every ~15 min)

```markdown
## Session Pulse - [[TIME]]

**Active Work:**
- OpenCode: [[What building/fixing]]
- Molt: [[What processing]]
- Historian: [[What documenting]]
- PM-Agent: [[What coordinating]]

**Updates Since Last:**
- ✅ [[Update 1]]
- ✅ [[Update 2]]

**Pending Actions:**
- ⏳ [[Action 1]] → [[Who]]
- ⏳ [[Action 2]] → [[Who]]

**Blockers:**
- [[None / Issue]]
```

### On Discovery/Decision (Immediately)

```markdown
## ⚡ Discovery - [[WHO]] - [[TIME]]

**What:** [[SHORT DESCRIPTION]]
**Impact:** [[HIGH/MEDIUM/LOW]]
**Action Required:** [[YES/NO]]

**Details:** [[2-3 SENTENCES]]

**Owner:** [[AGENT]]
**Update Location:** [[WHERE]]
```

### On Task Completion

```markdown
## ✅ Completed - [[WHO]] - [[TIME]]

**Task:** [[NAME]]
**Location:** [[FILE/PATH]]
**Next:** [[HANDOFF OR DONE]]

**Session Updated:** [[YES/NO]]
**Tracker Updated:** [[YES/NO]]
```

---

## 🎯 Agent Communication Duties

### OpenCode Duties

```markdown
When I discover/update:
→ New code pattern → Update PLAYBOOK immediately
→ New command/tool → Update 04-COMMANDS.md
→ Architecture decision → Update PLAYBOOK + notify PM-Agent
→ Code complete → Update SPRINT_TRACKER + handoff to Historian
```

### Molt Duties

```markdown
When I discover/update:
→ Content processing pattern → Update PLAYBOOK + notify Historian
→ User workflow insight → Update PLAYBOOK + notify PM-Agent
→ Content task complete → Update SPRINT_TRACKER + handoff to OpenCode
```

### Historian Duties

```markdown
When I discover/update:
→ New pattern → Update PLAYBOOK immediately
→ Documentation gap → Fill it + note in TIPS_TRICKS
→ Session log complete → Update INDEX + notify PM-Agent
→ New template → Add to TEMPLATES + update README
```

### PM-Agent Duties

```markdown
When I discover/update:
→ Any decision made → Update DECISION_LOG
→ Task status change → Update SPRINT_TRACKER
→ Session complete → Update INDEX
→ Blocker resolved → Update ROADBLOCKS
→ New pattern noted → Review PLAYBOOK health

**CONTINUOUS DOCUMENTATION (As We Chat):**
→ Feature progress → Update PLAYBOOK with step-by-step
→ Decision made → Log in DECISION_LOG with rationale
→ Problem solved → Document in ROADBLOCKS with solution
→ New insight → Add to TIPS_TRICKS with context
→ Every feature → Tell a story in JOURNAL for new devs
→ Every decision → Record WHY for learning series

**PURPOSE: Learning Series for Future Devs**
→ New devs can read our journey
→ "How did they build this?"
→ "Why did they choose X over Y?"
→ "What problems did they face?"
→ "How did they solve it?"

**END-OF-DAY (Critical):**
→ Run project-wide cohesion check
→ Identify refactoring needs
→ Log all changes and checkpoints
→ Ensure all docs updated
→ Report status to human

**SELF-IMPROVEMENT (Ongoing):**
→ Monitor for gaps in SOPs → Update SOPs
→ Monitor for missing docs → Create docs
→ Monitor for outdated info → Refresh docs
→ Monitor for better patterns → Propose improvements
→ **If human misses something → Remind politely**
→ **If process breaks → Fix and document fix**
```

---

## 🌙 End-of-Day Chief of Staff Review

### Daily Checkpoint (Every Session End)

PM-Agent MUST run this review before considering the day complete:

```markdown
## 🌙 End-of-Day Review - [[DATE]]

**Conducted By:** PM-Agent (AGT-006)
**Duration:** ~15-30 minutes

### 1. PROJECT-WIDE COHESION CHECK (The 6 Pillars)

| Pillar | Status | Last Updated | Issues |
|--------|--------|--------------|--------|
| **SOPs** | ✅/❌ | [[Time]] | [[Issues]] |
| **Version Control** | ✅/❌ | [[Time]] | [[Issues]] |
| **Playbook** | ✅/❌ | [[Time]] | [[Issues]] |
| **Journal** | ✅/❌ | [[Time]] | [[Issues]] |
| **Kanban** | ✅/❌ | [[Time]] | [[Issues]] |
| **Dashboard** | ✅/❌ | [[Time]] | [[Issues]] |

### 2. CROSS-REFERENCE SYNC VERIFICATION

| Update Made | Required Syncs | Status |
|------------|---------------|--------|
| [[Update 1]] | [[Required Docs]] | ✅/❌ |
| [[Update 2]] | [[Required Docs]] | ✅/❌ |

### 3. Refactoring Needs Identified

| Item | Priority | Owner | Action |
|------|----------|-------|--------|
| [[Issue]] | [[HIGH/MED/LOW]] | [[Agent]] | [[What to do]] |

### 4. All Changes Logged

| Change | Location | Agent |
|--------|----------|-------|
| [[Session logged]] | 80-Sessions/INDEX.md | [[Owner]] |
| [[Task updated]] | 90-Project-Board/ | [[Owner]] |
| [[Pattern documented]] | 60-Resources/PLAYBOOK/ | [[Owner]] |
| [[Decision recorded]] | DECISION_LOG | [[Owner]] |
| [[SOP updated]] | 40-SOPs/ | [[Owner]] |
| [[Deviation logged]] | DEVIATIONS.md | [[Owner]] |
| [[Branch created]] | .git/ | [[Owner]] |
| [[Dashboard updated]] | PROJECT_DASHBOARD.md | [[Owner]] |

### 5. Checkpoints Established

| Checkpoint | For | Due |
|------------|-----|-----|
| [[Checkpoint]] | [[What]] | [[When]] |

### 6. Human Handoff

```markdown
## 🌙 Daily Report - [[DATE]]

**Project Status:** [[HEALTHY/AT_RISK/BLOCKED]]

**Cohesion Score:** [[X]]/[[Y]] items in sync

**SOP Status:** [[Up-to-date / X updates pending]]
**Playbook Status:** [[Up-to-date / X updates pending]]
**Journal Status:** [[Up-to-date / X entries]]
**Kanban Status:** [[Up-to-date / X updates pending]]
**Dashboard Status:** [[Up-to-date / X updates pending]]

**Learning Series Progress:**
- 📖 [[Feature]] documented for future devs
- 📖 [[Decision]] rationale recorded
- 📖 [[Problem]] solution shared
- 📖 [[Lesson]] captured for next time

**For Future Developers:**
→ [[X]] new learning entries added
→ [[Feature]] now has complete documentation
→ [[Decision]] has clear rationale

**Documentation Quality Check:**
→ Every feature tells a story?
→ Every decision has rationale?
→ Every problem has solution?
→ Every lesson is shared?

**Self-Improvements Today:**
- 🧠 [[Gap detected]] → [[Fix applied]]

**Today's Wins:**
- ✅ [[Win 1]]
- ✅ [[Win 2]]

**Refactoring Done:**
- [[Refactor 1]]
- [[Refactor 2]]

**Documentation Updates:**
- 📄 PLAYBOOK: [[N]] new entries
- 📄 JOURNAL: [[N]] new entries
- 📄 DECISION_LOG: [[N]] decisions
- 📄 ROADBLOCKS: [[N]] solutions

**For Future Developers:**
→ [[X]] new learning entries added
→ [[Feature]] now has complete documentation
→ [[Decision]] has clear rationale

**Pending Items:**
- ⏳ [[Item]] → [[Owner]]

**Blockers:**
- [[None / Listed]]

**Tomorrow's Focus:**
1. [[Priority 1]]
2. [[Priority 2]]
```

---

## 📤 Session Chat Export

### Export Location

All session chats are exported to: `export_chat/YYYY-MM-DD_[session-name]-export.md`

### Export Template

```markdown
# Chat Export: [Session Name]

> **Date:** YYYY-MM-DD  
> **Session:** [Session Name]  
> **Duration:** ~X hours  
> **Agents Involved:** AGT-XXX, AGT-XXX  
> **Context:** [Brief description]

---

## 📋 Session Overview

| Field | Value |
|-------|-------|
| **Date** | YYYY-MM-DD |
| **Duration** | ~X hours |
| **Agents** | [Agents involved] |
| **Key Decisions** | [N decisions] |
| **Deliverables** | [Files created/modified] |

---

## 💬 Full Chat Log

### [Topic/Phase 1]

**[User]:** [Question/Request]

**[Assistant]:** [Response/Action]

[Tool outputs, code, etc.]

---

## 📦 Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `path/to/file` | Created/Modified | Purpose |

---

## 🎯 Key Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| [What] | [Why] | [Effect] |

---

## 📖 Learning Series Entries

| Entry | Document | Purpose |
|-------|----------|---------|
| [What] | [Where] | [Why for future devs] |

---

## 🔗 Related Sessions

- [Previous Session](link)
- [Related Session](link)

---

*Exported from chat session for V3 knowledge preservation.*
```

### Session Close Export Workflow

```markdown
## 🚪 Session Close

**Time:** [[Current time]]
**Trigger:** Human said "[[TRIGGER PHRASE]]"

---

### 📋 Session Summary

| Item | Status |
|------|--------|
| Session started | [[Time]] |
| Work completed | [[Summary]] |
| Docs updated | [[What]] |
| Next session | [[When/What continues]] |

### ✅ Quick Checklist

- [x] Current work saved
- [x] Docs updated for this session
- [x] Next steps documented
- [x] Session linked in INDEX.md
- [x] Chat exported to export_chat/

**Export:** `export_chat/YYYY-MM-DD_[session-name]-export.md`

### 📝 Next Session Will Continue

- [[What]]
- [[What]]

---

**Session saved. See you in the next session!**
```

### End-of-Day Export Workflow

End-of-Day already includes chat export in full review.

---

## 🚪 Session Close vs End-of-Day

### Session Close (Lighter)

Use when:
- Pausing work, continuing later
- Not end of work day
- Different session context needed

### End-of-Day (Full)

Use when:
- Truly done for the day
- Full review and report needed
- Tomorrow is a new day

---

## 🚪 Session Close Workflow

### How to Trigger

**Human says ANY of:**
- "close session"
- "end this session"
- "pause here"
- "continue later"
- "save state"

**PM-Agent response:**

```markdown
## 🚪 Session Close

**Time:** [[Current time]]
**Trigger:** Human said "[[TRIGGER PHRASE]]"

---

### 📋 Session Summary

| Item | Status |
|------|--------|
| Session started | [[Time]] |
| Work completed | [[Summary]] |
| Docs updated | [[What]] |
| Next session | [[When/What continues]] |

### ✅ Quick Checklist

- [ ] Current work saved
- [ ] Docs updated for this session
- [ ] Next steps documented
- [ ] Session linked in INDEX.md

### 📝 Next Session Will Continue

- [[What]]
- [[What]]

---

**Session saved. See you in the next session!**
```

---

### Session Close vs End-of-Day

| Aspect | Session Close | End-of-Day |
|--------|---------------|------------|
| **Triggers** | "close session", "pause here" | "end of day", "wrap up" |
| **Review** | Light | Full (6 pillars) |
| **Report** | Summary | Comprehensive |
| **Next** | Continue work | New day |
| **Time** | < 2 minutes | 15-30 minutes |

---

## 🔄 Concurrent Documentation Management

### When Multiple Updates Happen Simultaneously

If 2+ agents update docs concurrently:

1. **Agent A starts update** → Declare: `[UPDATE] Starting [[DOC]] update`
2. **Agent B wants update** → Check: `[REQUEST] Can I update [[DOC]]?`
3. **Resolution:**
   - If different docs → Both proceed
   - If same doc → Sequential (Agent A first, then Agent B)
4. **Sync verification** → PM-Agent confirms both updates reflected

### Conflict Detection

```markdown
[ALERT] PM-Agent: Documentation conflict detected

**Document:** [[DOC]]
**Agent A:** Updated at [[Time]]
**Agent B:** Updated at [[Time]]

**Resolution:**
- [ ] Merge both changes
- [ ] Choose one, archive other
- [ ] Request clarification from [[Agent]]
```

### Parallel Update Protocol

```
PARALLEL DOC UPDATES
      │
      ├─→ Agent A: `[UPDATE] Updating [[DOC-A]]`
      │
      ├─→ Agent B: `[UPDATE] Updating [[DOC-B]]`
      │
      ├─→ PM-Agent: Monitor for conflicts
      │
      ├─→ Both complete → PM-Agent: `[UPDATE] Docs [[A]] + [[B]] synced`
      │
      └─→ Conflict? → PM-Agent: `[ALERT] Conflict in [[DOC]]`
```

---

### End-of-Day Checklist (PM-Agent)

- [ ] **SOPs** - All recent changes synced with PLAYBOOK
- [ ] **Version Control** - Branches, commits, tags current
- [ ] **Playbook** - All patterns documented
- [ ] **Journal** - Entries for the day complete
- [ ] **Kanban** - All tasks accurate
- [ ] **Dashboard** - Metrics updated
- [ ] **Cross-references** - All docs point to right places
- [ ] **Deviations** - Logged and tracked
- [ ] **Session logs** - All complete in INDEX.md
- [ ] **Human report** - Generated and ready
- [ ] **Self-Improvement Check:**
  - [ ] Any gaps detected today?
  - [ ] Any SOPs need updating?
  - [ ] Any reminders needed for human?
  - [ ] Any new patterns to document?

---

## 🌙 End-of-Day Trigger

### How to Trigger End-of-Day

**Human says ANY of:**
- "end of day"
- "end of day wrap up"
- "wrap up"
- "close session"
- "that's all for today"
- "done for the day"

**PM-Agent response:**

```markdown
## 🌙 END-OF-DAY TRIGGERED

**Received:** [[Human's message]]
**Time:** [[Current time]]

**Initiating End-of-Day Review...**

[PM-Agent runs the full checklist below]
```

---

### End-of-Day Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    END-OF-DAY WORKFLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. HUMAN TRIGGERS                                          │
│     "end of day" / "wrap up" / "that's all"                │
│     ↓                                                       │
│  2. PM-AGENT ACKNOWLEDGES                                   │
│     "Initiating End-of-Day Review..."                       │
│     ↓                                                       │
│  3. COLLECT UPDATES FROM ALL AGENTS                        │
│     → OpenCode: What did you complete?                     │
│     → Molt: What did you complete?                         │
│     → Historian: What docs updated?                         │
│     ↓                                                       │
│  4. RUN COHESION CHECK                                     │
│     → SOPs synced?                                          │
│     → Playbook updated?                                     │
│     → Kanban accurate?                                      │
│     → Dashboard current?                                    │
│     → Session logs complete?                                │
│     ↓                                                       │
│  5. LOG ALL CHANGES                                         │
│     → Update INDEX.md                                       │
│     → Update SPRINT_TRACKER                                 │
│     → Update PLAYBOOK                                       │
│     → Update DEVIATIONS if any                              │
│     ↓                                                       │
│  6. IDENTIFY REFACTORING NEEDS                              │
│     → Code structure issues?                                │
│     → Documentation gaps?                                    │
│     → Process improvements?                                  │
│     ↓                                                       │
│  7. GENERATE HUMAN REPORT                                   │
│     → Daily Summary                                         │
│     → Cohesion Score                                        │
│     → Wins, Pending, Blockers                               │
│     → Tomorrow's Focus                                      │
│     ↓                                                       │
│  8. CONFIRM COMPLETION                                      │
│     "End-of-Day complete. See report below."                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### PM-Agent Response to "End of Day"

```markdown
## 🌙 End-of-Day Review Initiated

**Time:** [[YYYY-MM-DD HH:MM]]
**Trigger:** Human said "[[TRIGGER PHRASE]]"

---

### 📊 Collecting Agent Updates

**@OpenCode:** What did you complete today?

**@Molt:** What did you complete today?

**@Historian:** What documentation did you update?

---

### 🔄 Running Cohesion Check...

[PM-Agent checks all 6 pillars]

### 📝 Logging All Changes...

[PM-Agent updates INDEX.md, SPRINT_TRACKER, etc.]

### 🧠 Identifying Improvements...

[PM-Agent notes gaps and improvements]

---

### 🌙 Generating Daily Report...

[Full report appears here]

**End-of-Day Complete.**
**See report above for details.**
```

---

## 🧠 Self-Improvement Protocol

### PM-Agent Gap Detection

PM-Agent continuously monitors for:

| Gap Type | Detection Method | Action |
|----------|-----------------|--------|
| **Missing SOP** | Process has no documented procedure | Create SOP draft, propose to human |
| **Outdated SOP** | SOP contradicts current practice | Update SOP, flag for review |
| **Missing Documentation** | Concept exists but not documented | Create documentation, notify owner |
| **Process Gap** | Work happening without proper handoff | Create handoff template, train agents |
| **Tool Gap** | Manual task that should be automated | Propose automation, update PLAYBOOK |
| **Communication Gap** | Agents not coordinating | Strengthen protocol, add checkpoints |
| **New Workflow** | New pattern of work discovered | Add to AGENT_WORKFLOW_VISUALIZATION.md |
| **Workflow Improved** | Better way to handle handoffs | Update AGENT_WORKFLOW_VISUALIZATION.md |

### PM-Agent Human Reminders

When PM-Agent detects human missing something:

```markdown
[REMINDER] PM-Agent: [[ISSUE TYPE]] Detected

**What:** [[Short description of gap]]

**Impact:** [[Why this matters]]

**Suggested Action:** [[What human should do]]

**I'll:** [[What PM-Agent will do to help]]

Examples:
- "Hey, I noticed you didn't update the Kanban for that task. Want me to do it?"
- "The SOP for this process is missing. Should I draft one?"
- "This pattern isn't in the PLAYBOOK. Want me to add it?"
- "We're missing a checkpoint here. Shall I add one to the SOP?"
```

### Self-Improvement Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    SELF-IMPROVEMENT CYCLE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DETECT    → PM-Agent notices gap                        │
│       ↓                                                   │
│  2. ANALYZE   → What caused the gap?                        │
│       ↓                                                   │
│  3. PROPOSE   → Suggest fix to human                        │
│       ↓                                                   │
│  4. APPROVE   → Human approves or modifies                   │
│       ↓                                                   │
│  5. IMPLEMENT → PM-Agent updates SOPs/docs                  │
│       ↓                                                   │
│  6. VALIDATE  → Confirm fix works                          │
│       ↓                                                   │
│  7. DOCUMENT  → Log improvement in DECISIONS.md              │
│       ↓                                                   │
│  8. REPEAT   → Continuous monitoring                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### SOP Auto-Improvement Triggers

| Trigger | PM-Agent Action |
|---------|-----------------|
| Same deviation happens 3x | Propose new/revised SOP |
| Agent asks "how do I..." | Check SOP, if missing → Create draft |
| Process breaks | Fix immediately, document fix in ROADBLOCKS |
| New pattern emerges | Add to PLAYBOOK, propose to SOPs |
| Human says "we should..." | Create SOP action item |
| Documentation outdated | Refresh and timestamp |

### Improvement Logging

All self-improvements logged:

```markdown
## 🧠 Self-Improvement Log - [[DATE]]

### Gap Detected
- **Issue:** [[What was missing]]
- **Impact:** [[Why it mattered]]
- **Detected By:** PM-Agent

### Solution Proposed
- **Action:** [[What was done]]
- **SOPs Updated:** [[Which SOPs]]
- **Docs Created:** [[Which docs]]
- **Workflow Visualization:** [[Added/Updated AGENT_WORKFLOW_VISUALIZATION.md]]

### Human Approval
- **Approved By:** [[Human/Not applicable]]
- **Date:** [[Date]]

### Result
- **Status:** Implemented
- **Validation:** [[How we know it works]]
- **Next Review:** [[Date]]
```

### Workflow Visualization Updates

When new workflows are discovered:

```markdown
## 🔄 Workflow Update - [[DATE]]

**New Workflow:** [[Name]]
**Phase:** [[Which phase it belongs to]]
**Trigger:** [[When it begins]]
**Participants:** [[Which agents involved]]

**Added to:** AGENT_WORKFLOW_VISUALIZATION.md
**Status:** ✅ Documented
```

---

## 🔗 Quick Reference Cards

### End-of-Day Workflow (TRIGGER)

```
┌─────────────────────────────────────────────────────────────┐
│               END-OF-DAY WORKFLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HUMAN: "end of day" / "wrap up" / "done for today"       │
│      ↓                                                      │
│  PM-AGENT: "Initiating End-of-Day Review..."               │
│      ↓                                                      │
│  1. Collect updates from all agents                        │
│  2. Run cohesion check (6 pillars)                        │
│  3. Log all changes (INDEX, PLAYBOOK, JOURNAL, etc.)      │
│  4. Verify learning series entries for future devs         │
│  5. Identify refactoring needs                             │
│  6. Generate daily report for human                        │
│      ↓                                                      │
│  "End-of-Day complete. See report below."                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Learning Series Check:**
→ How many entries added today?
→ Is every feature documented?
→ Do new devs understand our journey?

### At a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                    UPDATE RESPONSIBILITIES                   │
├──────────────────┬──────────────────────────────────────────┤
│ NEW PATTERN      │ Owner → PLAYBOOK/                         │
│ NEW COMMAND      │ Any → PLAYBOOK/04-COMMANDS.md            │
│ NEW INSIGHT      │ Any → PLAYBOOK/07-TIPS_TRICKS.md         │
│ PROBLEM SOLVED   │ Any → PLAYBOOK/03-ROADBLOCKS.md          │
│ TASK DONE        │ Owner → 90-Project-Board/SPRINT_TRACKER  │
│ SESSION LOGGED   │ Owner → 80-Sessions/INDEX.md              │
│ ARCH DECISION    │ OpenCode → PLAYBOOK/ + DECISION_LOG.md   │
│ BLOCKER FOUND    │ Any → PM-Agent (alert) + PLAYBOOK/       │
│ GAP DETECTED     │ PM-Agent → [REMINDER] + Create SOP       │
└──────────────────┴──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         LEARNING SERIES FOR FUTURE DEVS                      │
├──────────────────┬──────────────────────────────────────────┤
│ Feature built    → → JOURNAL: "Here's what we built..."     │
│ Decision made    → → DECISION_LOG: "Why we chose X..."     │
│ Problem solved   → → ROADBLOCKS: "Issue Z → Solution Y"    │
│ Pattern learned  → → PLAYBOOK: "Better way to do X..."      │
│ Lesson captured  → → TIPS_TRICKS: "Next time, do Y..."     │
│ Every chat       → → PM-Agent: "Documenting this for..."   │
└──────────────────┴──────────────────────────────────────────┘
```

### Message Prefixes

```
[UPDATE]   - Status, no response
[REQUEST]  - Needs response
[ALERT]    - Urgent, all attention
[HANDOFF]  - Transfer ownership
[QUESTION] - Seeking clarification
[DECISION] - Final determination
[NOTE]     - FYI only
[REMINDER] - PM-Agent gap detected
```

### End-of-Day Trigger

```
HUMAN SAYS:
  → "end of day"
  → "end of day wrap up"
  → "wrap up"
  → "that's all for today"
  → "done for the day"

PM-AGENT RESPONDS:
  → Full End-of-Day Review
  → Collects agent updates
  → Runs cohesion check
  → Logs all changes
  → Generates daily report
```

### Session Close Trigger

```
HUMAN SAYS:
  → "close session"
  → "end this session"
  → "pause here"
  → "continue later"
  → "save state"

PM-AGENT RESPONDS:
  → Light Session Close
  → Quick summary
  → Docs updated for this session
  → Next steps documented
  → Ready for next session
```

### Quick Comparison

| Trigger | Response | Time |
|---------|----------|------|
| "end of day" | Full review + report | 15-30 min |
| "close session" | Light save + continue | < 2 min |
```

### Update Timeline

```
SESSION START → Presence declaration
    ↓
EVERY 15 MIN → Session Pulse
    ↓
ON DISCOVERY → Discovery note
    ↓
ON DECISION → Decision log
    ↓
ON COMPLETION → Completion note
    ↓
ON GAP DETECTED → PM-Agent [REMINDER]
    ↓
HUMAN SAYS "END OF DAY" → Full End-of-Day Workflow
    ↓
SESSION COMPLETE
```

### Self-Improvement Loop

```
DETECT → ANALYZE → PROPOSE → APPROVE → IMPLEMENT → VALIDATE → DOCUMENT
```

---

## 🚨 Enforcement

### Missing Updates Protocol

If an update is missed:

1. **Detection** - Another agent notices gap
2. **Alert** - `[ALERT] [WHO]: Missing update for [[EVENT]]`
3. **Response** - Primary agent updates within 10 minutes
4. **Escalation** - If no response, PM-Agent intervenes

### Quality Gates

- [ ] Updates have clear ownership
- [ ] Updates go to correct location
- [ ] Updates happen within cadence
- [ ] All agents aware of session status

---

## 📚 Related Documents

- [COORDINATION_PROTOCOL.md](./COORDINATION_PROTOCOL.md) - General coordination
- [AGENT_REGISTRY.md](./AGENT_REGISTRY.md) - Agent definitions
- [SESSION_TEMPLATE.md](../../80-Sessions/TEMPLATES/SESSION_TEMPLATE.md) - Session format

---

*Protocol ensures no discovery is lost, no update is forgotten.*
