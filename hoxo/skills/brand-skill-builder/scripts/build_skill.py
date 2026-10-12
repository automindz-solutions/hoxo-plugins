#!/usr/bin/env python3
"""
Scaffold a generated brand skill folder from a JSON spec, then package it as a .skill.

Usage:
    python build_skill.py <spec.json> <templates_dir> <output_dir>

The spec.json is produced by the brand-skill-builder workflow (Claude fills it in
based on extraction). It contains:
    - brand_name, brand_slug, brand_domain, source_url, generation_date, ...
    - all the placeholder values for the seven reference templates and SKILL.md
    - paths to extracted asset files to include in assets/

This script:
1. Creates <output_dir>/<brand_slug>-brand/
2. Copies and fills each template from <templates_dir>/<name>.tpl into the new folder
3. Copies extracted assets into assets/
4. Calls skill-creator's package_skill.py to produce the .skill file
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


TEMPLATES = [
    ("SKILL.md.tpl", "SKILL.md"),
    ("colors.md.tpl", "references/colors.md"),
    ("typography.md.tpl", "references/typography.md"),
    ("logo.md.tpl", "references/logo.md"),
    ("layouts.md.tpl", "references/layouts.md"),
    ("motifs.md.tpl", "references/motifs.md"),
    ("voice.md.tpl", "references/voice.md"),
    ("design-tokens.md.tpl", "references/design-tokens.md"),
]


def fill(template_text, spec):
    """Replace {{key}} placeholders with values from spec. Missing keys become '_(not extracted)_'."""
    out = template_text
    # Find all {{...}} occurrences and replace them
    import re
    def sub(match):
        key = match.group(1).strip()
        return str(spec.get(key, "_(not extracted)_"))
    return re.sub(r"\{\{([^}]+)\}\}", sub, out)


def main():
    if len(sys.argv) < 4:
        print("Usage: build_skill.py <spec.json> <templates_dir> <output_dir>")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    templates_dir = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    spec = json.loads(spec_path.read_text())
    brand_slug = spec["brand_slug"]
    skill_root = output_dir / f"{brand_slug}-brand"

    # Clean and create folder structure
    if skill_root.exists():
        shutil.rmtree(skill_root)
    (skill_root / "references").mkdir(parents=True, exist_ok=True)
    (skill_root / "assets").mkdir(parents=True, exist_ok=True)

    # Fill templates
    for tpl_name, out_name in TEMPLATES:
        tpl_path = templates_dir / tpl_name
        if not tpl_path.exists():
            print(f"⚠️  Template missing: {tpl_path}")
            continue
        tpl = tpl_path.read_text()
        filled = fill(tpl, spec)
        out_path = skill_root / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(filled)
        print(f"  Wrote: {out_path}")

    # Copy extracted assets
    for asset in spec.get("assets", []):
        src = Path(asset["src"])
        dst = skill_root / "assets" / asset["filename"]
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Bundled asset: {dst}")
        else:
            print(f"⚠️  Asset missing: {src}")

    # Package via skill-creator
    # SKILL_CREATOR overrides; otherwise a user-level install, then the copy the
    # official skill-creator plugin unpacks into the plugin cache (the usual case).
    skill_creator = find_skill_creator()
    if skill_creator.exists():
        result = subprocess.run(
            ["python3", "-m", "scripts.package_skill", str(skill_root.resolve()), str(output_dir.resolve())],
            cwd=str(skill_creator),
            capture_output=True, text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            print("⚠️  Packaging failed:", result.stderr)
            sys.exit(2)
    else:
        print(f"⚠️  skill-creator not found at {skill_creator}; skipping packaging step.")
        print("   Set SKILL_CREATOR to the skill-creator directory, or package manually with:")
        print(f'   cd "<skill-creator dir>" && python3 -m scripts.package_skill "{skill_root.resolve()}" "{output_dir.resolve()}"')

    final_skill = output_dir / f"{brand_slug}-brand.skill"
    print(f"\n✅ Built skill at: {skill_root}")
    if final_skill.exists():
        print(f"✅ Packaged to:    {final_skill}")


def find_skill_creator() -> Path:
    if os.environ.get("SKILL_CREATOR"):
        return Path(os.environ["SKILL_CREATOR"])
    user = Path.home() / ".claude/skills/skill-creator"
    if user.exists():
        return user
    cached = sorted(
        Path.home().glob(".claude/plugins/cache/*/skill-creator/*/skills/skill-creator"),
        key=lambda p: p.stat().st_mtime,
    )
    return cached[-1] if cached else user


if __name__ == "__main__":
    main()
