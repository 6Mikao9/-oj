#!/usr/bin/env python3
"""Quality guard for BUAA OJ repository.

Modes:
- quick: static checks on unsolved/attempted problems.
- full: run quick checks + full judge/doc audit via check_unsolved_quality.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OJ = ROOT / "oj"
YEARS_DIR = OJ / "data" / "years"
PROBLEMS_DIR = OJ / "problems"
SOLUTIONS_DIR = OJ / "solutions"
FULL_REPORT = ROOT / "未完成题质量检查报告_2026-03-10.md"
CHANGED_FULL_REPORT = ROOT / "未完成题质量检查报告_增量_2026-03-10.md"

REQ_HEADINGS = ["输入格式", "输出格式", "样例输入", "样例输出"]


@dataclass
class Issue:
    kind: str
    path: str
    detail: str


def load_unsolved_ids() -> List[str]:
    ids: List[str] = []
    for year_dir in sorted(YEARS_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for f in sorted(year_dir.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("status") != "已解决":
                ids.append(str(data["id"]))
    return ids


def _run_git_name_only(args: List[str]) -> List[str]:
    try:
        out = subprocess.check_output(args, cwd=str(ROOT), stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return []
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def _run_git_status_paths() -> List[str]:
    try:
        out = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return []

    paths: List[str] = []
    for line in out.splitlines():
        if len(line) < 4:
            continue
        p = line[3:]
        if " -> " in p:
            p = p.split(" -> ", 1)[1]
        p = p.strip().replace("\\", "/")
        if p:
            paths.append(p)
    return paths


def load_changed_problem_ids(include_unstaged: bool = False) -> List[str]:
    paths = set()
    for cmd in (["git", "diff", "--name-only", "--cached"],):
        for p in _run_git_name_only(cmd):
            paths.add(p)
    if include_unstaged:
        for p in _run_git_name_only(["git", "diff", "--name-only"]):
            paths.add(p)
        for p in _run_git_status_paths():
            paths.add(p)

    ids = set()
    for p in paths:
        m = re.match(r"^oj/problems/([^/]+)/", p)
        if m:
            ids.add(m.group(1))
            continue

        m = re.match(r"^oj/solutions/([^/]+)_solution\.cpp$", p)
        if m:
            ids.add(m.group(1))
            continue

        m = re.match(r"^oj/data/years/\d{4}/([^/]+)\.json$", p)
        if m:
            ids.add(m.group(1))

    valid = []
    for pid in sorted(ids):
        has_problem = (PROBLEMS_DIR / pid).exists()
        has_solution = (SOLUTIONS_DIR / f"{pid}_solution.cpp").exists()
        has_meta = any((YEARS_DIR / y / f"{pid}.json").exists() for y in [d.name for d in YEARS_DIR.iterdir() if d.is_dir()])
        if has_problem or has_solution or has_meta:
            valid.append(pid)
    return valid


def extract_section(md: str, heading: str) -> str:
    m = re.search(rf"^##\s*{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", md, flags=re.S | re.M)
    return m.group(1).strip() if m else ""


def extract_first_code_block(text: str) -> str:
    m = re.search(r"```\s*\n(.*?)```", text, flags=re.S)
    return m.group(1).strip() if m else ""


def run_quick(target_ids: List[str]) -> Tuple[int, List[Issue]]:
    issues: List[Issue] = []

    for pid in target_ids:
        pmd = PROBLEMS_DIR / pid / "problem.md"
        sol = SOLUTIONS_DIR / f"{pid}_solution.cpp"

        if not pmd.exists():
            issues.append(Issue("doc", str(pmd), "missing problem.md"))
            continue

        md = pmd.read_text(encoding="utf-8", errors="replace")
        for h in REQ_HEADINGS:
            sec = extract_section(md, h)
            if not sec:
                issues.append(Issue("doc", str(pmd), f"missing section: {h}"))
            elif "TODO" in sec:
                issues.append(Issue("doc", str(pmd), f"TODO found in section: {h}"))

        tc_in = PROBLEMS_DIR / pid / "testcases" / "1.in"
        tc_out = PROBLEMS_DIR / pid / "testcases" / "1.out"
        in_sec = extract_section(md, "样例输入")
        out_sec = extract_section(md, "样例输出")

        if tc_in.exists() and in_sec:
            sample_in = extract_first_code_block(in_sec)
            if sample_in and sample_in.strip() != tc_in.read_text(encoding="utf-8", errors="replace").strip():
                issues.append(Issue("doc", str(pmd), "sample input != testcase 1.in"))
        if tc_out.exists() and out_sec:
            sample_out = extract_first_code_block(out_sec)
            if sample_out and sample_out.strip() != tc_out.read_text(encoding="utf-8", errors="replace").strip():
                issues.append(Issue("doc", str(pmd), "sample output != testcase 1.out"))

        if not sol.exists():
            issues.append(Issue("solution", str(sol), "missing standard solution"))
        else:
            txt = sol.read_text(encoding="utf-8", errors="replace")
            if "TODO: Replace this placeholder" in txt:
                issues.append(Issue("solution", str(sol), "placeholder solution detected"))

    return (0 if not issues else 1), issues


def run_full(target_ids: List[str], scope: str) -> Tuple[int, List[Issue]]:
    code, issues = run_quick(target_ids)
    if scope == "changed" and not target_ids:
        return 0, issues

    py = sys.executable
    cmd = [py, str(ROOT / "scripts" / "check_unsolved_quality.py")]
    if scope == "changed":
        cmd.extend(["--ids", ",".join(target_ids)])
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode != 0:
        issues.append(Issue("full", "scripts/check_unsolved_quality.py", "script execution failed"))
        return 1, issues

    report_path = CHANGED_FULL_REPORT if scope == "changed" else FULL_REPORT
    if report_path.exists():
        report = report_path.read_text(encoding="utf-8", errors="replace")
        if "- 标答失败: 0" not in report:
            issues.append(Issue("full", str(report_path), "non-zero solution failures in report"))
        if "- IO/样例说明疑似问题: 0" not in report:
            issues.append(Issue("full", str(report_path), "non-zero io issues in report"))
    else:
        issues.append(Issue("full", str(report_path), "full report missing"))

    return (0 if not issues else 1), issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["quick", "full"], default="quick")
    parser.add_argument("--scope", choices=["all", "changed"], default="all")
    parser.add_argument(
        "--changed-source",
        choices=["staged", "all"],
        default="staged",
        help="when scope=changed, use only staged changes or include unstaged/untracked",
    )
    args = parser.parse_args()

    if args.scope == "all":
        target_ids = load_unsolved_ids()
    else:
        target_ids = load_changed_problem_ids(include_unstaged=(args.changed_source == "all"))

    if args.scope == "changed" and not target_ids:
        print("[QUALITY GUARD] PASSED")
        print("- [info] no changed problems detected")
        return 0

    if args.mode == "quick":
        code, issues = run_quick(target_ids)
    else:
        code, issues = run_full(target_ids, args.scope)

    if issues:
        print("[QUALITY GUARD] FAILED")
        for it in issues:
            print(f"- [{it.kind}] {it.path}: {it.detail}")
    else:
        print("[QUALITY GUARD] PASSED")

    return code


if __name__ == "__main__":
    raise SystemExit(main())
