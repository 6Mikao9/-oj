#!/usr/bin/env python3
"""
同步2017-2019年题目到BUAAOJ系统
将problems目录中的problem.md转换为data/years目录中的JSON文件
"""

import os
import json
from pathlib import Path

# 项目根目录
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = BASE_DIR / "problems"
DATA_YEARS_DIR = BASE_DIR / "data" / "years"

# 年份范围
years_to_sync = [2017, 2018, 2019, 2021, 2022, 2023]

def parse_problem_md(file_path):
    """解析problem.md文件，提取完整的题目信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    
    # 提取题目ID和标题
    if lines and lines[0].startswith('# '):
        title_line = lines[0][2:].strip()
        if ': ' in title_line:
            problem_id, title = title_line.split(': ', 1)
            problem_id = problem_id.strip()
            title = title.strip()
        else:
            problem_id = title_line
            title = title_line
    else:
        problem_id = os.path.basename(os.path.dirname(file_path))
        title = problem_id
    
    # 提取年份
    if '_' in problem_id:
        year_str = problem_id.split('_')[0]
        if year_str.isdigit():
            year = int(year_str)
        else:
            year = 2025
    else:
        year = 2025
    
    # 提取完整的题目描述（包括输入输出格式和样例）
    description_parts = []
    skip_until_next_section = False
    
    for line in lines[1:]:
        # 跳过空标题行
        if line.startswith('## ') and not line[3:].strip():
            continue
        
        # 遇到新的大节，添加分隔
        if line.startswith('## ') and description_parts:
            description_parts.append('\n')
        
        description_parts.append(line)
    
    description_text = '\n'.join(description_parts).strip()
    
    # 如果没有详细描述，使用基本信息
    if not description_text:
        description_text = f"Problem: {title}\n\n"
        description_text += "Please solve this problem.\n\n"
        description_text += f"Input format: See problem.md\n"
        description_text += f"Output format: See problem.md"
    
    return {
        'id': problem_id,
        'year': year,
        'title': title,
        'description': description_text
    }

def sync_year(year):
    """同步指定年份的题目"""
    year_str = str(year)
    year_dir = PROBLEMS_DIR / f"{year_str}_1"
    
    if not year_dir.exists():
        print(f"Year {year} not found in problems directory")
        return
    
    # 获取该年份的所有题目
    year_problems = []
    for i in range(1, 10):  # 假设每年最多9道题
        problem_dir = PROBLEMS_DIR / f"{year_str}_{i}"
        if problem_dir.exists():
            problem_md = problem_dir / "problem.md"
            if problem_md.exists():
                problem_info = parse_problem_md(problem_md)
                year_problems.append(problem_info)
                print(f"Found problem: {problem_info['id']} - {problem_info['title']}")
    
    if not year_problems:
        print(f"No problems found for year {year}")
        return
    
    # 创建目标年份目录
    target_year_dir = DATA_YEARS_DIR / year_str
    target_year_dir.mkdir(exist_ok=True)
    
    # 保存为JSON文件
    for problem in year_problems:
        json_file = target_year_dir / f"{problem['id']}.json"
        
        # 构建完整的题目数据
        problem_data = {
            'id': problem['id'],
            'year': problem['year'],
            'title': problem['title'],
            'description': problem['description'],
            'status': '未解决',
            'submissions': [],
            'solution_file': None,
            'notes': '',
            'tags': [],
            'is_favorite': False,
            'annotation': ''
        }
        
        # 保存JSON文件
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(problem_data, f, ensure_ascii=False, indent=2)
        
        print(f"Created JSON file: {json_file}")
        
        # 同时在oj_system中创建题目
        from oj_system import LocalOJ
        oj = LocalOJ()
        oj.create_problem(problem['id'], problem['title'], problem['description'])
        print(f"Created problem in oj_system: {problem['id']}")

def main():
    print("Syncing 2017-2019 problems to BUAAOJ system...")
    
    for year in years_to_sync:
        print(f"\n=== Syncing year {year} ===")
        sync_year(year)
    
    print("\n=== Sync completed ===")
    print("Problems should now be visible in the GUI.")

if __name__ == "__main__":
    main()
