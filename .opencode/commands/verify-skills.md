---
description: Verify all skills are properly configured and recognized by OpenCode
agent: build
---

Verify that all skills in the project are properly configured and recognized by OpenCode.

1. List all skills in `.opencode/skills/`
2. Check each skill has a valid SKILL.md file with proper frontmatter (name and description)
3. Verify the skill structure follows the correct pattern
4. Report any issues found

Current skills:
!.`ls -la .opencode/skills/`

Check each skill:
@.opencode/skills/skill-commit/SKILL.md
@.opencode/skills/skill-design/SKILL.md
@.opencode/skills/skill-generate/SKILL.md
@.opencode/skills/skill-doc/SKILL.md
@.opencode/skills/skill-sinc/SKILL.md

Report:
- Which skills are properly configured
- Which skills have issues (missing files, invalid format)
- Any recommendations to fix issues
