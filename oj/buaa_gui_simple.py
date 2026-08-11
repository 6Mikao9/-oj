#!/usr/bin/env python3
"""
北航 OJ 图形界面 - 简化稳定版
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from buaa_oj import BUAAOJ, ProblemStatus
    from oj_system import JudgeResult
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保 oj_system.py 和 buaa_oj.py 在同一目录")
    input("按回车键退出...")
    sys.exit(1)

class BUAAOJGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BUAA OJ - 北航复试刷题系统")
        self.root.geometry("900x600")
        
        # 初始化 OJ
        print("正在初始化系统...")
        self.oj = BUAAOJ()
        print("系统初始化完成")
        
        self.current_problem = None
        
        self.setup_ui()
        self.refresh_data()
        
    def setup_ui(self):
        """设置界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：题目列表
        left_frame = ttk.LabelFrame(main_frame, text="题目列表")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        left_frame.configure(width=400)
        
        # 筛选
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="年份:").pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value="全部")
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, 
                                       width=10, state="readonly")
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())
        
        # 题目列表
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('year', 'id', 'status', 'title')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        self.tree.heading('year', text='年份')
        self.tree.heading('id', text='题号')
        self.tree.heading('status', text='状态')
        self.tree.heading('title', text='标题')
        
        self.tree.column('year', width=50)
        self.tree.column('id', width=80)
        self.tree.column('status', width=60)
        self.tree.column('title', width=180)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # 统计
        self.stats_label = ttk.Label(left_frame, text="进度: 0/0")
        self.stats_label.pack(pady=5)
        
        # 右侧：操作区
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 题目信息
        info_frame = ttk.LabelFrame(right_frame, text="题目信息")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="请选择题目", font=('Arial', 12))
        self.info_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 代码提交
        submit_frame = ttk.LabelFrame(right_frame, text="代码提交")
        submit_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 代码路径
        path_frame = ttk.Frame(submit_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.code_path = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.code_path, state="readonly").pack(
            side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="浏览...", command=self.browse_code).pack(
            side=tk.RIGHT, padx=5)
        
        # 按钮
        btn_frame = ttk.Frame(submit_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="测试运行", 
                  command=lambda: self.judge(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="正式提交", 
                  command=lambda: self.judge(True)).pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        self.result_text = scrolledtext.ScrolledText(submit_frame, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 底部按钮
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(bottom_frame, text="新建题目", 
                  command=self.create_problem).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="刷新", 
                  command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        
    def refresh_data(self):
        """刷新数据"""
        # 更新年份列表
        years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
        self.year_combo['values'] = ['全部'] + [str(y) for y in years]
        
        self.refresh_list()
        
        # 更新统计
        stats = self.oj.get_statistics()
        solved = stats['by_status'].get('已解决', 0)
        total = stats['total']
        self.stats_label.config(text=f"进度: {solved}/{total}")
        
    def refresh_list(self):
        """刷新题目列表"""
        # 清空
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取题目
        year_filter = self.year_var.get()
        problems = list(self.oj.problems.values())
        
        if year_filter != "全部":
            problems = [p for p in problems if p.year == int(year_filter)]
        
        problems.sort(key=lambda p: (p.year, p.id))
        
        # 插入
        for p in problems:
            status = "✓" if p.status == ProblemStatus.SOLVED else "○"
            self.tree.insert('', tk.END, values=(p.year, p.id, status, p.title))
            
    def on_select(self, event):
        """选择题目"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        problem_id = item['values'][1]
        
        self.current_problem = self.oj.problems.get(problem_id)
        if self.current_problem:
            p = self.current_problem
            self.info_label.config(
                text=f"{p.id}: {p.title}\n状态: {p.status.value} | 提交: {len(p.submissions)}次")
            
    def browse_code(self):
        """浏览代码文件"""
        filename = filedialog.askopenfilename(
            title="选择 C++ 代码",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
        )
        if filename:
            self.code_path.set(filename)
            
    def judge(self, record=True):
        """评测代码"""
        if not self.current_problem:
            messagebox.showwarning("提示", "请先选择题目")
            return
            
        code_file = self.code_path.get()
        if not code_file:
            messagebox.showwarning("提示", "请选择代码文件")
            return
            
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"评测 {self.current_problem.id}...\n")
        self.result_text.insert(tk.END, "="*40 + "\n")
        self.root.update()
        
        try:
            if record:
                results = self.oj.submit(self.current_problem.id, code_file)
            else:
                results = self.oj.oj.judge(self.current_problem.id, code_file)
                
            self.result_text.delete('1.0', tk.END)
            
            ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
            total = len(results)
            
            for r in results:
                status = "通过" if r.result == JudgeResult.AC else r.result.value
                self.result_text.insert(tk.END, 
                    f"测试点 {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n")
            
            self.result_text.insert(tk.END, f"\n{'='*40}\n")
            self.result_text.insert(tk.END, f"结果: {ac_count}/{total}\n")
            
            if ac_count == total:
                self.result_text.insert(tk.END, "恭喜！全部通过！\n")
                
            if record:
                self.refresh_data()
                
        except Exception as e:
            self.result_text.insert(tk.END, f"\n错误: {str(e)}\n")
            
    def create_problem(self):
        """创建题目"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建题目")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="年份:").pack(pady=5)
        year_entry = ttk.Entry(dialog)
        year_entry.pack()
        year_entry.insert(0, "2025")
        
        ttk.Label(dialog, text="题号:").pack(pady=5)
        num_entry = ttk.Entry(dialog)
        num_entry.pack()
        num_entry.insert(0, "1")
        
        ttk.Label(dialog, text="标题:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=30)
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
        
        ttk.Button(dialog, text="创建", command=do_create).pack(pady=10)

def main():
    root = tk.Tk()
    app = BUAAOJGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
