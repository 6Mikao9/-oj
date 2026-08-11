#!/usr/bin/env python3
"""
创建示例题目：USACO 两只塔姆沃斯牛
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oj_system import LocalOJ

def main():
    oj = LocalOJ()
    
    # 创建题目
    print("创建题目: tamworth_two")
    oj.create_problem("tamworth_two", "两只塔姆沃斯牛", "USACO 2.4 经典题目")
    
    # 添加样例测试用例
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
    
    sample_output = """49"""
    
    print("\n添加样例测试用例...")
    oj.add_test_case("tamworth_two", sample_input, sample_output)
    
    # 添加更多测试用例（可以手动添加更多边界情况）
    # 测试用例 2：简单情况
    test2_input = """..........
..........
..........
..........
....F.....
..........
..........
....C.....
..........
.........."""
    
    test2_output = """3"""
    
    print("添加测试用例 2...")
    oj.add_test_case("tamworth_two", test2_input, test2_output)
    
    print("\n题目创建完成！")
    print("\n使用方法:")
    print("1. 命令行: python oj_system.py judge tamworth_two 你的代码.cpp")
    print("2. 图形界面: python oj_gui.py")

if __name__ == "__main__":
    main()
