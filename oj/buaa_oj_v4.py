#!/usr/bin/env python3
"""
北航 OJ 图形界面 V4 - 新增功能
- 查看历史提交记录
- 解题后显示最优解法
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import re
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from buaa_oj import BUAAOJ, ProblemStatus
    from oj_system import JudgeResult
except ImportError as e:
    print(f"Import error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

class BUAAOJV4:
    def __init__(self, root):
        self.root = root
        self.root.title("BUAA OJ 刷题系统")
        self.root.geometry("1800x1000")

        # Refined dark palette with stronger contrast and clearer hierarchy.
        self.theme = {
            'bg': '#17191c',
            'panel': '#1f2328',
            'panel_alt': '#252a31',
            'card': '#2b3138',
            'input': '#181c20',
            'border': '#4b5563',
            'border_soft': '#39424e',
            'text': '#f3f4f6',
            'text_soft': '#d8dee7',
            'muted': '#bcc6d1',
            'accent': '#0ea5c6',
            'accent_hover': '#38bdf8',
            'accent_soft': '#0f3340',
            'success': '#34d399',
            'warning': '#f6c65b',
            'error': '#fb7185'
        }

        self.root.configure(bg=self.theme['bg'])
        self.problem_cards = {}
        self.configure_ttk_styles()
        
        # 初始化 OJ
        self.oj = BUAAOJ()
        self.current_problem = None
        self.left_visible = True
        self.is_judging = False
        self.pending_hot_reload = False
        
        self.create_ui()
        self.apply_theme_recursive(self.root)
        self.load_problems()

        # 题库热更新：检测 data/years 与 problems 目录变化并自动刷新。
        self.hot_reload_interval_ms = 2000
        self._last_source_signature = self.build_problem_source_signature()
        self.schedule_hot_reload()

    def build_problem_source_signature(self):
        """构建题库文件签名，用于检测热更新。"""
        targets = [
            self.oj.years_dir,
            self.oj.base_dir / "problems",
        ]

        signature = []
        for target in targets:
            file_count = 0
            latest_mtime = 0.0
            path = Path(target)
            if path.exists():
                for root, _, files in os.walk(path):
                    for name in files:
                        if not name.endswith((".json", ".md", ".in", ".out")):
                            continue
                        file_count += 1
                        try:
                            mtime = os.path.getmtime(os.path.join(root, name))
                            if mtime > latest_mtime:
                                latest_mtime = mtime
                        except OSError:
                            continue
            signature.append((str(path), file_count, int(latest_mtime)))

        return tuple(signature)

    def apply_hot_reload(self):
        """执行题库热更新并尽量保持当前界面状态。"""
        selected_id = self.current_problem.id if self.current_problem else None
        selected_year = self.year_var.get()
        fav_only = self.fav_only_var.get()

        self.oj.reload_all_problems()
        self.year_var.set(selected_year)
        self.fav_only_var.set(fav_only)
        self.load_problems()

        if selected_id and selected_id in self.oj.problems:
            self.select_problem(self.oj.problems[selected_id], update_result_panel=not self.is_judging)
        else:
            self.current_problem = None

        self.hot_reload_status_label.config(text="题库已自动刷新", fg=self.theme['success'])

    def schedule_hot_reload(self):
        """周期性检测题库变化并刷新界面。"""
        try:
            current_signature = self.build_problem_source_signature()
            if current_signature != self._last_source_signature:
                self._last_source_signature = current_signature
                if self.is_judging:
                    self.pending_hot_reload = True
                    self.hot_reload_status_label.config(text="检测到题库更新，评测后自动刷新", fg=self.theme['warning'])
                else:
                    self.apply_hot_reload()
        except Exception:
            pass
        finally:
            self.root.after(self.hot_reload_interval_ms, self.schedule_hot_reload)

    def configure_ttk_styles(self):
        """Configure ttk controls to match dark UI."""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure('TCombobox',
                        fieldbackground=self.theme['input'],
                        background=self.theme['panel_alt'],
                        foreground=self.theme['text'],
                        bordercolor=self.theme['border'],
                        lightcolor=self.theme['border'],
                        darkcolor=self.theme['border'],
                        arrowcolor=self.theme['text'],
                        insertcolor=self.theme['text'],
                        padding=(8, 6))
        style.map('TCombobox',
                  fieldbackground=[('readonly', self.theme['input'])],
                  background=[('readonly', self.theme['panel_alt'])],
                  foreground=[('readonly', self.theme['text'])],
                  arrowcolor=[('active', self.theme['accent_hover'])])

        style.configure('Treeview',
                        background=self.theme['input'],
                        foreground=self.theme['text_soft'],
                        fieldbackground=self.theme['input'],
                        bordercolor=self.theme['border'],
                        rowheight=28)
        style.map('Treeview',
                  background=[('selected', self.theme['accent_soft'])],
                  foreground=[('selected', '#ffffff')])

        style.configure('Treeview.Heading',
                        background=self.theme['panel_alt'],
                        foreground=self.theme['text'],
                        bordercolor=self.theme['border'],
                        relief=tk.FLAT,
                        padding=(8, 8))
        style.map('Treeview.Heading',
                  background=[('active', self.theme['card'])],
                  foreground=[('active', self.theme['text'])])

        style.configure('Vertical.TScrollbar',
                        background=self.theme['panel_alt'],
                        troughcolor=self.theme['panel'],
                        bordercolor=self.theme['panel'],
                        arrowcolor=self.theme['text_soft'])

    def style_scrolled_text(self, widget):
        widget.configure(bg=self.theme['input'],
                         fg=self.theme['text_soft'],
                         insertbackground=self.theme['text'],
                         insertwidth=2,
                         selectbackground=self.theme['accent_soft'],
                         selectforeground='#ffffff',
                         relief=tk.FLAT,
                         bd=1,
                         highlightthickness=1,
                         highlightbackground=self.theme['border_soft'],
                         highlightcolor=self.theme['accent'])

    def style_problem_card(self, frame, selected=False, hover=False):
        bg = self.theme['accent_soft'] if selected else (self.theme['panel_alt'] if hover else self.theme['card'])
        border = self.theme['accent'] if selected else (self.theme['accent_hover'] if hover else self.theme['border_soft'])
        frame.configure(bg=bg, highlightbackground=border, highlightcolor=border, highlightthickness=1, bd=0)
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg)
                for nested in child.winfo_children():
                    if isinstance(nested, tk.Label):
                        role = getattr(nested, '_ui_role', 'primary')
                        fg = self.theme['text']
                        if role == 'meta':
                            fg = self.theme['muted']
                        elif role == 'badge':
                            fg = self.theme['accent_hover'] if not selected else '#ffffff'
                        elif role == 'count':
                            fg = self.theme['text_soft']
                        nested.configure(bg=bg, fg=fg)
            elif isinstance(child, tk.Label):
                role = getattr(child, '_ui_role', 'primary')
                fg = self.theme['text']
                if role == 'meta':
                    fg = self.theme['muted']
                elif role == 'badge':
                    fg = self.theme['accent_hover'] if not selected else '#ffffff'
                elif role == 'count':
                    fg = self.theme['text_soft']
                child.configure(bg=bg, fg=fg)

    def bind_problem_card(self, frame, problem):
        def bind_recursive(widget):
            widget.bind('<Button-1>', lambda e, prob=problem: self.select_problem(prob))
            widget.bind('<Button-3>', lambda e, prob=problem: self.show_problem_menu(e, prob))
            widget.bind('<Enter>', lambda e, pid=problem.id: self.on_problem_card_hover(pid, True))
            widget.bind('<Leave>', lambda e, pid=problem.id: self.on_problem_card_hover(pid, False))
            for child in widget.winfo_children():
                bind_recursive(child)

        bind_recursive(frame)

    def on_problem_card_hover(self, problem_id, hover):
        frame = self.problem_cards.get(problem_id)
        if not frame:
            return
        selected = self.current_problem is not None and self.current_problem.id == problem_id
        self.style_problem_card(frame, selected=selected, hover=hover and not selected)

    def on_problem_list_mousewheel(self, event):
        if event.delta == 0:
            return
        step = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(step, 'units')

    def bind_mousewheel_recursive(self, widget):
        widget.bind('<MouseWheel>', self.on_problem_list_mousewheel)
        for child in widget.winfo_children():
            self.bind_mousewheel_recursive(child)

    def update_problem_card_states(self):
        current_id = self.current_problem.id if self.current_problem else None
        for problem_id, frame in self.problem_cards.items():
            self.style_problem_card(frame, selected=(problem_id == current_id), hover=False)

    def style_menu(self, menu):
        menu.configure(bg=self.theme['panel_alt'],
                       fg=self.theme['text'],
                       activebackground=self.theme['accent_soft'],
                       activeforeground='#ffffff',
                       bd=0,
                       relief=tk.FLAT)

    def apply_theme_recursive(self, widget):
        """Recursively apply dark colors to tk widgets."""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.Toplevel, tk.PanedWindow)):
                widget.configure(bg=self.theme['panel'])
                if isinstance(widget, tk.LabelFrame):
                    widget.configure(fg=self.theme['text_soft'], highlightbackground=self.theme['border_soft'])
            elif isinstance(widget, tk.Canvas):
                widget.configure(bg=self.theme['panel'], highlightbackground=self.theme['border_soft'], bd=0, highlightthickness=0)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.theme['panel'], fg=self.theme['text_soft'])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.theme['panel_alt'],
                                 fg=self.theme['text'],
                                 activebackground=self.theme['accent_hover'],
                                 activeforeground='#ffffff',
                                 relief=tk.FLAT,
                                 bd=0,
                                 padx=12,
                                 pady=6,
                                 cursor='hand2')
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(bg=self.theme['panel'],
                                 fg=self.theme['text_soft'],
                                 activebackground=self.theme['panel'],
                                 activeforeground=self.theme['text'],
                                 selectcolor=self.theme['panel_alt'])
            elif isinstance(widget, (tk.Text, scrolledtext.ScrolledText)):
                self.style_scrolled_text(widget)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=self.theme['input'],
                                 fg=self.theme['text'],
                                 insertbackground=self.theme['text'],
                                 disabledforeground=self.theme['text_soft'],
                                 relief=tk.FLAT,
                                 highlightthickness=1,
                                 highlightbackground=self.theme['border_soft'],
                                 highlightcolor=self.theme['accent'])
            elif isinstance(widget, tk.Menu):
                self.style_menu(widget)
        except Exception:
            pass

        for child in widget.winfo_children():
            self.apply_theme_recursive(child)
        
    def create_ui(self):
        """创建三栏布局界面"""
        # 顶部标题栏
        header = tk.Frame(self.root, bg=self.theme['panel'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="BUAA OJ 刷题系统", 
                              font=('Microsoft YaHei', 16, 'bold'), 
                              bg=self.theme['panel'], fg=self.theme['text'])
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        subtitle_label = tk.Label(header,
                      text="高对比度界面，专注题目阅读、代码提交与结果分析",
                                  font=('Microsoft YaHei', 10),
                                  bg=self.theme['panel'], fg=self.theme['muted'])
        subtitle_label.pack(side=tk.RIGHT, padx=20)
        
        # 主内容区 - 使用PanedWindow实现三栏
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.theme['bg'], sashwidth=8,
                        sashrelief=tk.FLAT, showhandle=False)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ========== 左栏：题目列表 ==========
        self.left_frame = tk.LabelFrame(main_paned, text="题目列表", 
                                        font=('Microsoft YaHei', 11, 'bold'))
        self.left_frame.configure(width=320)
        main_paned.add(self.left_frame, minsize=250)
        
        # 筛选区
        filter_frame = tk.Frame(self.left_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(filter_frame, text="年份", font=('Microsoft YaHei', 10)).pack(side=tk.LEFT)
        self.year_var = tk.StringVar(value="全部")
        self.year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, 
                                       width=8, state="readonly")
        self.year_combo.pack(side=tk.LEFT, padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.on_year_change)
        
        # 只看收藏复选框
        self.fav_only_var = tk.BooleanVar(value=False)
        self.fav_only_check = tk.Checkbutton(filter_frame, text="仅收藏", 
                                             variable=self.fav_only_var,
                                             font=('Microsoft YaHei', 9),
                                             command=self.on_favorite_filter_change)
        self.fav_only_check.pack(side=tk.LEFT, padx=5)
        
        # 题目列表
        list_container = tk.Frame(self.left_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(list_container, width=280)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=280)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<MouseWheel>', self.on_problem_list_mousewheel)
        self.scrollable_frame.bind('<MouseWheel>', self.on_problem_list_mousewheel)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 统计信息
        self.stats_label = tk.Label(self.left_frame, text="进度 0/0", 
                       font=('Microsoft YaHei', 10), fg=self.theme['muted'])
        self.stats_label.pack(pady=5)
        
        # 底部按钮
        btn_frame = tk.Frame(self.left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="+ 新建", font=('Microsoft YaHei', 9),
                 command=self.create_problem).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="刷新", font=('Microsoft YaHei', 9),
                 command=self.load_problems).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="导出", font=('Microsoft YaHei', 9),
                 command=self.export_report).pack(side=tk.LEFT, padx=2)
        
        # ========== 中栏：题目描述 + 历史记录 ==========
        center_frame = tk.Frame(main_paned)
        main_paned.add(center_frame, minsize=600)
        
        # 上方：题目信息
        info_frame = tk.LabelFrame(center_frame, text="题目描述", 
                                   font=('Microsoft YaHei', 11, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.problem_title = tk.Label(info_frame, text="请选择一道题目", 
                         font=('Microsoft YaHei', 16, 'bold'), fg=self.theme['text'])
        self.problem_title.pack(anchor=tk.W, padx=15, pady=10)
        
        self.problem_info = tk.Label(info_frame, text="", 
                                    font=('Microsoft YaHei', 11), fg=self.theme['muted'])
        self.problem_info.pack(anchor=tk.W, padx=15)

        sample_btn_frame = tk.Frame(info_frame, bg=self.theme['panel'])
        sample_btn_frame.pack(anchor=tk.W, padx=15, pady=(8, 4))

        self.copy_sample_input_btn = tk.Button(sample_btn_frame,
                               text="复制样例输入",
                               font=('Microsoft YaHei', 10),
                               state=tk.DISABLED,
                               command=lambda: self.copy_sample_text('input'))
        self.copy_sample_input_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.copy_sample_output_btn = tk.Button(sample_btn_frame,
                            text="复制样例输出",
                            font=('Microsoft YaHei', 10),
                            state=tk.DISABLED,
                            command=lambda: self.copy_sample_text('output'))
        self.copy_sample_output_btn.pack(side=tk.LEFT)
        
        # 题目描述
        self.problem_desc = scrolledtext.ScrolledText(info_frame, 
                                                      font=('Microsoft YaHei', 12),
                                                      wrap=tk.WORD,
                                                      padx=10, pady=10)
        self.problem_desc.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.style_scrolled_text(self.problem_desc)
        self.configure_problem_desc_tags()
        self.problem_desc.insert(tk.END, "请从左侧题目列表中选择一道题查看详情。")
        self.problem_desc.config(state=tk.DISABLED)
        
        # 折叠左栏按钮
        self.toggle_left_btn = tk.Button(info_frame, text="◀", 
                                        font=('Microsoft YaHei', 10, 'bold'),
                                        bg=self.theme['accent'], fg='white',
                                        width=2, command=self.toggle_left)
        self.toggle_left_btn.place(x=5, y=5)
        
        # 下方：历史提交记录
        history_frame = tk.LabelFrame(center_frame, text="提交历史", 
                                      font=('Microsoft YaHei', 11, 'bold'))
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 历史记录列表
        self.history_tree = ttk.Treeview(history_frame, columns=('time', 'result', 'detail'), 
                                         show='headings', height=8)
        self.history_tree.heading('time', text='提交时间')
        self.history_tree.heading('result', text='结果')
        self.history_tree.heading('detail', text='详情')
        
        self.history_tree.column('time', width=150)
        self.history_tree.column('result', width=100)
        self.history_tree.column('detail', width=300)
        
        history_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 查看代码按钮
        tk.Button(history_frame, text="查看代码", font=('Microsoft YaHei', 10),
                 command=self.view_history_code).pack(anchor=tk.W, padx=5, pady=5)
        
        # ========== 右栏：代码提交 + 最优解法 ==========
        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame, minsize=450)
        
        # 上方：代码提交
        submit_frame = tk.LabelFrame(right_frame, text="代码提交", 
                                    font=('Microsoft YaHei', 11, 'bold'))
        submit_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        code_label = tk.Label(submit_frame, text="在这里粘贴 C++ 代码：", 
                             font=('Microsoft YaHei', 11))
        code_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.code_text = scrolledtext.ScrolledText(submit_frame, 
                                                   font=('Consolas', 12),
                                                   wrap=tk.NONE,
                                                   padx=5, pady=5)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.style_scrolled_text(self.code_text)
        
        # 按钮区
        btn_frame2 = tk.Frame(submit_frame)
        btn_frame2.pack(fill=tk.X, padx=10, pady=10)
        
        self.test_btn = tk.Button(btn_frame2, text="测试运行", 
                                 font=('Microsoft YaHei', 11, 'bold'),
                                 bg=self.theme['warning'], fg='#1e1e1e',
                                 width=12, height=1,
                                 command=lambda: self.submit_code(test_only=True))
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.submit_btn = tk.Button(btn_frame2, text="正式提交", 
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg=self.theme['accent'], fg='white',
                                   width=12, height=1,
                                   command=lambda: self.submit_code(test_only=False))
        self.submit_btn.pack(side=tk.LEFT, padx=5)
        
        btn_frame3 = tk.Frame(submit_frame)
        btn_frame3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame3, text="清空", font=('Microsoft YaHei', 10),
                 width=10, command=self.clear_code).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame3, text="载入文件", font=('Microsoft YaHei', 10),
                 width=10, command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区
        result_frame = tk.LabelFrame(right_frame, text="判题结果", 
                                    font=('Microsoft YaHei', 11, 'bold'))
        result_frame.pack(fill=tk.X, padx=5, pady=5)

        self.hot_reload_status_label = tk.Label(result_frame,
                            text="",
                            font=('Microsoft YaHei', 9),
                            fg=self.theme['muted'],
                            bg=self.theme['panel'],
                            anchor='w', justify=tk.LEFT)
        self.hot_reload_status_label.pack(fill=tk.X, padx=10, pady=(4, 0))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, 
                                                     font=('Consolas', 11),
                                                     wrap=tk.WORD,
                                                     padx=5, pady=5)
        self.result_text.pack(fill=tk.X, padx=10, pady=5)
        self.style_scrolled_text(self.result_text)
        self.result_text.insert(tk.END, "等待提交代码...")
        self.result_text.config(state=tk.DISABLED)
        
        # 配置文本标签颜色
        self.result_text.tag_configure("green", foreground=self.theme['success'])
        self.result_text.tag_configure("red", foreground=self.theme['error'])
        self.result_text.tag_configure("orange", foreground=self.theme['warning'])
        self.result_text.tag_configure("error_detail", foreground=self.theme['muted'], font=('Consolas', 9))
        
        # 下方：最优解法按钮（点击弹出大窗口）
        self.solution_frame = tk.LabelFrame(right_frame, text="参考解法", 
                                           font=('Microsoft YaHei', 11, 'bold'))
        self.solution_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 状态标签（未解锁时显示）
        self.solution_status_label = tk.Label(self.solution_frame, 
                                             text="解锁后可查看参考解法",
                                             font=('Microsoft YaHei', 10),
                                             fg=self.theme['muted'])
        self.solution_status_label.pack(padx=10, pady=10)
        
        # 查看解法按钮（解锁后显示，点击弹出大窗口）
        self.view_solution_btn = tk.Button(self.solution_frame, 
                                          text="点击查看参考解法",
                                          font=('Microsoft YaHei', 12, 'bold'),
                                          bg=self.theme['success'], 
                                          fg='white',
                                          activebackground=self.theme['accent_hover'],
                                          activeforeground='white',
                                          height=2,
                                          cursor='hand2',
                                          state=tk.DISABLED,
                                          command=self.view_solution)
        self.view_solution_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # 让状态标签也可以点击（双重保障）
        self.solution_status_label.bind('<Button-1>', lambda e: self.view_solution() if self.view_solution_btn['state'] == 'normal' else None)
        
    def toggle_left(self):
        """切换左栏显示/隐藏"""
        if self.left_visible:
            self.left_frame.pack_forget()
            self.toggle_left_btn.config(text="▶")
            self.left_visible = False
        else:
            self.left_visible = True
            self.load_problems()
            self.toggle_left_btn.config(text="◀")
            
    def load_problems(self):
        """加载题目列表"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.problem_cards = {}
        self.bind_mousewheel_recursive(self.scrollable_frame)
        
        years = sorted(set(p.year for p in self.oj.problems.values()), reverse=True)
        self.year_combo['values'] = ['全部'] + [str(y) for y in years]
        
        year_filter = self.year_var.get()
        fav_only = self.fav_only_var.get()
        problems = list(self.oj.problems.values())
        
        if year_filter != "全部":
            problems = [p for p in problems if p.year == int(year_filter)]
        
        if fav_only:
            problems = [p for p in problems if p.is_favorite]
        
        problems.sort(key=lambda p: (p.year, p.id))
        
        for i, p in enumerate(problems):
            if p.status == ProblemStatus.SOLVED:
                status_color = self.theme['success']
                status_text = '✓'
            elif p.status == ProblemStatus.ATTEMPTED:
                status_color = self.theme['warning']
                status_text = '△'
            else:
                status_color = self.theme['muted']
                status_text = '○'
            
            btn_frame = tk.Frame(self.scrollable_frame, bg=self.theme['card'], bd=0,
                                 relief=tk.FLAT, highlightbackground=self.theme['border_soft'],
                                 highlightthickness=1)
            btn_frame.pack(fill=tk.X, padx=2, pady=2)
            self.problem_cards[p.id] = btn_frame
            
            top_row = tk.Frame(btn_frame, bg=self.theme['card'])
            top_row.pack(fill=tk.X, padx=10, pady=(8, 2))

            fav_text = "⭐" if p.is_favorite else "·"
            fav_label = tk.Label(top_row, text=fav_text,
                                font=('Microsoft YaHei', 11),
                                bg=self.theme['card'], fg=self.theme['warning'], width=2)
            fav_label._ui_role = 'badge'
            fav_label.pack(side=tk.LEFT)

            status_label = tk.Label(top_row, text=status_text,
                                   font=('Microsoft YaHei', 12, 'bold'),
                                   fg=status_color, bg=self.theme['card'], width=2)
            status_label._ui_role = 'badge'
            status_label.pack(side=tk.LEFT, padx=(0, 4))

            max_title_len = 16
            short_title = p.title[:max_title_len] + "..." if len(p.title) > max_title_len else p.title
            title_text = f"{p.id}  {short_title}"
            if p.annotation:
                title_text += "  📝"
            title_label = tk.Label(top_row, text=title_text,
                                  font=('Microsoft YaHei', 10, 'bold'),
                                  bg=self.theme['card'], fg=self.theme['text'], anchor=tk.W, justify=tk.LEFT)
            title_label._ui_role = 'primary'
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            bottom_row = tk.Frame(btn_frame, bg=self.theme['card'])
            bottom_row.pack(fill=tk.X, padx=10, pady=(0, 8))

            meta_text = f"{p.year} 年  |  状态：{p.status.value}"
            meta_label = tk.Label(bottom_row, text=meta_text,
                                  font=('Microsoft YaHei', 9),
                                  bg=self.theme['card'], fg=self.theme['muted'], anchor=tk.W)
            meta_label._ui_role = 'meta'
            meta_label.pack(side=tk.LEFT)

            count_text = f"提交 {len(p.submissions)} 次" if p.submissions else "未提交"
            count_label = tk.Label(bottom_row, text=count_text,
                                  font=('Microsoft YaHei', 9),
                                  fg=self.theme['muted'], bg=self.theme['card'], anchor=tk.E, justify=tk.RIGHT)
            count_label._ui_role = 'count'
            count_label.pack(side=tk.RIGHT)

            self.bind_problem_card(btn_frame, p)
            self.bind_mousewheel_recursive(btn_frame)
            self.style_problem_card(btn_frame,
                                    selected=self.current_problem is not None and self.current_problem.id == p.id,
                                    hover=False)
        
        stats = self.oj.get_statistics()
        solved = stats['by_status'].get('已解决', 0)
        total = stats['total']
        fav_count = sum(1 for p in self.oj.problems.values() if p.is_favorite)
        pct = solved*100//total if total > 0 else 0
        self.stats_label.config(text=f"进度 {solved}/{total} ({pct}%)   收藏 {fav_count}")
        
    def on_year_change(self, event=None):
        """年份筛选变化"""
        self.load_problems()
    
    def on_favorite_filter_change(self):
        """收藏筛选变化"""
        self.load_problems()

    def configure_problem_desc_tags(self):
        """配置题面 Markdown 渲染样式。"""
        self.problem_desc.tag_configure("md_h1", font=('Microsoft YaHei', 18, 'bold'), foreground=self.theme['text'])
        self.problem_desc.tag_configure("md_h2", font=('Microsoft YaHei', 15, 'bold'), foreground=self.theme['text'])
        self.problem_desc.tag_configure("md_h3", font=('Microsoft YaHei', 13, 'bold'), foreground=self.theme['text_soft'])
        self.problem_desc.tag_configure("md_body", font=('Microsoft YaHei', 12), foreground=self.theme['text_soft'])
        self.problem_desc.tag_configure("md_list", font=('Microsoft YaHei', 12), foreground=self.theme['text_soft'], lmargin1=20, lmargin2=32)
        self.problem_desc.tag_configure("md_code", font=('Consolas', 11), foreground='#e2e8f0', background='#0f141b', lmargin1=18, lmargin2=18)
        self.problem_desc.tag_configure("md_code_inline", font=('Consolas', 11), foreground='#a5f3fc')

    def insert_inline_markdown(self, line: str):
        """渲染行内 `code` 片段。"""
        parts = re.split(r'(`[^`]*`)', line)
        for part in parts:
            if not part:
                continue
            if part.startswith('`') and part.endswith('`') and len(part) >= 2:
                self.problem_desc.insert(tk.END, part[1:-1], "md_code_inline")
            else:
                self.problem_desc.insert(tk.END, part, "md_body")
        self.problem_desc.insert(tk.END, "\n", "md_body")

    def render_problem_markdown(self, content: str):
        """将题面 Markdown 以可读样式渲染到文本框。"""
        self.problem_desc.config(state=tk.NORMAL)
        self.problem_desc.delete('1.0', tk.END)

        in_code_block = False
        for raw_line in content.splitlines():
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if stripped.startswith("```"):
                in_code_block = not in_code_block
                if not in_code_block:
                    self.problem_desc.insert(tk.END, "\n", "md_body")
                continue

            if in_code_block:
                self.problem_desc.insert(tk.END, line + "\n", "md_code")
                continue

            if not stripped:
                self.problem_desc.insert(tk.END, "\n", "md_body")
                continue

            if stripped.startswith("# "):
                self.problem_desc.insert(tk.END, stripped[2:] + "\n\n", "md_h1")
                continue
            if stripped.startswith("## "):
                self.problem_desc.insert(tk.END, stripped[3:] + "\n", "md_h2")
                continue
            if stripped.startswith("### "):
                self.problem_desc.insert(tk.END, stripped[4:] + "\n", "md_h3")
                continue

            if stripped.startswith("- "):
                self.problem_desc.insert(tk.END, "• " + stripped[2:] + "\n", "md_list")
                continue

            if re.match(r'^\d+\.\s+', stripped):
                self.problem_desc.insert(tk.END, stripped + "\n", "md_list")
                continue

            self.insert_inline_markdown(line)

        self.problem_desc.config(state=tk.DISABLED)

    def get_problem_statement(self, problem):
        """优先读取 problem.md，其次回退到 data/years 中的 description。"""
        statement_file = self.oj.base_dir / "problems" / problem.id / "problem.md"
        if statement_file.exists():
            try:
                with open(statement_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception:
                pass

        if problem.description:
            return problem.description.strip()

        return f"题目：{problem.title}\n\n暂无更详细的题面内容。"

    def extract_sample_sections(self, content: str):
        """从 Markdown 题面中提取样例输入/输出代码块。"""
        samples = {"input": "", "output": ""}
        current = None
        in_code_block = False
        buffer = []

        for raw_line in content.splitlines():
            stripped = raw_line.strip()

            if stripped in {"## 样例输入", "### 样例输入", "【样例输入】"}:
                current = "input"
                in_code_block = False
                buffer = []
                continue

            if stripped in {"## 样例输出", "### 样例输出", "【样例输出】"}:
                current = "output"
                in_code_block = False
                buffer = []
                continue

            if current is None:
                continue

            if stripped.startswith("```"):
                if in_code_block:
                    samples[current] = "\n".join(buffer).strip()
                    current = None
                    in_code_block = False
                    buffer = []
                else:
                    in_code_block = True
                continue

            if in_code_block:
                buffer.append(raw_line)
            elif stripped and not stripped.startswith("## ") and not stripped.startswith("### "):
                buffer.append(raw_line)
            elif buffer:
                samples[current] = "\n".join(buffer).strip()
                current = None
                buffer = []

        if current and buffer and not samples[current]:
            samples[current] = "\n".join(buffer).strip()

        return samples

    def update_sample_buttons(self, statement: str):
        """根据题面样例更新复制按钮状态。"""
        self.current_samples = self.extract_sample_sections(statement)

        input_state = tk.NORMAL if self.current_samples.get('input') else tk.DISABLED
        output_state = tk.NORMAL if self.current_samples.get('output') else tk.DISABLED
        self.copy_sample_input_btn.config(state=input_state)
        self.copy_sample_output_btn.config(state=output_state)

    def copy_sample_text(self, kind: str):
        """复制样例输入或样例输出到剪贴板。"""
        text = getattr(self, 'current_samples', {}).get(kind, '').strip()
        if not text:
            messagebox.showinfo("提示", "当前题目没有可复制的样例内容。")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        label = "样例输入" if kind == 'input' else "样例输出"
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"已复制{label}到剪贴板。")
        self.result_text.config(state=tk.DISABLED)
        
    def select_problem(self, problem, update_result_panel=True):
        """选择题目"""
        self.current_problem = problem
        
        self.problem_title.config(text=f"{problem.id}: {problem.title}")
        
        info_text = f"年份：{problem.year}  |  状态：{problem.status.value}"
        if problem.submissions:
            last = problem.submissions[-1]
            info_text += f"  |  最近一次：{last.result} ({last.passed}/{last.total})"
        self.problem_info.config(text=info_text)
        self.update_problem_card_states()

        statement = self.get_problem_statement(problem)
        self.render_problem_markdown(statement)
        self.update_sample_buttons(statement)
        
        # 更新历史记录
        self.update_history()
        
        # 更新最优解法显示
        self.update_solution_view()
        
        if update_result_panel:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"已选择题目：{problem.id}\n可以开始测试运行或正式提交。")
            self.result_text.config(state=tk.DISABLED)

            # 显示批注（如果有）
            if problem.annotation:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"\n\n{'='*50}\n批注：\n{problem.annotation}\n{'='*50}")
                self.result_text.config(state=tk.DISABLED)
        
    def show_problem_menu(self, event, problem):
        """显示题目右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        self.style_menu(menu)
        
        # 收藏/取消收藏
        if problem.is_favorite:
            menu.add_command(label="取消收藏", command=lambda: self.toggle_favorite(problem))
        else:
            menu.add_command(label="加入收藏", command=lambda: self.toggle_favorite(problem))
        
        menu.add_separator()
        
        # 批注
        if problem.annotation:
            menu.add_command(label="编辑批注", command=lambda: self.edit_annotation(problem))
            menu.add_command(label="查看批注", command=lambda: self.view_annotation(problem))
        else:
            menu.add_command(label="添加批注", command=lambda: self.edit_annotation(problem))
        
        menu.add_separator()
        
        # 选择题目
        menu.add_command(label="查看题目", command=lambda: self.select_problem(problem))
        
        menu.tk_popup(event.x_root, event.y_root)
    
    def toggle_favorite(self, problem):
        """切换题目收藏状态"""
        is_fav = self.oj.toggle_favorite(problem.id)
        status = "added to" if is_fav else "removed from"
        self.load_problems()  # 刷新列表显示
        # 可选：显示提示
        # messagebox.showinfo("Favorite", f"Problem {problem.id} {status} favorites!")
    
    def edit_annotation(self, problem):
        """编辑题目批注"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"题目批注 - {problem.id}")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.theme['panel'])
        self.apply_theme_recursive(dialog)
        
        # 标题
        tk.Label(dialog, text=f"题目批注：{problem.id}", 
                font=('Microsoft YaHei', 12, 'bold')).pack(pady=10)
        
        # 文本框
        text_frame = tk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(text_frame, wrap=tk.WORD, font=('Microsoft YaHei', 11),
                      yscrollcommand=scrollbar.set, height=8)
        text.pack(fill=tk.BOTH, expand=True)
        self.style_scrolled_text(text)
        scrollbar.config(command=text.yview)
        
        # 填充现有批注
        if problem.annotation:
            text.insert('1.0', problem.annotation)
        
        # 按钮
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def save():
            content = text.get('1.0', tk.END).strip()
            self.oj.update_annotation(problem.id, content)
            self.load_problems()  # 刷新列表显示批注标记
            # 如果当前选中的是这道题，刷新显示
            if self.current_problem and self.current_problem.id == problem.id:
                self.select_problem(self.oj.problems[problem.id])
            dialog.destroy()
        
        def clear():
            if messagebox.askyesno("确认", "确定清空这条批注吗？"):
                text.delete('1.0', tk.END)
        
        tk.Button(btn_frame, text="保存", command=save, bg=self.theme['success'], fg='#1e1e1e',
                 font=('Microsoft YaHei', 10, 'bold'), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="清空", command=clear, 
                 font=('Microsoft YaHei', 10), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", command=dialog.destroy,
                 font=('Microsoft YaHei', 10), width=10).pack(side=tk.LEFT, padx=5)
        
        text.focus_set()
    
    def view_annotation(self, problem):
        """查看题目批注"""
        if not problem.annotation:
            messagebox.showinfo("批注", "这道题还没有批注。")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"题目批注 - {problem.id}")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.configure(bg=self.theme['panel'])
        self.apply_theme_recursive(dialog)
        
        tk.Label(dialog, text=f"题目批注：{problem.id}", 
                font=('Microsoft YaHei', 12, 'bold')).pack(pady=10)
        
        text = tk.Text(dialog, wrap=tk.WORD, font=('Microsoft YaHei', 11),
                      bg=self.theme['card'], fg=self.theme['text'],
                      insertbackground=self.theme['text'], padx=10, pady=10, height=10)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.style_scrolled_text(text)
        text.insert('1.0', problem.annotation)
        text.config(state=tk.DISABLED)
        
        tk.Button(dialog, text="编辑", command=lambda: [dialog.destroy(), self.edit_annotation(problem)],
                 bg=self.theme['accent'], fg='white', font=('Microsoft YaHei', 10), width=10).pack(pady=10)
    
    def update_history(self):
        """更新历史提交记录显示"""
        # 清空历史记录列表
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if not self.current_problem or not self.current_problem.submissions:
            return
        
        # 添加历史记录（最新的在前）
        for s in reversed(self.current_problem.submissions):
            if s.result == "AC":
                result_text = "✓ 通过"
            else:
                result_text = f"✗ {s.result}"
            
            detail = f"通过测试点 {s.passed}/{s.total}"
            if s.notes:
                detail += f" | {s.notes}"
            
            self.history_tree.insert('', tk.END, values=(s.timestamp, result_text, detail))
    
    def view_history_code(self):
        """查看历史提交的代码"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先在提交历史里选择一条记录。")
            return
        
        if not self.current_problem:
            return
        
        # 获取选中的索引
        item = self.history_tree.item(selection[0])
        selected_time = item['values'][0]
        
        # 找到对应的提交记录
        for s in self.current_problem.submissions:
            if s.timestamp == selected_time:
                # 显示代码
                self.show_code_dialog(f"提交代码 - {s.timestamp}", s.code_file)
                return
    
    def show_code_dialog(self, title, code_file):
        """显示代码的对话框"""
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            dialog = tk.Toplevel(self.root)
            dialog.title(title)
            dialog.geometry("800x600")
            dialog.configure(bg=self.theme['panel'])
            self.apply_theme_recursive(dialog)
            
            text = scrolledtext.ScrolledText(dialog, font=('Consolas', 11))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.style_scrolled_text(text)
            text.insert(tk.END, code)
            text.config(state=tk.DISABLED)
            
            tk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)
        except Exception as e:
            messagebox.showerror("错误", f"读取代码文件失败：{e}")
    
    def update_solution_view(self):
        """更新最优解法显示"""
        if not self.current_problem:
            self.solution_status_label.config(text="请选择一道题后查看参考解法", fg=self.theme['muted'])
            self.solution_status_label.pack(padx=10, pady=10)
            self.view_solution_btn.config(state=tk.DISABLED, text="点击查看参考解法", bg=self.theme['muted'])
        elif self.current_problem.status == ProblemStatus.SOLVED:
            # 已解决，启用按钮，隐藏状态标签让按钮更突出
            self.solution_status_label.pack_forget()  # 隐藏状态标签
            self.view_solution_btn.config(
                state=tk.NORMAL,
                text="查看参考解法",
                bg=self.theme['success']
            )
        else:
            # 未解决，禁用按钮
            self.solution_status_label.pack(padx=10, pady=10)
            self.solution_status_label.config(
                text="解锁后可查看参考解法",
                fg=self.theme['muted']
            )
            self.view_solution_btn.config(state=tk.DISABLED, text="点击查看参考解法", bg=self.theme['muted'])
    
    def view_solution(self):
        """查看参考解法 - 弹出大窗口"""
        if not self.current_problem:
            return
        
        # 优先显示优化版本
        optimized_file = f"solutions/{self.current_problem.id}_optimized.cpp"
        solution_file = f"solutions/{self.current_problem.id}_solution.cpp"
        
        # 创建大窗口显示解法
        dialog = tk.Toplevel(self.root)
        dialog.title(f"参考解法 - {self.current_problem.id}")
        dialog.geometry("1200x800")
        dialog.configure(bg=self.theme['panel'])
        self.apply_theme_recursive(dialog)
        
        # 标题
        title_frame = tk.Frame(dialog, bg=self.theme['panel'], height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, 
                text=f"参考解法：{self.current_problem.id} - {self.current_problem.title}",
                font=('Microsoft YaHei', 16, 'bold'),
                bg=self.theme['panel'], fg=self.theme['text']).pack(pady=15)
        
        # 如果有优化版本，显示选择按钮
        has_optimized = os.path.exists(optimized_file)
        has_standard = os.path.exists(solution_file)
        
        if has_optimized and has_standard:
            btn_frame = tk.Frame(dialog)
            btn_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Button(btn_frame, text="标准解法", 
                     font=('Microsoft YaHei', 11),
                     command=lambda: self.load_solution_to_dialog(text_area, solution_file)).pack(side=tk.LEFT, padx=5)
            
            tk.Button(btn_frame, text="优化解法", 
                     font=('Microsoft YaHei', 11),
                     bg=self.theme['success'], fg='#1e1e1e',
                     command=lambda: self.load_solution_to_dialog(text_area, optimized_file)).pack(side=tk.LEFT, padx=5)
        
        # 代码显示区域
        text_area = scrolledtext.ScrolledText(dialog, 
                                              font=('Consolas', 12),
                                              wrap=tk.NONE,
                                              padx=10, pady=10)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.style_scrolled_text(text_area)
        
        # 默认加载优化版本或标准版本
        if has_optimized:
            self.load_solution_to_dialog(text_area, optimized_file)
        elif has_standard:
            self.load_solution_to_dialog(text_area, solution_file)
        else:
            text_area.insert(tk.END, "暂时还没有可用的参考解法。")
            text_area.config(state=tk.DISABLED)
        
        # 关闭按钮
        tk.Button(dialog, text="关闭", 
                 font=('Microsoft YaHei', 12),
                 width=15, command=dialog.destroy).pack(pady=10)
    
    def load_solution_to_dialog(self, text_widget, file_path):
        """加载解法到对话框"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            text_widget.config(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, f"// File: {file_path}\n")
            text_widget.insert(tk.END, f"// {'='*60}\n\n")
            text_widget.insert(tk.END, code)
            text_widget.config(state=tk.DISABLED)
        except Exception as e:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, f"加载参考解法失败：{e}")
            text_widget.config(state=tk.DISABLED)
        
    def submit_code(self, test_only=False):
        """提交代码"""
        if not self.current_problem:
            messagebox.showwarning("提示", "请先选择一道题目。")
            return
        
        code = self.code_text.get('1.0', tk.END).strip()
        if not code:
            messagebox.showwarning("提示", "请先输入代码。")
            return
        
        temp_file = self.oj.oj.temp_dir / f"submit_{self.current_problem.id}.cpp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"正在评测 {self.current_problem.id}...\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.config(state=tk.DISABLED)
        self.is_judging = True
        self.hot_reload_status_label.config(text="评测进行中...", fg=self.theme['muted'])
        self.root.update()
        
        try:
            if test_only:
                results = self.oj.oj.judge(self.current_problem.id, str(temp_file))
            else:
                results = self.oj.submit(self.current_problem.id, str(temp_file))
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            
            ac_count = sum(1 for r in results if r.result == JudgeResult.AC)
            total = len(results)
            
            for r in results:
                if r.result == JudgeResult.AC:
                    status = "✓ 通过"
                    color_tag = "green"
                elif r.result == JudgeResult.WA:
                    status = "✗ 答案错误"
                    color_tag = "red"
                elif r.result == JudgeResult.TLE:
                    status = "⏱ 超时"
                    color_tag = "orange"
                elif r.result == JudgeResult.RE:
                    status = "⚠ 运行错误"
                    color_tag = "red"
                elif r.result == JudgeResult.CE:
                    status = "✗ 编译错误"
                    color_tag = "red"
                else:
                    status = f"✗ {r.result.value}"
                    color_tag = "red"
                
                self.result_text.insert(tk.END, f"Test {r.test_case_num}: {status} ({r.time_used:.1f}ms)\n", color_tag)
                
                if r.message and r.result != JudgeResult.AC:
                    msg = r.message[:500] + "..." if len(r.message) > 500 else r.message
                    self.result_text.insert(tk.END, f"  错误信息：{msg}\n", "error_detail")
            
            self.result_text.insert(tk.END, f"\n{'='*50}\n")
            
            if ac_count == total:
                self.result_text.insert(tk.END, f"\n✓ 全部通过 ({ac_count}/{total})\n", "green")
                if not test_only:
                    self.result_text.insert(tk.END, "题目状态已更新为已解决。\n", "green")
                    self.result_text.insert(tk.END, "现在可以查看参考解法。\n", "green")
            else:
                self.result_text.insert(tk.END, f"\n✗ 未通过 ({ac_count}/{total})\n", "red")
                for r in results:
                    if r.result != JudgeResult.AC:
                        self.result_text.insert(tk.END, f"\n首个失败测试点：{r.test_case_num}\n", "orange")
                        if r.message:
                            self.result_text.insert(tk.END, f"错误详情：\n{r.message[:1000]}\n", "error_detail")
                        break
            
            self.result_text.config(state=tk.DISABLED)
            
            if not test_only:
                self.load_problems()
                self.update_history()
                self.update_solution_view()
                
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"\n错误：{str(e)}\n")
            self.result_text.config(state=tk.DISABLED)
        finally:
            self.is_judging = False
            if self.pending_hot_reload:
                self.pending_hot_reload = False
                self.apply_hot_reload()
            else:
                self.hot_reload_status_label.config(text="", fg=self.theme['muted'])
            if temp_file.exists():
                temp_file.unlink()
                
    def clear_code(self):
        """清空代码"""
        if messagebox.askyesno("确认", "确定清空当前代码吗？"):
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
                messagebox.showerror("错误", f"读取文件失败：{e}")
                
    def create_problem(self):
        """创建新题目"""
        dialog = tk.Toplevel(self.root)
        dialog.title("新建题目")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.configure(bg=self.theme['panel'])
        self.apply_theme_recursive(dialog)
        
        tk.Label(dialog, text="年份", font=('Microsoft YaHei', 11)).pack(pady=5)
        year_entry = tk.Entry(dialog, font=('Microsoft YaHei', 11), width=20)
        year_entry.pack()
        year_entry.insert(0, "2025")
        
        tk.Label(dialog, text="题号", font=('Microsoft YaHei', 11)).pack(pady=5)
        num_entry = tk.Entry(dialog, font=('Microsoft YaHei', 11), width=20)
        num_entry.pack()
        num_entry.insert(0, "1")
        
        tk.Label(dialog, text="标题", font=('Microsoft YaHei', 11)).pack(pady=5)
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
                    messagebox.showinfo("成功", "题目已创建。")
                else:
                    messagebox.showwarning("提示", "请输入题目标题。")
            except ValueError:
                messagebox.showerror("错误", "年份和题号必须是整数。")
        
        tk.Button(dialog, text="创建", font=('Microsoft YaHei', 11),
                 bg=self.theme['accent'], fg='white', width=10,
                 command=do_create).pack(pady=15)
        
    def export_report(self):
        """导出进度报告"""
        try:
            self.oj.export_progress()
            messagebox.showinfo("成功", "进度报告已导出到 data/progress_report.md")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")

def main():
    root = tk.Tk()
    app = BUAAOJV4(root)
    root.mainloop()

if __name__ == "__main__":
    main()
