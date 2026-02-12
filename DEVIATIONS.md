# AOKhmer - SOP Deviation Log

> **Purpose:** Track deviations from Standard Operating Procedures (SOPs) for future reference, lessons learned, and v3 improvements  
> **Last Updated:** 2026-02-11  
> **Status:** ACTIVE

---

## 📋 Deviation Entry Format

When deviating from any SOP, document it here using this format:

```markdown
### DEV-[NUMBER]: [Brief Title]
**Date:** YYYY-MM-DD  
**Agent:** [Agent Name]  
**SOP Violated:** [SOP Name/File]  
**Severity:** [CRITICAL / HIGH / MEDIUM / LOW]  

**Context:**
[Why the deviation was necessary - the specific situation]

**Deviation:**
[What was done differently from the SOP]

**Justification:**
[Why this was the right call at the time]

**Impact:**
[What happened as a result - good and bad]

**Lesson Learned:**
[What to remember for v3 or future iterations]

**Commit Reference:**
[SHA or commit message if applicable]
```

---

## 🚨 Deviation Entries

### DEV-002: Session Logging Workflow Creation
**Date:** 2026-02-11  
**Agent:** OpenCode (AGT-002)  
**SOP Violated:** None - Enhancement  
**Severity:** N/A (Improvement)  

**Context:**
Implementing comprehensive session logging and knowledge management system to support V3 planning.

**Deviation:**
Created NEW workflows rather than following existing patterns. Added:
- 5-file session template
- Knowledge management guide
- Framework health dashboard
- Updated 4 existing documents with logging duties

**Justification:**
Existing SOPs didn't explicitly require session logging. This enhancement formalizes the practice for V3 knowledge preservation.

**Impact:**
- All future sessions will be fully documented
- 5 mandatory files per session
- Framework health tracked weekly

**Lesson Learned:**
Start with comprehensive documentation from day 1 rather than retrofitting later.

**Commit Reference:**
`session: 2026-02-11 - Framework health & knowledge management`

---

### DEV-001: Initial Repository Setup - Flattened Structure
**Date:** 2026-02-11  
**Agent:** OpenCode (AGT-002)  
**SOP Violated:** AGENT-OPENCODE.md Workflow 1 (Feature Branch Process)  
**Severity:** LOW  

**Context:**
Setting up initial project repository. Files were nested in `clean_build_v2/` and needed to be moved to root for proper project structure.

**Deviation:**
Committed initial setup directly to main branch instead of creating a feature branch. This was initial repository setup with no prior history.

**Justification:**
- No prior commits existed (empty repository)
- No risk of conflict or breaking existing code
- Infrastructure setup, not feature development
- Would be unnecessarily bureaucratic to use feature branch for initial scaffolding

**Impact:**
- ✅ Repository properly structured
- ✅ All 70+ documentation files preserved
- ✅ No negative impact on project integrity

**Lesson Learned:**
Initial repository setup may bypass standard workflow since there's nothing to branch from. However, from now on, ALL changes must follow:
```
Feature Branch → PR → Merge → Main
```

**Commit Reference:**
Initial setup commit (multiple files)

---

### DEV-002: n8n Workflows Despite Deprecation
**Date:** 2026-02-11  
**Agent:** OpenCode (AGT-002) + Human Developer  
**SOP Violated:** Brand Identity Bible Section 9.1 (Recommends Prefect over n8n)  
**Severity:** LOW  

**Context:**
The Brand Identity Bible (generated 2026-02-11) marks n8n as DEPRECATED, recommending Prefect for workflow orchestration. User explicitly requested n8n for Phase 5 development.

**Deviation:**
Using n8n for workflow automation instead of Prefect (as recommended by Bible).

**Justification:**
- User preference for n8n takes priority over documentation recommendations
- n8n is sufficient for POC scale (50+ songs, not 1000+)
- Visual workflow is easier for beginner developer
- Can migrate to Prefect later when scaling (Bible notes n8n migration path)

**Impact:**
- ✅ Faster POC development (user comfortable with n8n)
- ⚠️ May need refactoring at scale
- ⚠️ Some Bible examples reference Prefect syntax

**Lesson Learned:**
- Document conflicts between user preference and generated documentation
- Keep n8n workflows modular for potential Prefect migration
- Re-evaluate Prefect at 1000+ songs scale

**Related Files:**
- `60-Resources/PLAYBOOK/08-BRAND_IDENTITY.md` (Integration note)
- Brand Identity Bible (full reference in chat history)

**Commit Reference:**
Phase 5 setup - n8n workflow foundation

---

### DEV-003: [Future Entry Template]
**Date:** YYYY-MM-DD  
**Agent:** [Agent Name]  
**SOP Violated:** [SOP Reference]  
**Severity:** [LEVEL]  

**Context:**
[Description]

**Deviation:**
[What was done differently]

**Justification:**
[Why]

**Impact:**
[Results]

**Lesson Learned:**
[Takeaway for v3]

**Commit Reference:**
[SHA]

---

## 📊 Deviation Statistics

| Metric | Count |
|--------|-------|
| Total Deviations | 2 |
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 2 |

---

## 🔄 Review Cycle

- **Weekly:** Review with human supervisor during development sprints
- **Monthly:** Compile lessons learned for v3 planning
- **Quarterly:** Full SOP review to incorporate deviations into official SOPs

---

## 📝 Notes for AI Agents

**When to document deviations:**
1. ✅ Always document when consciously choosing not to follow an SOP
2. ✅ Document when unclear situations require improvisation
3. ✅ Document when SOPs are incomplete or contradictory
4. ❌ Don't document for typos, formatting, or trivial changes
5. ❌ Don't document for SOP clarifications (update the SOP instead)

**Commit Message Integration:**
When a deviation is documented here, include a reference in the commit message:
```
feat: add user authentication

DEVIATION: DEV-001 - See DEVIATIONS.md for context on bypassing 
standard review process due to emergency patch requirement.
```

---

*"Every deviation is a lesson. Every lesson makes v3 better."*
