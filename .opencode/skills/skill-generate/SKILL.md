---
name: skill-generate
description: Generate new skills following the correct OpenCode pattern
---

## What I do
Create new skills in the correct OpenCode format:
- Create folder: `.opencode/skills/<skill-name>/SKILL.md`
- Add YAML frontmatter with name and description
- Follow naming rules: lowercase, alphanumeric with hyphens

## When to use me
Use this when creating a new skill for the project.

## Skill Structure
```
.opencode/skills/<name>/
└── SKILL.md
```

## SKILL.md Format
```markdown
---
name: <skill-name>
description: <description (1-1024 chars)>
---

## What I do
- Describe capabilities

## When to use me
- Describe usage context
```

## Naming Rules
- 1-64 characters
- Lowercase alphanumeric with single hyphens
- Cannot start or end with hyphen
- No consecutive hyphens
- Must match folder name
