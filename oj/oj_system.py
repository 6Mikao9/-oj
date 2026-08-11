#!/usr/bin/env python3
"""
本地 OJ 系统 - 用于 C++ 代码评测
支持：题目管理、测试用例、自动判题
"""

import os
import sys
import json
import subprocess
import time
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class JudgeResult(Enum):
    AC = "Accepted"           # 通过
    WA = "Wrong Answer"       # 答案错误
    TLE = "Time Limit Exceeded"  # 超时
    MLE = "Memory Limit Exceeded"  # 内存超限
    RE = "Runtime Error"      # 运行时错误
    CE = "Compile Error"      # 编译错误
    OLE = "Output Limit Exceeded"  # 输出超限
    UKE = "Unknown Error"     # 未知错误

@dataclass
class TestCase:
    """测试用例"""
    input_data: str
    expected_output: str
    
@dataclass
class JudgeStatus:
    """评测结果"""
    result: JudgeResult
    time_used: float  # 毫秒
    memory_used: int  # KB
    message: str
    test_case_num: int = 0

class LocalOJ:
    """本地 OJ 系统"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = Path(base_dir)
        self.problems_dir = self.base_dir / "problems"
        self.submissions_dir = self.base_dir / "submissions"
        self.temp_dir = self.base_dir / "temp"
        
        # 创建必要的目录
        self.problems_dir.mkdir(exist_ok=True)
        self.submissions_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        # 默认限制
        self.time_limit = 1000  # 毫秒
        self.memory_limit = 64 * 1024  # 64MB
        
    def create_problem(self, problem_id: str, title: str = "", description: str = ""):
        """创建新题目"""
        problem_dir = self.problems_dir / problem_id
        problem_dir.mkdir(exist_ok=True)
        
        # 创建题目信息文件
        problem_info = {
            "id": problem_id,
            "title": title,
            "description": description,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "test_cases": []
        }
        
        info_file = problem_dir / "info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(problem_info, f, ensure_ascii=False, indent=2)
            
        # 创建测试用例目录
        (problem_dir / "testcases").mkdir(exist_ok=True)
        
        print(f"题目 {problem_id} 创建成功！")
        print(f"测试用例目录: {problem_dir / 'testcases'}")
        return problem_dir
    
    def add_test_case(self, problem_id: str, input_data: str, expected_output: str, case_id: int = None):
        """添加测试用例"""
        problem_dir = self.problems_dir / problem_id
        if not problem_dir.exists():
            print(f"题目 {problem_id} 不存在！")
            return False
            
        testcase_dir = problem_dir / "testcases"
        
        # 自动编号
        if case_id is None:
            existing = list(testcase_dir.glob("*.in"))
            case_id = len(existing) + 1
            
        # 保存测试用例
        with open(testcase_dir / f"{case_id}.in", 'w', encoding='utf-8') as f:
            f.write(input_data)
        with open(testcase_dir / f"{case_id}.out", 'w', encoding='utf-8') as f:
            f.write(expected_output)
            
        # 更新题目信息
        info_file = problem_dir / "info.json"
        with open(info_file, 'r', encoding='utf-8') as f:
            info = json.load(f)
        info["test_cases"].append(case_id)
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
            
        print(f"测试用例 {case_id} 添加成功！")
        return True
    
    def get_test_cases(self, problem_id: str) -> List[TestCase]:
        """获取题目的所有测试用例"""
        problem_dir = self.problems_dir / problem_id
        testcase_dir = problem_dir / "testcases"
        
        test_cases = []
        for in_file in sorted(testcase_dir.glob("*.in")):
            case_id = in_file.stem
            out_file = testcase_dir / f"{case_id}.out"
            
            with open(in_file, 'r', encoding='utf-8') as f:
                input_data = f.read()
            with open(out_file, 'r', encoding='utf-8') as f:
                expected_output = f.read()
                
            test_cases.append(TestCase(input_data, expected_output))
            
        return test_cases
    
    def compile_code(self, source_file: str, output_file: str) -> Tuple[bool, str]:
        """编译 C++ 代码"""
        # 使用 g++ 编译
        cmd = [
            "g++",
            "-std=c++17",
            "-O2",
            "-Wall",
            "-o", output_file,
            source_file
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=False,  # 使用二进制模式避免编码错误
                timeout=10
            )
            
            if result.returncode != 0:
                # 尝试解码stderr
                try:
                    stderr = result.stderr.decode('utf-8', errors='replace')
                except:
                    stderr = str(result.stderr)[:500]
                return False, stderr
            return True, "编译成功"
        except subprocess.TimeoutExpired:
            return False, "编译超时"
        except Exception as e:
            return False, str(e)
    
    def run_code(self, executable: str, input_data: str) -> Tuple[JudgeResult, str, float]:
        """运行代码并返回结果"""
        import os
        start_time = time.time()
        
        try:
            # 创建临时输入文件
            input_file = self.temp_dir / "temp_input.txt"
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(input_data)
            
            # Windows 下需要确保路径正确
            if os.name == 'nt':  # Windows
                # 使用绝对路径并确保可执行文件存在
                executable = os.path.abspath(executable)
                if not os.path.exists(executable):
                    return JudgeResult.RE, f"可执行文件不存在: {executable}", 0
            # 运行程序：使用 Popen 来更可靠地在超时后终止子进程
            # Windows: 使用 CREATE_NO_WINDOW 标志禁用错误报告对话框
            kwargs = {}
            if os.name == 'nt':
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            with open(input_file, 'r', encoding='utf-8') as f_in:
                proc = subprocess.Popen(
                [executable],
                stdin=f_in,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # 使用二进制模式，避免编码错误
                shell=False,
                **kwargs
            )

                try:
                    stdout, stderr = proc.communicate(timeout=self.time_limit / 1000)
                except subprocess.TimeoutExpired:
                    # 超时：尝试终止子进程并收集输出
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    stdout, stderr = proc.communicate()
                    # 检查是否有错误输出（可能是程序崩溃导致的超时）
                    if stderr:
                        # 尝试解码stderr
                        try:
                            error_stderr = stderr.decode('utf-8', errors='replace')
                        except:
                            error_stderr = str(stderr)[:500]
                        return JudgeResult.RE, f"程序异常退出（可能原因：崩溃/死循环）\n错误信息: {error_stderr[:500]}", self.time_limit
                    return JudgeResult.TLE, "运行超时（可能原因：死循环或输入处理错误）", self.time_limit

            time_used = (time.time() - start_time) * 1000  # 转换为毫秒

            if proc.returncode != 0:
                # 收集 stderr 和可能的错误信息
                try:
                    error_msg = stderr.decode('utf-8', errors='replace') if stderr else f"程序异常退出，返回码: {proc.returncode}"
                except:
                    error_msg = str(stderr)[:500] if stderr else f"程序异常退出，返回码: {proc.returncode}"
                return JudgeResult.RE, error_msg, time_used

            # 检查输出大小（防止输出过大）
            if len(stdout) > 10 * 1024 * 1024:  # 10MB
                return JudgeResult.OLE, "输出过大", time_used

            # 尝试解码stdout，处理编码问题
            try:
                # 优先尝试utf-8编码
                output = stdout.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # 尝试gbk编码（Windows默认）
                    output = stdout.decode('gbk')
                except:
                    # 其他编码尝试
                    output = stdout.decode('latin-1', errors='replace')

            return JudgeResult.AC, output, time_used
            
        except subprocess.TimeoutExpired:
            return JudgeResult.TLE, "运行超时", self.time_limit
        except PermissionError as e:
            return JudgeResult.RE, f"权限错误: {str(e)}\n请检查杀毒软件是否拦截", 0
        except Exception as e:
            return JudgeResult.RE, f"运行错误: {str(e)}", 0
    
    def compare_output(self, actual: str, expected: str) -> bool:
        """比较输出（忽略行尾空白和空行差异）"""
        actual_lines = actual.strip().split('\n')
        expected_lines = expected.strip().split('\n')
        
        if len(actual_lines) != len(expected_lines):
            return False
            
        for a, e in zip(actual_lines, expected_lines):
            if a.rstrip() != e.rstrip():
                return False
                
        return True
    
    def judge(self, problem_id: str, source_file: str) -> List[JudgeStatus]:
        """评测代码"""
        print(f"\n{'='*50}")
        print(f"开始评测题目: {problem_id}")
        print(f"源代码: {source_file}")
        print(f"{'='*50}\n")
        
        # 检查源文件
        if not os.path.exists(source_file):
            print(f"错误: 源文件不存在 {source_file}")
            return [JudgeStatus(JudgeResult.UKE, 0, 0, "源文件不存在", 0)]
        
        # 编译
        executable = str(self.temp_dir / "solution")
        if os.name == 'nt':  # Windows
            executable += ".exe"
            
        print("正在编译...")
        success, message = self.compile_code(source_file, executable)
        if not success:
            print(f"编译错误:\n{message}")
            return [JudgeStatus(JudgeResult.CE, 0, 0, message, 0)]
        print("编译成功！\n")
        
        # 获取测试用例
        test_cases = self.get_test_cases(problem_id)
        if not test_cases:
            print("警告: 没有找到测试用例")
            return [JudgeStatus(JudgeResult.UKE, 0, 0, "没有测试用例", 0)]
        
        print(f"找到 {len(test_cases)} 个测试用例\n")
        
        # 逐个测试
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"测试点 {i}/{len(test_cases)}: ", end="", flush=True)
            
            # 运行代码
            result, output, time_used = self.run_code(executable, test_case.input_data)
            
            if result == JudgeResult.AC:
                # 检查答案
                if self.compare_output(output, test_case.expected_output):
                    result = JudgeResult.AC
                    msg = "通过"
                else:
                    result = JudgeResult.WA
                    msg = "答案错误"
                    # 显示差异
                    print(f"\n  期望输出:\n{test_case.expected_output[:200]}")
                    print(f"  实际输出:\n{output[:200]}")
            else:
                msg = output
            
            status = JudgeStatus(result, time_used, 0, msg, i)
            results.append(status)
            
            print(f"{result.value} ({time_used:.1f}ms)")
            
            # 如果非 AC，可以选择停止
            if result != JudgeResult.AC:
                pass  # 继续测试其他点
        
        # 清理 - 添加延迟和重试机制
        if os.path.exists(executable):
            import time
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    # 等待进程完全退出
                    time.sleep(0.5)
                    os.remove(executable)
                    break  # 成功删除，跳出循环
                except PermissionError:
                    if attempt < max_retries - 1:
                        # 还有重试次数，继续等待
                        continue
                    else:
                        # 最后一次尝试失败，给出警告但不影响评测结果
                        print(f"提示: 可执行文件将在稍后自动清理: {executable}")
                except Exception as e:
                    print(f"提示: 清理临时文件时出错: {e}")
                    break
            
        # 输出总结
        print(f"\n{'='*50}")
        print("评测结果总结:")
        ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
        print(f"通过: {ac_count}/{len(results)}")
        for r in results:
            status = "✓" if r.result == JudgeResult.AC else "✗"
            print(f"  测试点 {r.test_case_num}: {status} {r.result.value}")
        print(f"{'='*50}\n")
        
        return results
    
    def list_problems(self):
        """列出所有题目"""
        print("\n题目列表:")
        for problem_dir in self.problems_dir.iterdir():
            if problem_dir.is_dir():
                info_file = problem_dir / "info.json"
                if info_file.exists():
                    with open(info_file, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                    print(f"  {info['id']}: {info.get('title', '无标题')}")
                    print(f"    测试用例数: {len(info.get('test_cases', []))}")


def main():
    """命令行接口"""
    oj = LocalOJ()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python oj_system.py create <problem_id> [title]  - 创建题目")
        print("  python oj_system.py add <problem_id> <input_file> <output_file>  - 添加测试用例")
        print("  python oj_system.py judge <problem_id> <source_file>  - 评测代码")
        print("  python oj_system.py list  - 列出所有题目")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("请提供题目 ID")
            return
        problem_id = sys.argv[2]
        title = sys.argv[3] if len(sys.argv) > 3 else ""
        oj.create_problem(problem_id, title)
        
    elif command == "add":
        if len(sys.argv) < 5:
            print("请提供题目 ID、输入文件和输出文件")
            return
        problem_id = sys.argv[2]
        input_file = sys.argv[3]
        output_file = sys.argv[4]
        
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = f.read()
        with open(output_file, 'r', encoding='utf-8') as f:
            output_data = f.read()
            
        oj.add_test_case(problem_id, input_data, output_data)
        
    elif command == "judge":
        if len(sys.argv) < 4:
            print("请提供题目 ID 和源代码文件")
            return
        problem_id = sys.argv[2]
        source_file = sys.argv[3]
        oj.judge(problem_id, source_file)
        
    elif command == "list":
        oj.list_problems()
        
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
