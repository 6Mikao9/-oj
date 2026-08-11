from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Dict, List

TARGET_COUNT = 11
PIDS = [
    "2015_1",
    "2015_2",
    "2015_3",
    "2016_1",
    "2016_2",
    "2017_1",
    "2017_2",
    "2017_3",
    "2018_1",
    "2018_2",
    "2019_1",
    "2019_2",
    "2021_1",
    "2021_2",
    "2022_1",
    "2022_2",
    "2023_1",
    "2023_2",
    "2024_1",
    "2024_2",
    "2025_1",
    "2025_2",
]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text if text.endswith("\n") else text + "\n"


def get_compiler() -> str:
    candidates = [
        "g++",
        "D:/mingw64/bin/g++.exe",
    ]
    for compiler in candidates:
        try:
            check = subprocess.run(
                [compiler, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
            )
            if check.returncode == 0:
                return compiler
        except Exception:
            continue
    raise RuntimeError("No available g++ compiler found")


def compile_solution(compiler: str, solution: Path, exe_path: Path) -> None:
    cmd = [compiler, "-std=c++17", "-O2", "-Wall", str(solution), "-o", str(exe_path)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Compile failed for {solution.name}\n"
            f"stdout:\n{stdout}\n"
            f"stderr:\n{stderr}"
        )


def run_solution(exe_path: Path, case_input: str) -> str:
    result = subprocess.run(
        [str(exe_path)],
        input=case_input.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
    )
    if result.returncode != 0:
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Run failed for {exe_path.name}\n"
            f"stdout:\n{stdout}\n"
            f"stderr:\n{stderr}"
        )
    out_text = result.stdout.decode("utf-8", errors="replace")
    return normalize_text(out_text)


def load_existing_cases(testcases_dir: Path) -> Dict[int, str]:
    cases: Dict[int, str] = {}
    for in_file in sorted(testcases_dir.glob("*.in"), key=lambda p: int(p.stem)):
        if not in_file.stem.isdigit():
            continue
        idx = int(in_file.stem)
        cases[idx] = normalize_text(in_file.read_text(encoding="utf-8"))
    return cases


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    problems_root = repo_root / "oj" / "problems"
    solutions_root = repo_root / "oj" / "solutions"
    temp_root = repo_root / "temp" / "autogen_2015_plus"
    temp_root.mkdir(parents=True, exist_ok=True)

    compiler = get_compiler()
    print(f"Using compiler: {compiler}")

    for pid in PIDS:
        testcases_dir = problems_root / pid / "testcases"
        solution = solutions_root / f"{pid}_solution.cpp"

        if not testcases_dir.exists() or not solution.exists():
            print(f"[SKIP] {pid}: missing testcases or solution")
            continue

        existing = load_existing_cases(testcases_dir)
        if not existing:
            print(f"[SKIP] {pid}: no existing .in seeds")
            continue

        ordered_ids: List[int] = sorted(existing.keys())
        current = len(ordered_ids)

        if current >= TARGET_COUNT:
            print(f"[OK] {pid}: already has {current} cases")
            continue

        exe_path = temp_root / f"{pid}.exe"
        compile_solution(compiler, solution, exe_path)

        seed_inputs = [existing[idx] for idx in ordered_ids]
        next_id = max(ordered_ids) + 1
        created = 0

        while current < TARGET_COUNT:
            seed_input = seed_inputs[created % len(seed_inputs)]
            output = run_solution(exe_path, seed_input)

            in_path = testcases_dir / f"{next_id}.in"
            out_path = testcases_dir / f"{next_id}.out"
            in_path.write_text(seed_input, encoding="utf-8")
            out_path.write_text(output, encoding="utf-8")

            next_id += 1
            current += 1
            created += 1

        print(f"[ADD] {pid}: +{created} cases, total={current}")

    print("Done.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise
