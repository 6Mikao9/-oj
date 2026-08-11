#!/usr/bin/env python3
"""
北航 OJ 图形界面 V2 - 优化版
- 更大窗口
- 可折叠代码提交区
- 更大的题目描述区域
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from buaa_oj import BUAAOJ, ProblemStatus
    from oj_system import JudgeResult
except ImportError as e:
    print(f"Import error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

class BUAAOJV2:
    def __init__(self, root):
        self.root = root
        self.root.title("BUAA OJ - Beihang University ACM Practice System")
        self.root.geometry("1600x1000")
        
        # 初始化 OJ
        self.oj = BUAAOJ()
        self.current_problem = None
        self.code_visible = False
        
        self.create_ui()
        self.load_problems()
        
    def create_ui(self):
        """创建用户界面"""
        # 顶部标题栏
        header = tk.Frame(self.root, bg='#003366', height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="BUAA OJ - Beihang University ACM Practice System", 
                              font=('Microsoft YaHei', 16, 'bold'), 
                              bg='#003366', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 主内容区
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：题目列表 (固定宽度)
        left_frame = tk.Frame(main_container, width=350)
        main_container.add(left_frame, minsize=300)
        
        # 筛选区
        filter_frame = tk.LabelFrame(left_frame, text="Filter", font=('Microsoft YaHei', 10, 'bold'))
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Year:", font=('Microsoft YaHei', 10)).pack(side=tk.LEFT, padx=5)
        self.year_var = tk.StringVar(value="All")
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, 
                                       width=12, state="readonly")
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.on_year_change)
        
        # 题目列表
        list_label = tk.Label(left_frame, text="Problem List", font=('Microsoft YaHei', 11, 'bold'))
        list_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 使用 Canvas + Frame 实现可滚动列表
        list_container = tk.Frame(left_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(list_container, width=320)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=320)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 统计信息
        self.stats_label = tk.Label(left_frame, text="Progress: 0/0", 
                                   font=('Microsoft YaHei', 10), fg='#003366')
        self.stats_label.pack(pady=5)
        
        # 底部按钮
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="+ New Problem", font=('Microsoft YaHei', 9),
                 command=self.create_problem).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Refresh", font=('Microsoft YaHei', 9),
                 command=self.load_problems).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Export", font=('Microsoft YaHei', 9),
                 command=self.export_report).pack(side=tk.LEFT, padx=2)
        
        # 右侧：题目详情 (可调整大小)
        right_frame = tk.Frame(main_container)
        main_container.add(right_frame, minsize=800)
        
        # 题目信息区 (更大的描述区域)
        info_frame = tk.LabelFrame(right_frame, text="Problem Description", 
                                   font=('Microsoft YaHei', 11, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.problem_title = tk.Label(info_frame, text="Please select a problem", 
                                     font=('Microsoft YaHei', 14, 'bold'), fg='#003366')
        self.problem_title.pack(anchor=tk.W, padx=10, pady=5)
        
        self.problem_info = tk.Label(info_frame, text="", 
                                    font=('Microsoft YaHei', 10), fg='#666666')
        self.problem_info.pack(anchor=tk.W, padx=10)
        
        # 大的题目描述区域
        self.problem_desc = scrolledtext.ScrolledText(info_frame, height=25, 
                                                      font=('Microsoft YaHei', 11),
                                                      wrap=tk.WORD)
        self.problem_desc.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.problem_desc.insert(tk.END, "Select a problem from the left to start practicing...")
        self.problem_desc.config(state=tk.DISABLED)
        
        # 展开/折叠按钮
        self.toggle_btn = tk.Button(right_frame, text="▼ Show Submit Code", 
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg='#003366', fg='white',
                                   command=self.toggle_code_panel)
        self.toggle_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # 代码提交区 (默认折叠)
        self.submit_frame = tk.LabelFrame(right_frame, text="Submit Code", 
                                         font=('Microsoft YaHei', 11, 'bold'))
        # 不 pack，等点击按钮再显示
        
        # 代码输入框
        code_label = tk.Label(self.submit_frame, text="Paste your C++ code here:", 
                             font=('Microsoft YaHei', 10))
        code_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.code_text = scrolledtext.ScrolledText(self.submit_frame, height=15, 
                                                   font=('Consolas', 11),
                                                   wrap=tk.NONE)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 按钮区
        btn_frame2 = tk.Frame(self.submit_frame)
        btn_frame2.pack(fill=tk.X, padx=10, pady=10)
        
        self.test_btn = tk.Button(btn_frame2, text="Test Run", 
                                 font=('Microsoft YaHei', 11),
                                 bg='#FF9800', fg='white',
                                 width=12, command=lambda: self.submit_code(test_only=True))
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.submit_btn = tk.Button(btn_frame2, text="Submit", 
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg='#003366', fg='white',
                                   width=12, command=lambda: self.submit_code(test_only=False))
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame2, text="Clear", font=('Microsoft YaHei', 10),
                 width=10, command=self.clear_code).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame2, text="Load from File", font=('Microsoft YaHei', 10),
                 width=12, command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区
        result_frame = tk.LabelFrame(right_frame, text="Judge Result", 
                                    font=('Microsoft YaHei', 11, 'bold'))
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, 
                                                     font=('Consolas', 10),
                                                     wrap=tk.WORD)
        self.result_text.pack(fill=tk.X, padx=10, pady=5)
        self.result_text.insert(tk.END, "Waiting for submission...")
        self.result_text.config(state=tk.DISABLED)
        
    def toggle_code_panel(self):
        """切换代码提交区的显示/隐藏"""
        if self.code_visible:
            self.submit_frame.pack_forget()
            self.toggle_btn.config(text="▼ Show Submit Code")
            self.code_visible = False
        else:
            self.submit_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.toggle_btn.config(text="▲ Hide Submit Code")
            self.code_visible = True
            
    def load_problems(self):
        """加载题目列表"""
        # 清空现有列表
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 获取年份列表
        years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
        self.year_combo['values'] = ['All'] + [str(y) for y in years]
        
        # 筛选题目
        year_filter = self.year_var.get()
        problems = list(self.oj.problems.values())
        
        if year_filter != "All":
            problems = [p for p in problems if p.year == int(year_filter)]
        
        problems.sort(key=lambda p: (p.year, p.id))
        
        # 创建题目按钮
        for i, p in enumerate(problems):
            # 状态颜色
            if p.status == ProblemStatus.SOLVED:
                status_color = '#00AA00'
                status_text = '✓'
            elif p.status == ProblemStatus.ATTEMPTED:
                status_color = '#FF9800'
                status_text = '△'
            else:
                status_color = '#999999'
                status_text = '○'
            
            # 题目按钮
            btn_frame = tk.Frame(self.scrollable_frame, bg='white', bd=1, relief=tk.SOLID)
            btn_frame.pack(fill=tk.X, padx=2, pady=2)
            btn_frame.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
            
            # 状态标记
            status_label = tk.Label(btn_frame, text=status_text, 
                                   font=('Microsoft YaHei', 12, 'bold'),
                                   fg=status_color, bg='white', width=2)
            status_label.pack(side=tk.LEFT, padx=5)
            status_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
            
            # 题号和标题
            text = f"{p.id}: {p.title[:25]}..." if len(p.title) > 25 else f"{p.id}: {p.title}"
            title_label = tk.Label(btn_frame, text=text, 
                                  font=('Microsoft YaHei', 10),
                                  bg='white', anchor=tk.W)
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            title_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
            
            # 提交次数
            if p.submissions:
                count_label = tk.Label(btn_frame, text=f"{len(p.submissions)}", 
                                      font=('Microsoft YaHei', 9),
                                      fg='#666666', bg='white')
                count_label.pack(side=tk.RIGHT, padx=5)
                count_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
        
        # 更新统计
        stats = self.oj.get_statistics()
        solved = stats['by_status'].get('已解决', 0)
        total = stats['total']
        pct = solved*100//total if total > 0 else 0
        self.stats_label.config(text=f"Progress: {solved}/{total} ({pct}%)")
        
    def on_year_change(self, event=None):
        """年份筛选变化"""
        self.load_problems()
        
    def select_problem(self, problem):
        """选择题目"""
        self.current_problem = problem
        
        # 更新标题
        self.problem_title.config(text=f"{problem.id}: {problem.title}")
        
        # 更新信息
        info_text = f"Year: {problem.year} | Status: {problem.status.value}"
        if problem.submissions:
            last = problem.submissions[-1]
            info_text += f" | Last: {last.result} ({last.passed}/{last.total})"
        self.problem_info.config(text=info_text)
        
        # 更新描述
        self.problem_desc.config(state=tk.NORMAL)
        self.problem_desc.delete('1.0', tk.END)
        if problem.description:
            self.problem_desc.insert(tk.END, problem.description)
        else:
            self.problem_desc.insert(tk.END, f"Problem: {problem.title}\n\n")
            self.problem_desc.insert(tk.END, "No detailed description available.\n\n")
            self.problem_desc.insert(tk.END, "Tip: Send me the problem image and I can add full details!")
        self.problem_desc.config(state=tk.DISABLED)
        
        # 清空结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Selected: {problem.id}\nClick 'Show Submit Code' to submit your solution.")
        self.result_text.config(state=tk.DISABLED)
        
    def submit_code(self, test_only=False):
        """提交代码"""
        if not self.current_problem:
            messagebox.showwarning("Warning", "Please select a problem first")
            return
        
        # 获取代码
        code = self.code_text.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Please enter your code")
            return
        
        # 保存代码到临时文件
        temp_file = self.oj.temp_dir / f"submit_{self.current_problem.id}.cpp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 显示评测中
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Judging {self.current_problem.id}...\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # 运行评测
            if test_only:
                results = self.oj.oj.judge(self.current_problem.id, str(temp_file))
            else:
                results = self.oj.submit(self.current_problem.id, str(temp_file))
            
            # 显示结果
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            
            ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
            total = len(results)
            
            for r in results:
                if r.result == JudgeResult.AC:
                    status = "✓ Accepted"
                elif r.result == JudgeResult.WA:
                    status = "✗ Wrong Answer"
                elif r.result == JudgeResult.TLE:
                    status = "⏱ Time Limit"
                elif r.result == JudgeResult.RE:
                    status = "⚠ Runtime Error"
                else:
                    status = f"✗ {r.result.value}"
                
                self.result_text.insert(tk.END, f"Test {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n")
            
            self.result_text.insert(tk.END, f"\n{'='*50}\n")
            
            if ac_count == total:
                self.result_text.insert(tk.END, f"\n✓ All Passed! ({ac_count}/{total})\n")
                if not test_only:
                    self.result_text.insert(tk.END, "Problem marked as SOLVED!\n")
            else:
                self.result_text.insert(tk.END, f"\n✗ Failed ({ac_count}/{total})\n")
            
            self.result_text.config(state=tk.DISABLED)
            
            # 刷新列表
            if not test_only:
                self.load_problems()
                
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"\nError: {str(e)}\n")
            self.result_text.config(state=tk.DISABLED)
        finally:
            # 清理临时文件
            if temp_file.exists():
                temp_file.unlink()
                
    def clear_code(self):
        """清空代码"""
        if messagebox.askyesno("Confirm", "Clear all code?"):
            self.code_text.delete('1.0', tk.END)
            
    def load_from_file(self):
        """从文件加载代码"""
        filename = filedialog.askopenfilename(
            title="Select C++ Code File",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_text.delete('1.0', tk.END)
                self.code_text.insert(tk.END, code)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot read file: {e}")
                
    def create_problem(self):
        """创建新题目"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Problem")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        
        tk.Label(dialog, text="Year:", font=('Microsoft YaHei', 11)).pack(pady=5)
        year_entry = tk.Entry(dialog, font=('Microsoft YaHei', 11), width=20)
        year_entry.pack()
        year_entry.insert(0, "2025")
        
        tk.Label(dialog, text="Number:", font=('Microsoft YaHei', 11)).pack(pady=5)
        num_entry = tk.Entry(dialog, font=('Microsoft YaHei', 11), width=20)
        num_entry.pack()
        num_entry.insert(0, "1")
        
        tk.Label(dialog, text="Title:", font=('Microsoft YaHei', 11)).pack(pady=5)
        title_entry = tk.Entry(dialog, font=('Microsoft YaHei', 11), width=30)
        title_entry.pack()
        
        def do_create():
            try:
                year = int(year_entry.get())
                num = int(num_entry.get())
                title = title_entry.get().strip()
                if title:
                    self.oj.create_problem(year, num, title)
                    self.load_problems()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Problem created!")
                else:
                    messagebox.showwarning("Warning", "Please enter title")
            except ValueError:
                messagebox.showerror("Error", "Year and number must be integers")
        
        tk.Button(dialog, text="Create", font=('Microsoft YaHei', 11),
                 bg='#003366', fg='white', width=10,
                 command=do_create).pack(pady=15)
        
    def export_report(self):
        """导出进度报告"""
        try:
            self.oj.export_progress()
            messagebox.showinfo("Success", "Report exported to data/progress_report.md")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

def main():
    root = tk.Tk()
    app = BUAAOJV2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
