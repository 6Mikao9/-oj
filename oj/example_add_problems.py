#!/usr/bin/env python3
"""
示例：如何添加北航复试题目
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from buaa_oj import BUAAOJ

def main():
    oj = BUAAOJ()
    
    print("="*60)
    print("BUAA OJ - Add Problems Example")
    print("="*60)
    print()
    
    # 示例：添加 2017 年的题目
    # 实际使用时，你需要把题目图片发给我，我会帮你提取信息和创建测试用例
    
    print("Creating sample problems for 2017...")
    print()
    
    # 题目1
    prob1 = oj.create_problem(2017, 1, "字符串处理", "基础字符串操作题目")
    oj.add_test_case(prob1.id, "hello\n", "olleh\n")
    oj.add_test_case(prob1.id, "12345\n", "54321\n")
    print(f"✓ Created: {prob1.id}")
    
    # 题目2
    prob2 = oj.create_problem(2017, 2, "数组排序", "排序算法练习")
    oj.add_test_case(prob2.id, "5\n3 1 4 1 5\n", "1 1 3 4 5\n")
    print(f"✓ Created: {prob2.id}")
    
    # 题目3
    prob3 = oj.create_problem(2017, 3, "简单模拟", "按照规则模拟过程")
    oj.add_test_case(prob3.id, "3 3\n", "9\n")
    print(f"✓ Created: {prob3.id}")
    
    print()
    print("="*60)
    print("Sample problems created!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Run: python buaa_gui.py")
    print("2. Or run: python buaa_oj.py list")
    print()
    print("When you have real problems:")
    print("- Send me the problem images")
    print("- I'll help you create test cases")
    print("- You can practice and submit solutions")

if __name__ == "__main__":
    main()
