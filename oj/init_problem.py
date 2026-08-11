#!/usr/bin/env python3
"""
快速创建题目和测试用例
"""

import os
import json
from pathlib import Path

def create_problem(problem_id, title=""):
    """创建题目目录结构"""
    base_dir = Path(__file__).parent
    problem_dir = base_dir / "problems" / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 info.json
    info = {
        "id": problem_id,
        "title": title,
        "time_limit": 1000,
        "memory_limit": 65536,
        "test_cases": []
    }
    
    with open(problem_dir / "info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    # 创建测试用例目录
    (problem_dir / "testcases").mkdir(exist_ok=True)
    
    print(f"✓ 题目 '{problem_id}' 创建成功！")
    print(f"  目录: {problem_dir}")
    return problem_dir

def add_test_case(problem_id, case_num, input_data, output_data):
    """添加测试用例"""
    base_dir = Path(__file__).parent
    testcase_dir = base_dir / "problems" / problem_id / "testcases"
    testcase_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存输入输出
    with open(testcase_dir / f"{case_num}.in", 'w', encoding='utf-8') as f:
        f.write(input_data)
    with open(testcase_dir / f"{case_num}.out", 'w', encoding='utf-8') as f:
        f.write(output_data)
    
    # 更新 info.json
    info_file = base_dir / "problems" / problem_id / "info.json"
    if info_file.exists():
        with open(info_file, 'r', encoding='utf-8') as f:
            info = json.load(f)
        if case_num not in info.get("test_cases", []):
            info.setdefault("test_cases", []).append(case_num)
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 测试用例 {case_num} 添加成功！")

if __name__ == "__main__":
    # 创建示例题目：两只塔姆沃斯牛
    create_problem("tamworth_two", "两只塔姆沃斯牛")
    
    # 样例测试
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
    
    sample_output = "49\n"
    
    add_test_case("tamworth_two", 1, sample_input, sample_output)
    
    print("\n" + "="*50)
    print("初始化完成！")
    print("="*50)
    print("\n使用方法:")
    print("1. 命令行评测:")
    print("   python oj_system.py judge tamworth_two 你的代码.cpp")
    print("\n2. 图形界面:")
    print("   python oj_gui.py")
    print("\n3. 添加新测试用例:")
    print("   编辑本文件，添加更多 add_test_case 调用")
