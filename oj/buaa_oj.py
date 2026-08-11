#!/usr/bin/env python3
"""
北航复试 OJ 系统 - 增强版
支持年份组织、提交记录、题解管理
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, fields
from typing import List, Dict, Optional
from enum import Enum

# 添加原 OJ 系统
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oj_system import LocalOJ, JudgeResult, JudgeStatus

class ProblemStatus(Enum):
    UNSOLVED = "未解决"
    ATTEMPTED = "尝试中"
    SOLVED = "已解决"
    REVIEWED = "已审阅"

@dataclass
class Submission:
    """提交记录"""
    id: str
    timestamp: str
    code_file: str
    result: str
    passed: int
    total: int
    time_used: float
    notes: str = ""  # 备注

@dataclass
class Problem:
    """题目信息"""
    id: str
    year: int
    title: str
    description: str
    status: ProblemStatus
    submissions: List[Submission]
    solution_file: Optional[str]  # 最终题解
    notes: str  # 学习笔记
    tags: List[str]  # 标签
    is_favorite: bool = False  # 是否收藏
    annotation: str = ""  # 题目批注

class BUAAOJ:
    """北航 OJ 管理系统"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / "data"
        self.years_dir = self.data_dir / "years"
        self.submissions_dir = self.data_dir / "submissions"
        self.solutions_dir = self.data_dir / "solutions"
        
        # 创建目录
        self.data_dir.mkdir(exist_ok=True)
        self.years_dir.mkdir(exist_ok=True)
        self.submissions_dir.mkdir(exist_ok=True)
        self.solutions_dir.mkdir(exist_ok=True)
        
        # 初始化原 OJ
        self.oj = LocalOJ()
        
        # 加载数据
        self.problems: Dict[str, Problem] = {}
        self.load_all_problems()
    
    def load_all_problems(self):
        """加载所有题目"""
        for year_dir in self.years_dir.iterdir():
            if year_dir.is_dir():
                year = int(year_dir.name)
                for prob_file in year_dir.glob("*.json"):
                    with open(prob_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        problem = Problem(
                            id=data['id'],
                            year=data['year'],
                            title=data['title'],
                            description=data['description'],
                            status=ProblemStatus(data['status']),
                            submissions=[Submission(**s) for s in data.get('submissions', [])],
                            solution_file=data.get('solution_file'),
                            notes=data.get('notes', ''),
                            tags=data.get('tags', []),
                            is_favorite=data.get('is_favorite', False),
                            annotation=data.get('annotation', '')
                        )
                        self.problems[problem.id] = problem

    def reload_all_problems(self):
        """重新从磁盘加载题目，支持 GUI 热更新。"""
        self.problems.clear()
        self.load_all_problems()
    
    def save_problem(self, problem: Problem):
        """保存题目信息"""
        year_dir = self.years_dir / str(problem.year)
        year_dir.mkdir(exist_ok=True)
        
        data = {
            'id': problem.id,
            'year': problem.year,
            'title': problem.title,
            'description': problem.description,
            'status': problem.status.value,
            'submissions': [asdict(s) for s in problem.submissions],
            'solution_file': problem.solution_file,
            'notes': problem.notes,
            'tags': problem.tags,
            'is_favorite': problem.is_favorite,
            'annotation': problem.annotation
        }
        
        with open(year_dir / f"{problem.id}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_problem(self, year: int, problem_num: int, title: str, description: str = "") -> Problem:
        """创建新题目"""
        problem_id = f"{year}_{problem_num}"
        
        problem = Problem(
            id=problem_id,
            year=year,
            title=title,
            description=description,
            status=ProblemStatus.UNSOLVED,
            submissions=[],
            solution_file=None,
            notes="",
            tags=[]
        )
        
        self.problems[problem_id] = problem
        self.save_problem(problem)
        
        # 同时在原 OJ 中创建题目
        self.oj.create_problem(problem_id, title, description)
        
        print(f"Created problem: {problem_id} - {title}")
        return problem
    
    def add_test_case(self, problem_id: str, input_data: str, output_data: str, case_id: int = None):
        """添加测试用例"""
        return self.oj.add_test_case(problem_id, input_data, output_data, case_id)
    
    def submit(self, problem_id: str, code_file: str, notes: str = "") -> List[JudgeStatus]:
        """提交代码"""
        if problem_id not in self.problems:
            print(f"Error: Problem {problem_id} not found!")
            return []
        
        problem = self.problems[problem_id]
        
        # 运行评测
        print(f"\n{'='*60}")
        print(f"Submitting: {problem_id} - {problem.title}")
        print(f"{'='*60}\n")
        
        results = self.oj.judge(problem_id, code_file)
        
        # 统计结果
        passed = sum(1 for r in results if r.result == JudgeResult.AC)
        total = len(results)
        avg_time = sum(r.time_used for r in results) / len(results) if results else 0
        
        # 生成提交ID
        submission_id = f"{problem_id}_{int(time.time())}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存代码副本
        submission_dir = self.submissions_dir / problem_id
        submission_dir.mkdir(exist_ok=True)
        saved_code = submission_dir / f"{submission_id}.cpp"
        shutil.copy(code_file, saved_code)
        
        # 创建提交记录
        result_str = "AC" if passed == total else results[0].result.value if results else "UKE"
        submission = Submission(
            id=submission_id,
            timestamp=timestamp,
            code_file=str(saved_code),
            result=result_str,
            passed=passed,
            total=total,
            time_used=avg_time,
            notes=notes
        )
        
        problem.submissions.append(submission)
        
        # 更新状态
        if passed == total:
            problem.status = ProblemStatus.SOLVED
            # 保存为最终题解
            solution_file = self.solutions_dir / f"{problem_id}_solution.cpp"
            shutil.copy(code_file, solution_file)
            problem.solution_file = str(solution_file)
            print(f"\n[OK] Problem solved! Solution saved to: {solution_file}")
        else:
            if problem.status == ProblemStatus.UNSOLVED:
                problem.status = ProblemStatus.ATTEMPTED
        
        self.save_problem(problem)
        
        return results
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = {
            'total': len(self.problems),
            'by_year': {},
            'by_status': {
                ProblemStatus.UNSOLVED.value: 0,
                ProblemStatus.ATTEMPTED.value: 0,
                ProblemStatus.SOLVED.value: 0,
                ProblemStatus.REVIEWED.value: 0
            }
        }
        
        for prob in self.problems.values():
            # 按年份统计
            year = prob.year
            if year not in stats['by_year']:
                stats['by_year'][year] = {'total': 0, 'solved': 0}
            stats['by_year'][year]['total'] += 1
            if prob.status == ProblemStatus.SOLVED:
                stats['by_year'][year]['solved'] += 1
            
            # 按状态统计
            stats['by_status'][prob.status.value] += 1
        
        return stats
    
    def list_problems(self, year: int = None, status: ProblemStatus = None):
        """列出题目"""
        problems = self.problems.values()
        
        if year:
            problems = [p for p in problems if p.year == year]
        
        if status:
            problems = [p for p in problems if p.status == status]
        
        problems = sorted(problems, key=lambda p: (p.year, p.id))
        
        print(f"\n{'='*80}")
        print(f"{'Year':<6} {'ID':<12} {'Status':<10} {'Title':<40} {'Submissions':<12}")
        print(f"{'-'*80}")
        
        for p in problems:
            status_icon = "[V]" if p.status == ProblemStatus.SOLVED else "[ ]" if p.status == ProblemStatus.UNSOLVED else "[~]"
            print(f"{p.year:<6} {p.id:<12} {status_icon} {p.status.value:<8} {p.title:<40} {len(p.submissions):<12}")
        
        print(f"{'='*80}")
        print(f"Total: {len(problems)} problems\n")
    
    def show_problem_detail(self, problem_id: str):
        """显示题目详情"""
        if problem_id not in self.problems:
            print(f"Problem {problem_id} not found!")
            return
        
        p = self.problems[problem_id]
        
        print(f"\n{'='*60}")
        print(f"Problem: {p.id}")
        print(f"{'='*60}")
        print(f"Year: {p.year}")
        print(f"Title: {p.title}")
        print(f"Status: {p.status.value}")
        print(f"Tags: {', '.join(p.tags) if p.tags else 'None'}")
        print(f"\nDescription:")
        print(p.description if p.description else "No description")
        
        if p.notes:
            print(f"\nNotes:")
            print(p.notes)
        
        if p.solution_file:
            print(f"\nSolution: {p.solution_file}")
        
        if p.submissions:
            print(f"\nSubmission History ({len(p.submissions)} total):")
            print(f"{'-'*60}")
            for s in reversed(p.submissions[-10:]):  # 显示最近10次
                status = "[AC]" if s.passed == s.total else "[WA]"
                print(f"  {s.timestamp} | {status} {s.result} ({s.passed}/{s.total}) | {s.time_used:.1f}ms")
                if s.notes:
                    print(f"    Note: {s.notes}")
        
        print(f"{'='*60}\n")
    
    def add_notes(self, problem_id: str, notes: str):
        """添加学习笔记"""
        if problem_id not in self.problems:
            print(f"Problem {problem_id} not found!")
            return
        
        problem = self.problems[problem_id]
        problem.notes = notes
        self.save_problem(problem)
        print(f"[OK] Notes added to {problem_id}")
    
    def add_tags(self, problem_id: str, tags: List[str]):
        """添加标签"""
        if problem_id not in self.problems:
            print(f"Problem {problem_id} not found!")
            return
        
        problem = self.problems[problem_id]
        problem.tags = list(set(problem.tags + tags))
        self.save_problem(problem)
        print(f"[OK] Tags added: {', '.join(tags)}")
    
    def toggle_favorite(self, problem_id: str) -> bool:
        """切换题目收藏状态"""
        if problem_id not in self.problems:
            return False
        
        problem = self.problems[problem_id]
        problem.is_favorite = not problem.is_favorite
        self.save_problem(problem)
        return problem.is_favorite
    
    def update_annotation(self, problem_id: str, annotation: str):
        """更新题目批注"""
        if problem_id not in self.problems:
            return
        
        problem = self.problems[problem_id]
        problem.annotation = annotation
        self.save_problem(problem)
    
    def export_progress(self, filename: str = "progress_report.md"):
        """导出学习进度报告"""
        stats = self.get_statistics()
        
        with open(self.data_dir / filename, 'w', encoding='utf-8') as f:
            f.write("# 北航复试刷题进度报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 总体统计
            f.write("## 总体进度\n\n")
            total = stats['total']
            solved = stats['by_status'][ProblemStatus.SOLVED.value]
            f.write(f"- 总题数: {total}\n")
            f.write(f"- 已解决: {solved} ({solved/total*100:.1f}%)\n")
            f.write(f"- 尝试中: {stats['by_status'][ProblemStatus.ATTEMPTED.value]}\n")
            f.write(f"- 未开始: {stats['by_status'][ProblemStatus.UNSOLVED.value]}\n\n")
            
            # 按年份统计
            f.write("## 按年份统计\n\n")
            f.write("| 年份 | 总数 | 已解决 | 进度 |\n")
            f.write("|------|------|--------|------|\n")
            for year in sorted(stats['by_year'].keys(), reverse=True):
                y = stats['by_year'][year]
                pct = y['solved']/y['total']*100 if y['total'] > 0 else 0
                f.write(f"| {year} | {y['total']} | {y['solved']} | {pct:.1f}% |\n")
            
            f.write("\n## 已解决题目\n\n")
            solved_problems = [p for p in self.problems.values() if p.status == ProblemStatus.SOLVED]
            solved_problems.sort(key=lambda p: p.year, reverse=True)
            
            for p in solved_problems:
                f.write(f"### {p.id}: {p.title}\n")
                f.write(f"- 年份: {p.year}\n")
                f.write(f"- 标签: {', '.join(p.tags) if p.tags else 'None'}\n")
                if p.notes:
                    f.write(f"- 笔记: {p.notes}\n")
                if p.submissions:
                    last = p.submissions[-1]
                    f.write(f"- 最后提交: {last.timestamp} | {last.result}\n")
                f.write("\n")
        
        print(f"[OK] Progress report exported to: {self.data_dir / filename}")

# 命令行接口
def main():
    oj = BUAAOJ()
    
    if len(sys.argv) < 2:
        print("BUAA OJ System")
        print("="*60)
        print("Commands:")
        print("  create <year> <num> <title>     - Create new problem")
        print("  list [year] [status]            - List problems")
        print("  show <problem_id>               - Show problem details")
        print("  submit <problem_id> <code.cpp>  - Submit solution")
        print("  note <problem_id> <notes>       - Add notes")
        print("  tag <problem_id> <tag1,tag2>    - Add tags")
        print("  stats                           - Show statistics")
        print("  export                          - Export progress report")
        print("  test <problem_id> <code.cpp>    - Test without recording")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) >= 5:
        year = int(sys.argv[2])
        num = int(sys.argv[3])
        title = sys.argv[4]
        oj.create_problem(year, num, title)
    
    elif cmd == "list":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        status = ProblemStatus(sys.argv[3]) if len(sys.argv) > 3 else None
        oj.list_problems(year, status)
    
    elif cmd == "show" and len(sys.argv) >= 3:
        oj.show_problem_detail(sys.argv[2])
    
    elif cmd == "submit" and len(sys.argv) >= 4:
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        oj.submit(sys.argv[2], sys.argv[3], notes)
    
    elif cmd == "note" and len(sys.argv) >= 4:
        oj.add_notes(sys.argv[2], sys.argv[3])
    
    elif cmd == "tag" and len(sys.argv) >= 4:
        tags = sys.argv[3].split(",")
        oj.add_tags(sys.argv[2], tags)
    
    elif cmd == "stats":
        stats = oj.get_statistics()
        print(f"\nTotal Problems: {stats['total']}")
        print(f"Solved: {stats['by_status'][ProblemStatus.SOLVED.value]}")
        print(f"Attempted: {stats['by_status'][ProblemStatus.ATTEMPTED.value]}")
        print(f"Unsolved: {stats['by_status'][ProblemStatus.UNSOLVED.value]}")
    
    elif cmd == "export":
        oj.export_progress()
    
    elif cmd == "test" and len(sys.argv) >= 4:
        # 仅测试，不记录
        oj.oj.judge(sys.argv[2], sys.argv[3])
    
    else:
        print(f"Unknown command or invalid arguments: {cmd}")

if __name__ == "__main__":
    main()
