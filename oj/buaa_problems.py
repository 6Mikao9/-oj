#!/usr/bin/env python3
"""
北航研究生复试上机题目合集
你可以把题目图片发给我，我会帮你构建测试用例
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oj_system import LocalOJ

def create_buaa_problem(problem_id, title, description=""):
    """创建北航复试题目"""
    oj = LocalOJ()
    return oj.create_problem(problem_id, title, description)

def add_buaa_testcase(problem_id, input_data, output_data):
    """添加测试用例"""
    oj = LocalOJ()
    return oj.add_test_case(problem_id, input_data, output_data)

# ==================== 题目模板 ====================

# 题目1: 字符串处理
def setup_string_problem():
    """字符串处理示例题目"""
    create_buaa_problem("buaa_string", "字符串处理", "基础字符串操作")
    
    # 测试用例1
    add_buaa_testcase("buaa_string", 
        "hello world\n",
        "dlrow olleh\n")
    
    # 测试用例2
    add_buaa_testcase("buaa_string",
        "12345\n",
        "54321\n")

# 题目2: 数组排序
def setup_sort_problem():
    """排序题目"""
    create_buaa_problem("buaa_sort", "数组排序", "基础排序算法")
    
    add_buaa_testcase("buaa_sort",
        "5\n3 1 4 1 5\n",
        "1 1 3 4 5\n")
    
    add_buaa_testcase("buaa_sort",
        "3\n9 8 7\n",
        "7 8 9\n")

# 题目3: 简单模拟
def setup_simulation_problem():
    """模拟题目"""
    create_buaa_problem("buaa_simulation", "简单模拟", "按照规则模拟过程")
    
    add_buaa_testcase("buaa_simulation",
        "3 3\n1 2 3\n",
        "6\n")

# ==================== 使用说明 ====================

HELP_TEXT = """
北航复试 OJ 系统使用说明
========================

1. 当你有新的题目图片时：
   - 把图片发给我
   - 我会帮你分析题目要求
   - 构建测试用例
   - 你可以在本系统练习

2. 常用命令：
   - 创建题目: python buaa_problems.py create <id> <title>
   - 添加测试: 编辑本文件，添加测试用例
   - 评测代码: python oj_system.py judge <id> <code.cpp>

3. 目录结构：
   oj/
   ├── problems/          # 所有题目
   │   ├── tamworth_two/  # 示例题目
   │   └── buaa_xxx/      # 北航题目
   ├── oj_system.py       # 评测核心
   ├── oj_gui.py          # 图形界面
   └── 启动OJ.bat         # 快速启动

4. 复试准备建议：
   - 每天练习2-3道题目
   - 熟悉常用算法模板
   - 注意输入输出格式
   - 控制代码运行时间
"""

def show_help():
    print(HELP_TEXT)

def setup_all():
    """初始化所有示例题目"""
    print("正在创建示例题目...")
    setup_string_problem()
    setup_sort_problem()
    setup_simulation_problem()
    print("\n所有题目创建完成！")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_help()
        print("\n可用命令:")
        print("  python buaa_problems.py setup    - 创建所有示例题目")
        print("  python buaa_problems.py help     - 显示帮助")
        print("  python buaa_problems.py list     - 列出所有题目")
    else:
        cmd = sys.argv[1]
        if cmd == "setup":
            setup_all()
        elif cmd == "help":
            show_help()
        elif cmd == "list":
            oj = LocalOJ()
            oj.list_problems()
        else:
            print(f"未知命令: {cmd}")
