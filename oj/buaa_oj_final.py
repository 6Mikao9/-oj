#!/usr/bin/env python3
"""
北航 OJ 图形界面 - 仿官方界面最终版
支持：点击选择题目、代码粘贴提交
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
    print(f"导入错误: {e}")
    input("按回车键退出...")
    sys.exit(1)

class BUAAOJApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BUAA OJ - 北航复试刷题系统")
        self.root.geometry("1400x900")
        
        # 配置样式
        self.setup_style()
        
        # 初始化 OJ
        self.oj = BUAAOJ()
        self.current_problem = None
        
        # 创建界面
        self.create_ui()
        
        # 加载数据
        self.load_problems()
        
    def setup_style(self):
        """设置样式"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#003366')
        style.configure('Subtitle.TLabel', font=('微软雅黑', 12), foreground='#0066CC')
        style.configure('Problem.TLabel', font=('微软雅黑', 11))
        style.configure('Info.TLabel', font=('微软雅黑', 10), foreground='#666666')
        style.configure('AC.TLabel', font=('微软雅黑', 10), foreground='#00AA00')
        style.configure('WA.TLabel', font=('微软雅黑', 10), foreground='#AA0000')
        
        # 按钮样式
        style.configure('Submit.TButton', font=('微软雅黑', 11, 'bold'))
        style.configure('Test.TButton', font=('微软雅黑', 10))
        
    def create_ui(self):
        """创建用户界面"""
        # 顶部标题栏
        header = tk.Frame(self.root, bg='#003366', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="BUAA OJ - 北航研究生复试刷题系统", 
                              font=('微软雅黑', 18, 'bold'), 
                              bg='#003366', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 主内容区
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：题目列表
        left_panel = tk.LabelFrame(main_container, text="题目列表", 
                                   font=('微软雅黑', 11, 'bold'))
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        left_panel.configure(width=350)
        
        # 筛选区
        filter_frame = tk.Frame(left_panel)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(filter_frame, text="年份:", font=('微软雅黑', 10)).pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value="全部")
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, 
                                       width=12, state="readonly", font=('微软雅黑', 10))
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.on_year_change)
        
        # 题目列表（使用 Listbox 替代 Treeview，更容易点击）
        list_frame = tk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 使用 Canvas + Frame 实现可滚动列表
        self.canvas = tk.Canvas(list_frame, width=300)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=300)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 统计信息
        self.stats_label = tk.Label(left_panel, text="进度: 0/0", 
                                   font=('微软雅黑', 10), fg='#003366')
        self.stats_label.pack(pady=5)
        
        # 右侧：题目详情和提交
        right_panel = tk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 题目信息区
        self.problem_frame = tk.LabelFrame(right_panel, text="题目详情", 
                                          font=('微软雅黑', 11, 'bold'))
        self.problem_frame.pack(fill=tk.X, pady=5)
        
        self.problem_title = tk.Label(self.problem_frame, text="请选择题目", 
                                     font=('微软雅黑', 14, 'bold'), fg='#003366')
        self.problem_title.pack(anchor=tk.W, padx=10, pady=5)
        
        self.problem_info = tk.Label(self.problem_frame, text="", 
                                    font=('微软雅黑', 10), fg='#666666')
        self.problem_info.pack(anchor=tk.W, padx=10)
        
        self.problem_desc = scrolledtext.ScrolledText(self.problem_frame, height=8, 
                                                      font=('微软雅黑', 10),
                                                      wrap=tk.WORD)
        self.problem_desc.pack(fill=tk.X, padx=10, pady=5)
        self.problem_desc.insert(tk.END, "请从左侧选择一道题目开始练习...")
        self.problem_desc.config(state=tk.DISABLED)
        
        # 代码提交区
        submit_frame = tk.LabelFrame(right_panel, text="提交代码", 
                                    font=('微软雅黑', 11, 'bold'))
        submit_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 代码输入框
        code_label = tk.Label(submit_frame, text="请在此粘贴您的 C++ 代码:", 
                             font=('微软雅黑', 10))
        code_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.code_text = scrolledtext.ScrolledText(submit_frame, height=15, 
                                                   font=('Consolas', 11),
                                                   wrap=tk.NONE)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 按钮区
        btn_frame = tk.Frame(submit_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.test_btn = tk.Button(btn_frame, text="测试运行", 
                                 font=('微软雅黑', 11),
                                 bg='#FF9800', fg='white',
                                 width=12, height=1,
                                 command=lambda: self.submit_code(test_only=True))
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.submit_btn = tk.Button(btn_frame, text="确认提交", 
                                   font=('微软雅黑', 11, 'bold'),
                                   bg='#003366', fg='white',
                                   width=12, height=1,
                                   command=lambda: self.submit_code(test_only=False))
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="清空代码", 
                 font=('微软雅黑', 10),
                 width=10,
                 command=self.clear_code).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="从文件加载", 
                 font=('微软雅黑', 10),
                 width=12,
                 command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区
        result_frame = tk.LabelFrame(right_panel, text="评测结果", 
                                    font=('微软雅黑', 11, 'bold'))
        result_frame.pack(fill=tk.X, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, 
                                                     font=('Consolas', 10),
                                                     wrap=tk.WORD)
        self.result_text.pack(fill=tk.X, padx=10, pady=5)
        self.result_text.insert(tk.END, "等待提交...")
        self.result_text.config(state=tk.DISABLED)
        
        # 底部按钮
        bottom_frame = tk.Frame(right_panel)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(bottom_frame, text="+ 新建题目", 
                 font=('微软雅黑', 10),
                 command=self.create_problem).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="刷新列表", 
                 font=('微软雅黑', 10),
                 command=self.load_problems).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="导出进度报告", 
                 font=('微软雅黑', 10),
                 command=self.export_report).pack(side=tk.LEFT, padx=5)
        
    def load_problems(self):
        """加载题目列表"""
        # 清空现有列表
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 获取年份列表
        years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
        self.year_combo['values'] = ['全部'] + [str(y) for y in years]
        
        # 筛选题目
        year_filter = self.year_var.get()
        problems = list(self.oj.problems.values())
        
        if year_filter != "全部":
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
                                   font=('微软雅黑', 12, 'bold'),
                                   fg=status_color, bg='white', width=2)
            status_label.pack(side=tk.LEFT, padx=5)
            status_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
            
            # 题号和标题
            text = f"{p.id}: {p.title[:20]}..." if len(p.title) > 20 else f"{p.id}: {p.title}"
            title_label = tk.Label(btn_frame, text=text, 
                                  font=('微软雅黑', 10),
                                  bg='white', anchor=tk.W)
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            title_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
            
            # 提交次数
            if p.submissions:
                count_label = tk.Label(btn_frame, text=f"{len(p.submissions)}次", 
                                      font=('微软雅黑', 9),
                                      fg='#666666', bg='white')
                count_label.pack(side=tk.RIGHT, padx=5)
                count_label.bind('<Button-1>', lambda e, prob=p: self.select_problem(prob))
        
        # 更新统计
        stats = self.oj.get_statistics()
        solved = stats['by_status'].get('已解决', 0)
        total = stats['total']
        self.stats_label.config(text=f"进度: {solved}/{total} ({solved*100//total}%)")
        
    def on_year_change(self, event=None):
        """年份筛选变化"""
        self.load_problems()
        
    def select_problem(self, problem):
        """选择题目"""
        self.current_problem = problem
        
        # 更新标题
        self.problem_title.config(text=f"{problem.id}: {problem.title}")
        
        # 更新信息
        info_text = f"年份: {problem.year} | 状态: {problem.status.value}"
        if problem.submissions:
            last = problem.submissions[-1]
            info_text += f" | 最近提交: {last.result} ({last.passed}/{last.total})"
        self.problem_info.config(text=info_text)
        
        # 更新描述
        self.problem_desc.config(state=tk.NORMAL)
        self.problem_desc.delete('1.0', tk.END)
        if problem.description:
            self.problem_desc.insert(tk.END, problem.description)
        else:
            self.problem_desc.insert(tk.END, f"题目: {problem.title}\n\n")
            self.problem_desc.insert(tk.END, "暂无详细描述，请根据题号查找原题。\n\n")
            self.problem_desc.insert(tk.END, "提示: 把真题图片发给我，我可以帮你添加完整题目信息！")
        self.problem_desc.config(state=tk.DISABLED)
        
        # 清空结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"已选择题目: {problem.id}\n等待提交代码...")
        self.result_text.config(state=tk.DISABLED)
        
    def submit_code(self, test_only=False):
        """提交代码"""
        if not self.current_problem:
            messagebox.showwarning("提示", "请先选择题目")
            return
        
        # 获取代码
        code = self.code_text.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("提示", "请输入代码")
            return
        
        # 保存代码到临时文件
        temp_file = self.oj.temp_dir / f"submit_{self.current_problem.id}.cpp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 显示评测中
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"正在评测 {self.current_problem.id}...\n")
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
                    color = "#00AA00"
                elif r.result == JudgeResult.WA:
                    status = "✗ Wrong Answer"
                    color = "#AA0000"
                elif r.result == JudgeResult.TLE:
                    status = "⏱ Time Limit"
                    color = "#FF9800"
                elif r.result == JudgeResult.RE:
                    status = "⚠ Runtime Error"
                    color = "#AA0000"
                else:
                    status = f"✗ {r.result.value}"
                    color = "#AA0000"
                
                self.result_text.insert(tk.END, f"测试点 {r.test_case_num}: ")
                self.result_text.insert(tk.END, f"{status}\n", color)
            
            self.result_text.insert(tk.END, f"\n{'='*50}\n")
            
            if ac_count == total:
                self.result_text.insert(tk.END, f"\n✓ 全部通过！({ac_count}/{total})\n", "#00AA00")
                if not test_only:
                    self.result_text.insert(tk.END, "题目已标记为已解决！\n")
            else:
                self.result_text.insert(tk.END, f"\n✗ 未通过 ({ac_count}/{total})\n", "#AA0000")
            
            self.result_text.config(state=tk.DISABLED)
            
            # 刷新列表
            if not test_only:
                self.load_problems()
                
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"\n错误: {str(e)}\n")
            self.result_text.config(state=tk.DISABLED)
        finally:
            # 清理临时文件
            if temp_file.exists():
                temp_file.unlink()
                
    def clear_code(self):
        """清空代码"""
        if messagebox.askyesno("确认", "确定要清空代码吗？"):
            self.code_text.delete('1.0', tk.END)
            
    def load_from_file(self):
        """从文件加载代码"""
        filename = filedialog.askopenfilename(
            title="选择 C++ 代码文件",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_text.delete('1.0', tk.END)
                self.code_text.insert(tk.END, code)
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {e}")
                
    def create_problem(self):
        """创建新题目"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建题目")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        
        tk.Label(dialog, text="年份:", font=('微软雅黑', 11)).pack(pady=5)
        year_entry = tk.Entry(dialog, font=('微软雅黑', 11), width=20)
        year_entry.pack()
        year_entry.insert(0, "2025")
        
        tk.Label(dialog, text="题号:", font=('微软雅黑', 11)).pack(pady=5)
        num_entry = tk.Entry(dialog, font=('微软雅黑', 11), width=20)
        num_entry.pack()
        num_entry.insert(0, "1")
        
        tk.Label(dialog, text="标题:", font=('微软雅黑', 11)).pack(pady=5)
        title_entry = tk.Entry(dialog, font=('微软雅黑', 11), width=30)
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
                    messagebox.showinfo("成功", "题目创建成功！")
                else:
                    messagebox.showwarning("提示", "请输入标题")
            except ValueError:
                messagebox.showerror("错误", "年份和题号必须是数字")
        
        tk.Button(dialog, text="创建", font=('微软雅黑', 11),
                 bg='#003366', fg='white', width=10,
                 command=do_create).pack(pady=15)
        
    def export_report(self):
        """导出进度报告"""
        try:
            self.oj.export_progress()
            messagebox.showinfo("成功", "进度报告已导出到 data/progress_report.md")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")

def main():
    root = tk.Tk()
    app = BUAAOJApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
