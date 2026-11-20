# -*- coding: utf-8 -*-
"""
verify_pages_deploy_ready.py
Regression checks preventing GitHub Pages Jekyll/Liquid syntax errors and workflow artifact failures:
1. Empty `.nojekyll` marker exists at repo root so legacy branch Pages skips Jekyll.
2. All tracked Markdown files keep `{{` / `{%` directives escaped inside `{% raw %}...{% endraw %}`.
3. `.github/workflows/deploy.yml` stages only static web files + `.nojekyll` (excluding docs/scripts)
   and splits `build` -> `deploy` jobs using Node 24 Pages actions to prevent artifact-index races.
"""

import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# Strip balanced {% raw %}...{% endraw %} (including optional HTML comments wrapping them)
RAW_OPEN_RE = re.compile(r"\{%-?\s*raw\s*-?%\}")
RAW_CLOSE_RE = re.compile(r"\{%-?\s*endraw\s*-?%\}")
RAW_BLOCK_RE = re.compile(r"(?:<!--\s*)?\{%-?\s*raw\s*-?%\}(?:[\s\S]*?)\{%-?\s*endraw\s*-?%\}(?:\s*-->)?")
LIQUID_TOKEN_RE = re.compile(r"(\{\{|\{%)")


def find_unescaped_liquid_in_markdown(root: Path) -> list[str]:
    issues = []
    tracked = subprocess.check_output(
        ["git", "ls-files", "*.md", "**/*.md"],
        cwd=root,
        text=True,
        encoding="utf-8",
    ).splitlines()

    for rel in sorted(set(tracked)):
        p = root / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        raw_opens = len(RAW_OPEN_RE.findall(text))
        raw_closes = len(RAW_CLOSE_RE.findall(text))
        if raw_opens != raw_closes:
            issues.append(f"{rel}: unbalanced raw/endraw tags (open={raw_opens}, close={raw_closes})")
        # Replace raw blocks with equal-line placeholder so line numbers remain exact
        sanitized = RAW_BLOCK_RE.sub(
            lambda m: "\n" * m.group(0).count("\n"),
            text,
        )
        for lineno, line in enumerate(sanitized.splitlines(), 1):
            if LIQUID_TOKEN_RE.search(line):
                issues.append(f"{rel}:{lineno}: unescaped Liquid syntax outside {{% raw %}}: {line.strip()[:100]}")
    return issues


def verify_deploy_workflow(workflow_path: Path) -> list[str]:
    failures = []
    if not workflow_path.exists():
        return [".github/workflows/deploy.yml: file missing"]

    yml = workflow_path.read_text(encoding="utf-8")

    if re.search(r"path:\s*['\"]?\.['\"]?\s*$", yml, re.MULTILINE):
        failures.append("deploy.yml: must stage static site files (not raw path: '.')")

    required_tokens = [
        ("actions/checkout@v7", "must use actions/checkout@v7"),
        ("actions/configure-pages@v6", "must use actions/configure-pages@v6"),
        ("actions/upload-pages-artifact@v5", "must use actions/upload-pages-artifact@v5"),
        ("actions/deploy-pages@v5", "must use actions/deploy-pages@v5"),
        ("include-hidden-files: 'true'", "must enable include-hidden-files so .nojekyll stays in artifact"),
        ("needs: build", "deploy job must run after build job (needs: build) to avoid artifact race"),
        (".nojekyll", "staging step must copy .nojekyll into artifact directory"),
    ]
    for token, msg in required_tokens:
        if token not in yml:
            failures.append(f"deploy.yml: {msg}")

    for asset_dir in ("index.html", "admin", "pages", "css", "js", "assets"):
        if asset_dir not in yml:
            failures.append(f"deploy.yml: missing static web entry '{asset_dir}' in staging copy")

    return failures


def main() -> int:
    failures = []

    nojekyll = ROOT / ".nojekyll"
    if not nojekyll.exists() or not nojekyll.is_file():
        failures.append(".nojekyll: missing empty marker file at repository root")

    failures.extend(find_unescaped_liquid_in_markdown(ROOT))
    failures.extend(verify_deploy_workflow(ROOT / ".github" / "workflows" / "deploy.yml"))

    if failures:
        print("FAIL:")
        for item in failures:
            print(f" - {item}")
        return 1

    print("ALL CHECKS PASSED: GitHub Pages .nojekyll, Liquid-safe docs, and deploy workflow verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
