# 🚨 Emergency End Session Protocol

> **Purpose:** Ensure all session documentation is preserved even if chat closes unexpectedly  
> **Trigger:** User says "end session" or chat window at risk of closing  
> **Status:** ACTIVE  
> **Last Updated:** 2026-02-11

---

## 🎯 When to Use

| Situation | Action |
|-----------|--------|
| Chat window closing unexpectedly | Run emergency save |
| Session ending normally | Follow complete protocol |
| Lunch break > 1 hour | Run quick save |
| End of work day | Run complete protocol |

---

## 🏃 Emergency Save (Quick - 2 minutes)

**If chat is closing NOW:**

1. **Run this command:**
```bash
# Creates backup of all unsaved session files
cp -r 80-Sessions/2026-02/2026-02-11_*/ ~/.klm-backup/ 2>/dev/null || echo "Backup folder created"
```

2. **Minimum save:**
- Copy session folder path to clipboard
- Note: `80-Sessions/YYYY-MM/SESSION_NAME/`

---

## 📋 Complete End Session Protocol (5-10 minutes)

### Step 1: Verify Session Files Exist

```bash
# Check current session folder
ls -la 80-Sessions/2026-02/*/SUMMARY.md 2>/dev/null || echo "No session folder found"

# List current session files
ls 80-Sessions/2026-02/*/ 2>/dev/null | head -20
```

### Step 2: Complete Session Checklist

**For the current session folder, verify:**

| File | Status | Action |
|------|--------|--------|
| `SUMMARY.md` | ☐ | Fill executive overview |
| `FULL_LOG.md` | ☐ | Complete running log |
| `DECISIONS.md` | ☐ | Log all decisions |
| `COMMITS.md` | ☐ | Document git history |
| `METRICS.md` | ☐ | Record KPIs |

### Step 3: Update Cross-References

| Document | Update Required |
|----------|-----------------|
| `80-Sessions/INDEX.md` | Add session link |
| `90-Project-Board/SPRINT_TRACKER.md` | Update task status |
| `60-Resources/PLAYBOOK/` | Add new patterns if any |
| `DEVIATIONS.md` | Log if any SOP deviations |
| `export_chat/` | Export chat session |

### Step 4: Export Chat Session

```bash
# Export this session to export_chat folder
# Copy template
cp export_chat/CHAT_EXPORT_TEMPLATE.md export_chat/YYYY-MM-DD_[session-name]-export.md

# Fill with session summary:
# - Overview
# - Key decisions
# - Files created/modified
# - Lessons learned
```

### Step 5: Commit Session Files

```bash
# Add session folder
git add 80-Sessions/YYYY-MM/session-name/

# Commit
git commit -m "session: YYYY-MM-DD - Brief description

- Duration: X hours
- SOP Compliance: X%
- Tasks completed: N
- Files created: session-folder/
"
```

---

## 🔄 Quick Reference Commands

### Before Closing Chat

```bash
# 1. Quick backup
cp -r 80-Sessions/2026-02/*current-session* ~/.klm-backup/ 2>/dev/null

# 2. Check session files exist
ls 80-Sessions/2026-02/*/SUMMARY.md

# 3. Note session folder
echo "Session folder: $(ls -d 80-Sessions/2026-02/*/ | tail -1)"
```

### Recovery (If Chat Closes)

```bash
# 1. Check backup
ls ~/.klm-backup/ 2>/dev/null

# 2. Resume session
# - Open session folder
# - Continue documentation
```

---

## 📝 Session Recovery Template

**If chat closes and you need to recover:**

```markdown
# Session Recovery: [SESSION NAME]

**Original Date:** YYYY-MM-DD
**Recovery Date:** YYYY-MM-DD

## What Was Completed
- [Task 1]
- [Task 2]

## Files That Exist
- [x] SUMMARY.md
- [ ] FULL_LOG.md (incomplete)
- [ ] DECISIONS.md (incomplete)

## What Needs Completion
1. [ ] Finish FULL_LOG.md
2. [ ] Complete DECISIONS.md
3. [ ] Update INDEX.md
4. [ ] Update SPRINT_TRACKER.md

## Recovery Notes
[Any context lost that needs reconstruction]
```

---

## 🛡️ Safety Checklist

Before ending any session:

- [ ] All 5 session files created
- [ ] Cross-references updated
- [ ] Git committed (or staged)
- [ ] Backup copied (optional)
- [ ] Session folder noted
- [ ] Chat exported to `export_chat/`

---

## 💾 Chat Export

| Item | Status |
|------|--------|
| Template exists | ✅ `export_chat/CHAT_EXPORT_TEMPLATE.md` |
| Export location | `export_chat/YYYY-MM-DD_[session]-export.md` |
| This session exported | ✅ `export_chat/2026-02-11_pm-agent-session-export.md` |

---

## 🤖 Agent End Session Workflow

When user says "end session", agents should:

1. **Pause current work**
2. **Run completion checklist**
3. **Verify all files exist**
4. **Commit if ready**
5. **Report completion status**

---

## 📞 Recovery Resources

| Situation | Action |
|-----------|--------|
| Chat closed unexpectedly | Check `~/.klm-backup/` |
| Session files incomplete | Open and finish |
| Cross-references missing | Update INDEX.md, SPRINT_TRACKER.md |
| Git not committed | Stage and commit |
| Unsure what was done | Check `FULL_LOG.md` |

---

*Part of PM-Agent (AGT-006) Chief of Staff operations*
