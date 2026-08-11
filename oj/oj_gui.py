#!/usr/bin/env python3
"""
本地 OJ 图形界面 - 简化操作
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
from pathlib import Path

# 添加 oj_system 到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oj_system import LocalOJ, JudgeResult

class OJGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("本地 OJ 系统")
        self.root.geometry("900x700")
        
        self.oj = LocalOJ()
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        # 标题
        title = tk.Label(self.root, text="本地 OJ 评测系统", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左侧：题目管理
        left_frame = ttk.LabelFrame(main_frame, text="题目管理", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 创建题目
        ttk.Label(left_frame, text="题目 ID:").pack(anchor=tk.W)
        self.problem_id = ttk.Entry(left_frame)
        self.problem_id.pack(fill=tk.X, pady=2)
        
        ttk.Label(left_frame, text="题目名称:").pack(anchor=tk.W)
        self.problem_title = ttk.Entry(left_frame)
        self.problem_title.pack(fill=tk.X, pady=2)
        
        ttk.Button(left_frame, text="创建题目", command=self.create_problem).pack(fill=tk.X, pady=5)
        
        # 测试用例
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(left_frame, text="添加测试用例", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        ttk.Label(left_frame, text="输入数据:").pack(anchor=tk.W)
        self.input_text = scrolledtext.ScrolledText(left_frame, height=8)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        ttk.Label(left_frame, text="期望输出:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(left_frame, height=8)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        ttk.Button(left_frame, text="添加测试用例", command=self.add_test_case).pack(fill=tk.X, pady=5)
        
        # 右侧：代码评测
        right_frame = ttk.LabelFrame(main_frame, text="代码评测", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 选择题目
        ttk.Label(right_frame, text="选择题目:").pack(anchor=tk.W)
        self.problem_var = tk.StringVar()
        self.problem_combo = ttk.Combobox(right_frame, textvariable=self.problem_var, state="readonly")
        self.problem_combo.pack(fill=tk.X, pady=2)
        self.refresh_problem_list()
        
        # 代码文件
        file_frame = ttk.Frame(right_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.code_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.code_path, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="选择代码", command=self.select_code).pack(side=tk.RIGHT, padx=5)
        
        # 评测按钮
        ttk.Button(right_frame, text="开始评测", command=self.judge).pack(fill=tk.X, pady=5)
        
        # 结果显示
        ttk.Label(right_frame, text="评测结果:").pack(anchor=tk.W, pady=(10,0))
        self.result_text = scrolledtext.ScrolledText(right_frame, height=20, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # 刷新按钮
        ttk.Button(right_frame, text="刷新题目列表", command=self.refresh_problem_list).pack(fill=tk.X, pady=5)
        
    def refresh_problem_list(self):
        """刷新题目列表"""
        problems = []
        for d in self.oj.problems_dir.iterdir():
            if d.is_dir():
                problems.append(d.name)
        self.problem_combo['values'] = problems
        if problems:
            self.problem_combo.current(0)
            
    def create_problem(self):
        """创建题目"""
        pid = self.problem_id.get().strip()
        title = self.problem_title.get().strip()
        
        if not pid:
            messagebox.showerror("错误", "请输入题目 ID")
            return
            
        self.oj.create_problem(pid, title)
        self.refresh_problem_list()
        messagebox.showinfo("成功", f"题目 {pid} 创建成功！")
        
    def add_test_case(self):
        """添加测试用例"""
        pid = self.problem_id.get().strip()
        if not pid:
            messagebox.showerror("错误", "请输入题目 ID")
            return
            
        input_data = self.input_text.get("1.0", tk.END).strip()
        output_data = self.output_text.get("1.0", tk.END).strip()
        
        if not input_data or not output_data:
            messagebox.showerror("错误", "请输入输入数据和期望输出")
            return
            
        self.oj.add_test_case(pid, input_data, output_data)
        messagebox.showinfo("成功", "测试用例添加成功！")
        
        # 清空输入
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        
    def select_code(self):
        """选择代码文件"""
        filename = filedialog.askopenfilename(
            title="选择 C++ 源代码",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
        )
        if filename:
            self.code_path.set(filename)
            
    def judge(self):
        """评测代码"""
        pid = self.problem_var.get()
        code_file = self.code_path.get()
        
        if not pid:
            messagebox.showerror("错误", "请选择题目")
            return
            
        if not code_file:
            messagebox.showerror("错误", "请选择代码文件")
            return
            
        # 清空结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"开始评测题目 {pid}...\n")
        self.result_text.insert(tk.END, f"代码文件: {code_file}\n")
        self.result_text.insert(tk.END, "="*50 + "\n\n")
        self.result_text.config(state=tk.DISABLED)
        self.root.update()
        
        # 运行评测
        results = self.oj.judge(pid, code_file)
        
        # 显示结果
        self.result_text.config(state=tk.NORMAL)
        
        ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
        total = len(results)
        
        self.result_text.insert(tk.END, f"\n{'='*50}\n")
        self.result_text.insert(tk.END, f"最终成绩: {ac_count}/{total}\n")
        
        for r in results:
            status = "✓ 通过" if r.result == JudgeResult.AC else f"✗ {r.result.value}"
            self.result_text.insert(tk.END, f"测试点 {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n")
            if r.result != JudgeResult.AC and r.message:
                self.result_text.insert(tk.END, f"  信息: {r.message[:200]}\n")
                
        self.result_text.config(state=tk.DISABLED)
        
        # 弹出提示
        if ac_count == total:
            messagebox.showinfo("恭喜", "全部通过！")
        else:
            messagebox.showwarning("结果", f"通过 {ac_count}/{total} 个测试点")

def main():
    root = tk.Tk()
    app = OJGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
