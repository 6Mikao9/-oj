#!/usr/bin/env python3
"""
直接创建测试用例
"""

import os
import json
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    
    # 创建题目目录
    problem_dir = base_dir / "problems" / "tamworth_two"
    testcase_dir = problem_dir / "testcases"
    testcase_dir.mkdir(parents=True, exist_ok=True)
    
    # 样例输入
    sample_input = """*...*.....
......*...
...*...*..
..........
...*.F....
*.....*...
...*......
..C......*
...*.*....
.*.*......"""
    
    # 样例输出
    sample_output = "49\n"
    
    # 保存测试用例
    with open(testcase_dir / "1.in", 'w', encoding='utf-8') as f:
        f.write(sample_input)
    
    with open(testcase_dir / "1.out", 'w', encoding='utf-8') as f:
        f.write(sample_output)
    
    # 创建 info.json
    info = {
        "id": "tamworth_two",
        "title": "Two Tamworth Cows",
        "time_limit": 1000,
        "memory_limit": 65536,
        "test_cases": [1]
    }
    
    with open(problem_dir / "info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2)
    
    print("Test case created successfully!")
    print(f"Problem directory: {problem_dir}")
    print(f"Test case: {testcase_dir / '1.in'}")
    print(f"Expected output: {testcase_dir / '1.out'}")

if __name__ == "__main__":
    main()
