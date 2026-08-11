#!/usr/bin/env python3
"""Check unsolved/attempted problems:
1) whether standard solutions pass local testcases;
2) whether statement IO/sample likely mismatches testcase facts.
"""

from __future__ import annotations

import json
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OJ = ROOT / "oj"
YEARS_DIR = OJ / "data" / "years"
PROBLEMS_DIR = OJ / "problems"
SOLUTIONS_DIR = OJ / "solutions"
REPORT = ROOT / "未完成题质量检查报告_2026-03-10.md"
CHANGED_REPORT = ROOT / "未完成题质量检查报告_增量_2026-03-10.md"

import sys
sys.path.insert(0, str(OJ))
from oj_system import LocalOJ, JudgeResult  # type: ignore


@dataclass
class ProblemCheck:
    pid: str
    status: str
    has_solution: bool
    solution_is_placeholder: bool
    judge_passed: bool
    judge_detail: str
    io_issues: List[str]


def load_not_solved() -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for year_dir in sorted(YEARS_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for f in sorted(year_dir.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            status = data.get("status", "")
            # not solved = unsolved or attempted
            if status != "已解决":
                items.append((data["id"], status))
    return items


def load_status_map() -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for year_dir in sorted(YEARS_DIR.iterdir()):
        if not year_dir.is_dir():
            continue
        for f in sorted(year_dir.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            mapping[str(data["id"])] = str(data.get("status", ""))
    return mapping


def load_targets(ids_arg: str | None) -> List[Tuple[str, str]]:
    if not ids_arg:
        return load_not_solved()

    status_map = load_status_map()
    ids = [x.strip() for x in ids_arg.split(",") if x.strip()]
    seen = set()
    targets: List[Tuple[str, str]] = []
    for pid in ids:
        if pid in seen:
            continue
        seen.add(pid)
        targets.append((pid, status_map.get(pid, "指定")))
    return targets


def extract_section(md: str, heading: str) -> str:
    # capture text under '## heading' until next '## '
    pattern = rf"^##\s*{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)"
    m = re.search(pattern, md, flags=re.S | re.M)
    return m.group(1).strip() if m else ""


def extract_first_code_block(text: str) -> str:
    m = re.search(r"```\s*\n(.*?)```", text, flags=re.S)
    return m.group(1).strip() if m else ""


def has_decimal(text: str) -> bool:
    return bool(re.search(r"\d+\.\d+", text))


def io_checks(pid: str) -> List[str]:
    issues: List[str] = []
    pdir = PROBLEMS_DIR / pid
    md_file = pdir / "problem.md"
    if not md_file.exists():
        return ["missing problem.md"]

    md = md_file.read_text(encoding="utf-8", errors="replace")

    input_sec = extract_section(md, "输入格式")
    output_sec = extract_section(md, "输出格式")
    sample_in_sec = extract_section(md, "样例输入")
    sample_out_sec = extract_section(md, "样例输出")

    for sec_name, sec in (("输入格式", input_sec), ("输出格式", output_sec), ("样例输入", sample_in_sec), ("样例输出", sample_out_sec)):
        if not sec:
            issues.append(f"missing section: {sec_name}")
        if "TODO" in sec:
            issues.append(f"section has TODO placeholder: {sec_name}")

    tc_in = pdir / "testcases" / "1.in"
    tc_out = pdir / "testcases" / "1.out"
    if tc_in.exists() and sample_in_sec:
        sample_in = extract_first_code_block(sample_in_sec)
        if sample_in:
            if sample_in.strip() != tc_in.read_text(encoding="utf-8", errors="replace").strip():
                issues.append("sample input != testcase 1.in")
    if tc_out.exists() and sample_out_sec:
        sample_out = extract_first_code_block(sample_out_sec)
        if sample_out:
            if sample_out.strip() != tc_out.read_text(encoding="utf-8", errors="replace").strip():
                issues.append("sample output != testcase 1.out")

    # light type-consistency heuristics
    tc_in_txt = tc_in.read_text(encoding="utf-8", errors="replace") if tc_in.exists() else ""
    tc_out_txt = tc_out.read_text(encoding="utf-8", errors="replace") if tc_out.exists() else ""

    if has_decimal(tc_in_txt) and ("整数" in input_sec and "浮点" not in input_sec):
        issues.append("input section says integer but testcase input has decimal")
    if has_decimal(tc_out_txt) and ("整数" in output_sec and "浮点" not in output_sec and "小数" not in output_sec):
        issues.append("output section says integer but testcase output has decimal")

    return issues


def judge_solution(oj: LocalOJ, pid: str) -> Tuple[bool, bool, bool, str]:
    sol = SOLUTIONS_DIR / f"{pid}_solution.cpp"
    if not sol.exists():
        return False, False, False, "missing standard solution file"

    txt = sol.read_text(encoding="utf-8", errors="replace")
    placeholder = "TODO: Replace this placeholder" in txt

    try:
        results = oj.judge(pid, str(sol))
    except Exception as e:
        return True, placeholder, False, f"judge exception: {e}"

    if not results:
        return True, placeholder, False, "no judge results"

    passed = all(r.result == JudgeResult.AC for r in results)
    if passed:
        return True, placeholder, True, f"AC {len(results)}/{len(results)}"

    first_fail = next((r for r in results if r.result != JudgeResult.AC), results[0])
    return True, placeholder, False, f"failed at test {first_fail.test_case_num}: {first_fail.result.value}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated problem ids to check")
    args = parser.parse_args()

    report_path = CHANGED_REPORT if args.ids else REPORT

    oj = LocalOJ(str(OJ))
    targets = load_targets(args.ids)

    checks: List[ProblemCheck] = []
    for pid, status in targets:
        has_sol, is_placeholder, passed, detail = judge_solution(oj, pid)
        issues = io_checks(pid)
        checks.append(ProblemCheck(
            pid=pid,
            status=status,
            has_solution=has_sol,
            solution_is_placeholder=is_placeholder,
            judge_passed=passed,
            judge_detail=detail,
            io_issues=issues,
        ))

    total = len(checks)
    sol_pass = sum(1 for c in checks if c.has_solution and c.judge_passed)
    sol_fail = sum(1 for c in checks if c.has_solution and not c.judge_passed)
    no_sol = sum(1 for c in checks if not c.has_solution)
    with_io_issue = sum(1 for c in checks if c.io_issues)

    lines: List[str] = []
    lines.append("# 未完成题质量检查报告（2026-03-10）")
    lines.append("")
    lines.append(f"- 检查题目数: {total}")
    lines.append(f"- 标答通过: {sol_pass}")
    lines.append(f"- 标答失败: {sol_fail}")
    lines.append(f"- 缺少标答: {no_sol}")
    lines.append(f"- IO/样例说明疑似问题: {with_io_issue}")
    lines.append("")
    lines.append("## 逐题结果")
    lines.append("")

    for c in checks:
        lines.append(f"### {c.pid} ({c.status})")
        lines.append(f"- 标答文件: {'有' if c.has_solution else '无'}")
        if c.has_solution:
            lines.append(f"- 标答是否占位: {'是' if c.solution_is_placeholder else '否'}")
            lines.append(f"- 判题结果: {'通过' if c.judge_passed else '失败'} ({c.judge_detail})")
        if c.io_issues:
            lines.append("- IO检查问题:")
            for issue in c.io_issues:
                lines.append(f"  - {issue}")
        else:
            lines.append("- IO检查问题: 无明显问题")
        lines.append("")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Checked {total} not-solved problems")
    print(f"solution pass/fail/no-solution: {sol_pass}/{sol_fail}/{no_sol}")
    print(f"IO issue count: {with_io_issue}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
