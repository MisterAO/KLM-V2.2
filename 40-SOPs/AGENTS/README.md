# 🤖 AGENT SOPs - README

> **Quick guide to the Agent SOP system**

---

## 📖 What Are Agent SOPs?

Agent SOPs (Standard Operating Procedures) are **role-specific guides** for AI agents that define:

1. **WHO** - Agent identity and responsibilities
2. **WHAT** - Standard workflows to execute
3. **WHEN** - Decision matrices for taking vs escalating work
4. **HOW** - Step-by-step procedures with error handling
5. **WHY** - Context for how their role fits the bigger picture

---

## 🗂️ Structure

```
AGENTS/
├── AGENT-MOLT.md          ← Production Manager (ACTIVE)
├── AGENT-OPENCODE.md      ← Lead Engineer (ACTIVE)
├── AGENT-GUARDIAN.md      ← Security (PLANNED)
├── AGENT-TECHNICIAN.md    ← DevOps (PLANNED)
├── AGENT-HISTORIAN.md     ← Content (PLANNED)
├── AGENT-PM.md            ← Project Manager (PLANNED)
└── AGENT-ANALYST.md       ← Data Analyst (PLANNED)
```

---

## 🎯 For AI Agents

**If you're a new agent instance:**

1. **Read your assigned SOP** - This is your operational bible
2. **Check AGENT_REGISTRY.md** - Understand the ecosystem
3. **Review WORKFLOW_INTEGRATION.md** - Learn how to use technical SOPs
4. **Follow decision matrices** - Know when to work vs escalate
5. **Use error procedures** - Follow the recovery decision trees

**Key sections in every Agent SOP:**
- ✅ **Purpose** - Your role and philosophy
- ✅ **Decision Matrix** - What work to take vs handoff
- ✅ **Standard Workflows** - Step-by-step procedures
- ✅ **Error Recovery** - Decision trees for failures
- ✅ **Handoff Protocols** - How to escalate
- ✅ **Success Metrics** - How you're measured

---

## 👥 For Humans

**If you're onboarding or managing agents:**

1. **AGENT_REGISTRY.md** - Central registry of all agents
2. **SOP_INDEX.md** - Complete catalog of all SOPs
3. **Individual Agent SOPs** - Detailed operational guides

**Version Control:**
- All SOPs are version controlled
- Changes logged in each SOP's version history
- Major changes require human approval
- Agents always use latest version

---

## 🔗 Integration with Technical SOPs

Agent SOPs reference **Phase-2-God-Tier** technical SOPs for implementation details:

```
Agent SOP (WHO + WHAT)
    ↓
Workflow Integration (mapping)
    ↓
Technical SOP (HOW)
```

**Example:**
- **Molt** wants to auto-retry a failed API call
- **AGENT-MOLT.md** says "Use exponential backoff"
- **WORKFLOW_INTEGRATION.md** maps to 02-Self-Healing.md
- **02-Self-Healing.md** provides exact code and procedures

---

## 🚨 Emergency Procedures

Every Agent SOP includes:
- Error recovery decision trees
- Escalation paths
- Emergency contacts
- Rollback procedures

**When in doubt:**
1. Check your Agent SOP error section
2. Consult WORKFLOW_INTEGRATION.md
3. Escalate to complementary agent
4. Alert human if critical

---

## 📝 SOP Maintenance

**Who updates SOPs?**
- **Agents themselves** - When they find gaps
- **Human supervisors** - For major changes
- **PM-Agent** (when active) - For coordination

**Update process:**
1. Identify gap or improvement
2. Draft changes in feature branch
3. Review by complementary agent
4. Test in staging environment
5. Merge with version bump
6. Notify all affected agents

---

## 📊 Success Metrics

Agent SOPs are measured by:
- Task completion rate > 95%
- Escalation rate < 5%
- Decision accuracy > 98%
- Response time < 30s
- SOP adherence 100%

---

**Questions? Check AGENT_REGISTRY.md or ask your complementary agent.**

**Version:** 1.0.0  
**Last Updated:** 2026-02-11
