---
title: "Task: {{TITLE}}"
task_id: "{{ID}}"
priority: "{{PRIORITY}}"
status: "{{STATUS}}"
category: "{{CATEGORY}}"
---

# {{ID}}: {{TITLE}}

**Task ID:** {{ID}}  
**Title:** {{TITLE}}  
**Priority:** {{PRIORITY}}  
**Status:** {{STATUS}}  
**Category:** {{CATEGORY}}  
**Created:** {{CREATED_DATE}}  
**Last Updated:** {{UPDATED_DATE}}

---

## 🎯 Objective

{{OBJECTIVE}}

---

## 📋 Requirements

{{#each requirements}}
- [ ] {{this}}
{{/each}}

---

## ✅ Acceptance Criteria

{{#each criteria}}
- [ ] {{this}}
{{/each}}

---

## 👤 Assignment

**Primary:** {{ASSIGNEE}}  
**Reviewer:** {{REVIEWER}}  
**Estimated Duration:** {{ESTIMATE}}

---

## 🔗 Dependencies

{{#if dependencies}}
**Blocked By:**
{{#each dependencies}}
- [{{id}}]({{link}}) - {{title}}
{{/each}}
{{else}}
No dependencies
{{/if}}

**Blocks:**
{{#if blocks}}
{{#each blocks}}
- [{{id}}]({{link}}) - {{title}}
{{/each}}
{{else}}
Nothing blocked
{{/if}}

---

## 📅 Timeline

| Phase | Date | Notes |
|-------|------|-------|
| Created | {{CREATED_DATE}} | - |
| Started | {{STARTED_DATE}} | - |
| Completed | {{COMPLETED_DATE}} | - |
| Validated | {{VALIDATED_DATE}} | - |

---

## 📝 Implementation Notes

{{IMPLEMENTATION_NOTES}}

---

## 🧪 Testing

{{#each tests}}
- [ ] {{description}}
  - Method: {{method}}
  - Expected: {{expected}}
{{/each}}

---

## 🔒 Security Considerations

{{SECURITY_NOTES}}

---

## 📚 Related Resources

{{#each resources}}
- [{{name}}]({{link}}) - {{description}}
{{/each}}

---

## 💬 Discussion Log

{{#each discussions}}
**{{date}} - {{author}}**
{{content}}

{{/each}}

---

## 🏷️ Tags

{{#each tags}}
- {{this}}
{{/each}}

---

**Session Reference:** [{{SESSION_DATE}}](../../80-Sessions/{{SESSION_PATH}})

*Last updated by: {{UPDATED_BY}} on {{UPDATED_DATE}}*
