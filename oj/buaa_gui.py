#!/usr/bin/env python3
"""
北航 OJ 图形界面 - 现代化设计
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buaa_oj import BUAAOJ, ProblemStatus
from oj_system import JudgeResult

class ModernBUAAOJGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BUAA OJ - 复试刷题系统")
        self.root.geometry("1200x800")
        
        # 设置主题颜色
        self.colors = {
            'bg': '#f5f5f5',
            'primary': '#2196F3',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#f44336',
            'text': '#333333'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # 初始化 OJ
        self.oj = BUAAOJ()
        
        # 当前选中的题目
        self.current_problem = None
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """设置界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：题目列表
        left_frame = ttk.LabelFrame(main_frame, text="题目列表", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        left_frame.configure(width=400)
        
        # 筛选栏
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="年份:").pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value="全部")
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, width=10, state="readonly")
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_problem_list())
        
        ttk.Label(filter_frame, text="状态:").pack(side=tk.LEFT, padx=(10,0))
        self.status_var = tk.StringVar(value="全部")
        self.status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, 
                                         values=["全部", "未解决", "尝试中", "已解决"], 
                                         width=10, state="readonly")
        self.status_combo.pack(side=tk.LEFT, padx=5)
        self.status_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_problem_list())
        
        # 题目列表
        columns = ('year', 'id', 'status', 'title')
        self.problem_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=20)
        
        self.problem_tree.heading('year', text='年份')
        self.problem_tree.heading('id', text='题号')
        self.problem_tree.heading('status', text='状态')
        self.problem_tree.heading('title', text='标题')
        
        self.problem_tree.column('year', width=60)
        self.problem_tree.column('id', width=80)
        self.problem_tree.column('status', width=80)
        self.problem_tree.column('title', width=180)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.problem_tree.yview)
        self.problem_tree.configure(yscrollcommand=scrollbar.set)
        
        self.problem_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.problem_tree.bind("<<TreeviewSelect>>", self.on_problem_select)
        
        # 统计信息
        self.stats_label = ttk.Label(left_frame, text="统计: 0/0")
        self.stats_label.pack(pady=5)
        
        # 右侧：详情和操作
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 题目详情
        detail_frame = ttk.LabelFrame(right_frame, text="题目详情", padding=10)
        detail_frame.pack(fill=tk.X, pady=5)
        
        self.detail_title = ttk.Label(detail_frame, text="请选择题目", font=('Arial', 14, 'bold'))
        self.detail_title.pack(anchor=tk.W)
        
        self.detail_info = ttk.Label(detail_frame, text="")
        self.detail_info.pack(anchor=tk.W, pady=5)
        
        self.detail_desc = scrolledtext.ScrolledText(detail_frame, height=6, wrap=tk.WORD)
        self.detail_desc.pack(fill=tk.X, pady=5)
        
        # 笔记区域
        notes_frame = ttk.LabelFrame(right_frame, text="学习笔记", padding=10)
        notes_frame.pack(fill=tk.X, pady=5)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=4, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        
        ttk.Button(notes_frame, text="保存笔记", command=self.save_notes).pack(anchor=tk.E, pady=5)
        
        # 提交区域
        submit_frame = ttk.LabelFrame(right_frame, text="代码提交", padding=10)
        submit_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 代码选择
        code_frame = ttk.Frame(submit_frame)
        code_frame.pack(fill=tk.X, pady=5)
        
        self.code_path = tk.StringVar()
        ttk.Entry(code_frame, textvariable=self.code_path, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(code_frame, text="选择代码", command=self.select_code).pack(side=tk.RIGHT, padx=5)
        
        # 提交按钮
        btn_frame = ttk.Frame(submit_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="测试运行", command=lambda: self.submit_code(record=False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="正式提交", command=lambda: self.submit_code(record=True)).pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        self.result_text = scrolledtext.ScrolledText(submit_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 提交历史
        history_frame = ttk.LabelFrame(right_frame, text="提交历史", padding=10)
        history_frame.pack(fill=tk.X, pady=5)
        
        self.history_list = tk.Listbox(history_frame, height=5)
        self.history_list.pack(fill=tk.X)
        
        # 底部按钮
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(bottom_frame, text="新建题目", command=self.create_problem_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="刷新数据", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="导出报告", command=self.export_report).pack(side=tk.LEFT, padx=5)
    
    def refresh_data(self):
        """刷新数据"""
        # 更新年份筛选
        years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
        self.year_combo['values'] = ['全部'] + [str(y) for y in years]
        
        # 刷新题目列表
        self.refresh_problem_list()
        
        # 更新统计
        stats = self.oj.get_statistics()
        solved = stats['by_status'][ProblemStatus.SOLVED.value]
        total = stats['total']
        self.stats_label.config(text=f"进度: {solved}/{total} ({solved/total*100:.1f}%)")
    
    def refresh_problem_list(self):
        """刷新题目列表"""
        # 清空
        for item in self.problem_tree.get_children():
            self.problem_tree.delete(item)
        
        # 筛选
        year_filter = self.year_var.get()
        status_filter = self.status_var.get()
        
        problems = list(self.oj.problems.values())
        
        if year_filter != "全部":
            problems = [p for p in problems if p.year == int(year_filter)]
        
        if status_filter != "全部":
            status_map = {"未解决": ProblemStatus.UNSOLVED, 
                         "尝试中": ProblemStatus.ATTEMPTED,
                         "已解决": ProblemStatus.SOLVED}
            problems = [p for p in problems if p.status == status_map.get(status_filter)]
        
        # 排序并插入
        problems.sort(key=lambda p: (p.year, p.id))
        
        for p in problems:
            status_icon = "✓" if p.status == ProblemStatus.SOLVED else "○" if p.status == ProblemStatus.UNSOLVED else "△"
            self.problem_tree.insert('', tk.END, values=(p.year, p.id, status_icon, p.title))
    
    def on_problem_select(self, event):
        """选择题目"""
        selection = self.problem_tree.selection()
        if not selection:
            return
        
        item = self.problem_tree.item(selection[0])
        problem_id = item['values'][1]
        
        self.current_problem = self.oj.problems.get(problem_id)
        if self.current_problem:
            self.show_problem_detail()
    
    def show_problem_detail(self):
        """显示题目详情"""
        p = self.current_problem
        
        self.detail_title.config(text=f"{p.id}: {p.title}")
        self.detail_info.config(text=f"年份: {p.year} | 状态: {p.status.value} | 提交次数: {len(p.submissions)}")
        
        self.detail_desc.delete('1.0', tk.END)
        self.detail_desc.insert(tk.END, p.description if p.description else "暂无描述")
        
        self.notes_text.delete('1.0', tk.END)
        self.notes_text.insert(tk.END, p.notes)
        
        # 刷新历史
        self.history_list.delete(0, tk.END)
        for s in reversed(p.submissions[-10:]):
            status = "✓" if s.passed == s.total else "✗"
            self.history_list.insert(tk.END, f"{s.timestamp} {status} {s.result} ({s.passed}/{s.total})")
    
    def save_notes(self):
        """保存笔记"""
        if not self.current_problem:
            messagebox.showwarning("警告", "请先选择题目")
            return
        
        notes = self.notes_text.get('1.0', tk.END).strip()
        self.oj.add_notes(self.current_problem.id, notes)
        messagebox.showinfo("成功", "笔记已保存")
    
    def select_code(self):
        """选择代码文件"""
        filename = filedialog.askopenfilename(
            title="选择 C++ 代码",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
        )
        if filename:
            self.code_path.set(filename)
    
    def submit_code(self, record=True):
        """提交代码"""
        if not self.current_problem:
            messagebox.showwarning("警告", "请先选择题目")
            return
        
        code_file = self.code_path.get()
        if not code_file:
            messagebox.showwarning("警告", "请选择代码文件")
            return
        
        # 清空结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"正在评测 {self.current_problem.id}...\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.config(state=tk.DISABLED)
        self.root.update()
        
        # 运行评测
        if record:
            results = self.oj.submit(self.current_problem.id, code_file)
        else:
            results = self.oj.oj.judge(self.current_problem.id, code_file)
        
        # 显示结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
        total = len(results)
        
        for r in results:
            status = "✓ 通过" if r.result == JudgeResult.AC else f"✗ {r.result.value}"
            self.result_text.insert(tk.END, f"测试点 {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n")
        
        self.result_text.insert(tk.END, f"\n{'='*50}\n")
        self.result_text.insert(tk.END, f"结果: {ac_count}/{total}\n")
        
        if ac_count == total:
            self.result_text.insert(tk.END, "恭喜！全部通过！\n")
        
        self.result_text.config(state=tk.DISABLED)
        
        # 刷新显示
        if record:
            self.refresh_data()
            self.show_problem_detail()
    
    def create_problem_dialog(self):
        """创建新题目对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建题目")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="年份:").pack(pady=5)
        year_entry = ttk.Entry(dialog)
        year_entry.pack()
        year_entry.insert(0, "2025")
        
        ttk.Label(dialog, text="题号:").pack(pady=5)
        num_entry = ttk.Entry(dialog)
        num_entry.pack()
        num_entry.insert(0, "1")
        
        ttk.Label(dialog, text="标题:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.pack()
        
        def do_create():
            try:
                year = int(year_entry.get())
                num = int(num_entry.get())
                title = title_entry.get()
                if title:
                    self.oj.create_problem(year, num, title)
                    self.refresh_data()
                    dialog.destroy()
                    messagebox.showinfo("成功", "题目创建成功！")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        ttk.Button(dialog, text="创建", command=do_create).pack(pady=20)
    
    def export_report(self):
        """导出报告"""
        self.oj.export_progress()
        messagebox.showinfo("成功", "报告已导出到 data/progress_report.md")

def main():
    root = tk.Tk()
    app = ModernBUAAOJGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
