#!/usr/bin/env python3
"""
北航 OJ 图形界面 - 调试版本
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import traceback

# 错误日志
def log_error(msg):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{__import__('datetime').datetime.now()}] {msg}\n")

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from buaa_oj import BUAAOJ, ProblemStatus
    from oj_system import JudgeResult
except Exception as e:
    log_error(f"Import error: {traceback.format_exc()}")
    raise

class SimpleBUAAOJGUI:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("BUAA OJ - 复试刷题系统")
            self.root.geometry("1000x700")
            
            # 初始化 OJ
            log_error("Initializing BUAAOJ...")
            self.oj = BUAAOJ()
            log_error("BUAAOJ initialized successfully")
            
            # 当前选中的题目
            self.current_problem = None
            
            self.setup_ui()
            self.refresh_data()
        except Exception as e:
            log_error(f"Init error: {traceback.format_exc()}")
            raise
    
    def setup_ui(self):
        """设置界面"""
        try:
            # 主框架
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 左侧：题目列表
            left_frame = ttk.LabelFrame(main_frame, text="题目列表", padding=10)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
            left_frame.configure(width=350)
            
            # 筛选栏
            filter_frame = ttk.Frame(left_frame)
            filter_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(filter_frame, text="年份:").pack(side=tk.LEFT)
            self.year_var = tk.StringVar(value="全部")
            self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, width=8, state="readonly")
            self.year_combo.pack(side=tk.LEFT, padx=5)
            self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_problem_list())
            
            # 题目列表
            columns = ('year', 'id', 'title')
            self.problem_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=20)
            
            self.problem_tree.heading('year', text='年份')
            self.problem_tree.heading('id', text='题号')
            self.problem_tree.heading('title', text='标题')
            
            self.problem_tree.column('year', width=50)
            self.problem_tree.column('id', width=80)
            self.problem_tree.column('title', width=200)
            
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
            
            self.detail_title = ttk.Label(detail_frame, text="请选择题目", font=('Arial', 12, 'bold'))
            self.detail_title.pack(anchor=tk.W)
            
            self.detail_info = ttk.Label(detail_frame, text="")
            self.detail_info.pack(anchor=tk.W, pady=5)
            
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
            self.result_text = scrolledtext.ScrolledText(submit_frame, height=15, wrap=tk.WORD)
            self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # 底部按钮
            bottom_frame = ttk.Frame(right_frame)
            bottom_frame.pack(fill=tk.X, pady=10)
            
            ttk.Button(bottom_frame, text="新建题目", command=self.create_problem_dialog).pack(side=tk.LEFT, padx=5)
            ttk.Button(bottom_frame, text="刷新数据", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
            
            log_error("UI setup completed")
        except Exception as e:
            log_error(f"UI setup error: {traceback.format_exc()}")
            raise
    
    def refresh_data(self):
        """刷新数据"""
        try:
            # 更新年份筛选
            years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
            self.year_combo['values'] = ['全部'] + [str(y) for y in years]
            
            # 刷新题目列表
            self.refresh_problem_list()
            
            # 更新统计
            stats = self.oj.get_statistics()
            solved = stats['by_status'][ProblemStatus.SOLVED.value]
            total = stats['total']
            self.stats_label.config(text=f"进度: {solved}/{total}")
        except Exception as e:
            log_error(f"Refresh error: {traceback.format_exc()}")
    
    def refresh_problem_list(self):
        """刷新题目列表"""
        try:
            # 清空
            for item in self.problem_tree.get_children():
                self.problem_tree.delete(item)
            
            # 筛选
            year_filter = self.year_var.get()
            
            problems = list(self.oj.problems.values())
            
            if year_filter != "全部":
                problems = [p for p in problems if p.year == int(year_filter)]
            
            # 排序并插入
            problems.sort(key=lambda p: (p.year, p.id))
            
            for p in problems:
                self.problem_tree.insert('', tk.END, values=(p.year, p.id, p.title))
        except Exception as e:
            log_error(f"Refresh list error: {traceback.format_exc()}")
    
    def on_problem_select(self, event):
        """选择题目"""
        try:
            selection = self.problem_tree.selection()
            if not selection:
                return
            
            item = self.problem_tree.item(selection[0])
            problem_id = item['values'][1]
            
            self.current_problem = self.oj.problems.get(problem_id)
            if self.current_problem:
                self.show_problem_detail()
        except Exception as e:
            log_error(f"Select error: {traceback.format_exc()}")
    
    def show_problem_detail(self):
        """显示题目详情"""
        try:
            p = self.current_problem
            
            self.detail_title.config(text=f"{p.id}: {p.title}")
            self.detail_info.config(text=f"年份: {p.year} | 状态: {p.status.value} | 提交: {len(p.submissions)}次")
        except Exception as e:
            log_error(f"Show detail error: {traceback.format_exc()}")
    
    def select_code(self):
        """选择代码文件"""
        try:
            filename = filedialog.askopenfilename(
                title="选择 C++ 代码",
                filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
            )
            if filename:
                self.code_path.set(filename)
        except Exception as e:
            log_error(f"Select code error: {traceback.format_exc()}")
    
    def submit_code(self, record=True):
        """提交代码"""
        try:
            if not self.current_problem:
                messagebox.showwarning("警告", "请先选择题目")
                return
            
            code_file = self.code_path.get()
            if not code_file:
                messagebox.showwarning("警告", "请选择代码文件")
                return
            
            # 清空结果
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"正在评测 {self.current_problem.id}...\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.root.update()
            
            # 运行评测
            if record:
                results = self.oj.submit(self.current_problem.id, code_file)
            else:
                results = self.oj.oj.judge(self.current_problem.id, code_file)
            
            # 显示结果
            self.result_text.delete('1.0', tk.END)
            
            ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
            total = len(results)
            
            for r in results:
                status = "AC" if r.result == JudgeResult.AC else r.result.value
                self.result_text.insert(tk.END, f"测试点 {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n")
            
            self.result_text.insert(tk.END, f"\n{'='*50}\n")
            self.result_text.insert(tk.END, f"结果: {ac_count}/{total}\n")
            
            if ac_count == total:
                self.result_text.insert(tk.END, "全部通过！\n")
            
            # 刷新显示
            if record:
                self.refresh_data()
                self.show_problem_detail()
        except Exception as e:
            log_error(f"Submit error: {traceback.format_exc()}")
            self.result_text.insert(tk.END, f"\n错误: {str(e)}\n")
    
    def create_problem_dialog(self):
        """创建新题目对话框"""
        try:
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
        except Exception as e:
            log_error(f"Create dialog error: {traceback.format_exc()}")

def main():
    try:
        log_error("="*50)
        log_error("Starting BUAA OJ GUI...")
        root = tk.Tk()
        app = SimpleBUAAOJGUI(root)
        log_error("Entering main loop...")
        root.mainloop()
    except Exception as e:
        log_error(f"Main error: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()
