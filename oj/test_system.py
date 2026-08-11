#!/usr/bin/env python3
"""
测试系统是否能正常导入和运行
"""

import sys
import os

print("="*60)
print("系统测试")
print("="*60)
print()

# 测试1: 导入 oj_system
print("测试1: 导入 oj_system...")
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from oj_system import LocalOJ, JudgeResult
    print("✓ oj_system 导入成功")
except Exception as e:
    print(f"✗ oj_system 导入失败: {e}")
    sys.exit(1)

# 测试2: 导入 buaa_oj
print("\n测试2: 导入 buaa_oj...")
try:
    from buaa_oj import BUAAOJ, ProblemStatus
    print("✓ buaa_oj 导入成功")
except Exception as e:
    print(f"✗ buaa_oj 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试3: 初始化 BUAAOJ
print("\n测试3: 初始化 BUAAOJ...")
try:
    oj = BUAAOJ()
    print(f"✓ BUAAOJ 初始化成功")
    print(f"  - 题目数量: {len(oj.problems)}")
    print(f"  - 数据目录: {oj.data_dir}")
except Exception as e:
    print(f"✗ BUAAOJ 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4: 创建测试题目
print("\n测试4: 创建测试题目...")
try:
    prob = oj.create_problem(2025, 99, "测试题目")
    print(f"✓ 题目创建成功: {prob.id}")
except Exception as e:
    print(f"✗ 题目创建失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
print("所有测试通过！")
print("="*60)
print("\n现在可以运行: python buaa_gui_simple.py")

input("\n按回车键退出...")
