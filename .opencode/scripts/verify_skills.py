#!/usr/bin/env python3
"""Verify OpenCode skills are properly configured."""

import sys
import re
from pathlib import Path


def verify_skills(skills_dir: Path) -> bool:
    """Verify all skills in the given directory."""
    if not skills_dir.exists():
        print(f"ERROR: Skills directory not found: {skills_dir}")
        return False

    skills = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skills:
        print("WARNING: No skills found")
        return True

    all_valid = True
    print(f"\n{'='*50}")
    print(f"Verifying {len(skills)} skill(s) in {skills_dir}")
    print(f"{'='*50}\n")

    for skill_dir in sorted(skills):
        skill_name = skill_dir.name
        skill_file = skill_dir / "SKILL.md"

        print(f"Checking: {skill_name}")

        if not skill_file.exists():
            print(f"  ❌ ERROR: SKILL.md not found")
            all_valid = False
            continue

        try:
            content = skill_file.read_text(encoding="utf-8")

            frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not frontmatter_match:
                print(f"  ❌ ERROR: No valid frontmatter found")
                all_valid = False
                continue

            frontmatter = frontmatter_match.group(1)

            name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)

            if not name_match:
                print(f"  ❌ ERROR: 'name' not in frontmatter")
                all_valid = False
                continue

            if not desc_match:
                print(f"  ❌ ERROR: 'description' not in frontmatter")
                all_valid = False
                continue

            name = name_match.group(1).strip()
            description = desc_match.group(1).strip()

            if name != skill_name:
                print(f"  ⚠️  WARNING: name '{name}' doesn't match folder '{skill_name}'")

            if len(description) < 1 or len(description) > 1024:
                print(f"  ⚠️  WARNING: description length ({len(description)}) should be 1-1024 chars")

            print(f"  ✅ Valid: {name}")
            print(f"     Description: {description[:60]}...")

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            all_valid = False

    print(f"\n{'='*50}")
    if all_valid:
        print("✅ All skills are properly configured!")
    else:
        print("❌ Some skills have issues - please fix them")
    print(f"{'='*50}\n")

    return all_valid


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    skills_dir = project_root / ".opencode" / "skills"

    success = verify_skills(skills_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
