from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
problems_root = root / "oj" / "problems"
years_root = root / "oj" / "data" / "years" / "2026"
years_root.mkdir(parents=True, exist_ok=True)

items = [
    {
        "id": "2026_2",
        "title": "窗口点击叠放模拟",
        "summary": "模拟桌面窗口被点击后的层级变化，输出最终窗口顺序。",
        "md": """# 2026_2: 窗口点击叠放模拟

## 问题描述
有 n 个窗口，输入顺序表示从上到下的初始叠放顺序（先输入的在更上层）。
每次鼠标点击会命中最上层且包含点击点的窗口，该窗口会被提升到最上层。
请输出所有点击结束后的窗口叠放顺序（从上到下）。

## 输入格式
- 第一行：整数 n（1 <= n <= 100）
- 接下来 n 行：`id x1 y1 x2 y2`，表示窗口编号与矩形区域
- 下一行：整数 m（1 <= m <= 1000）
- 接下来 m 行：`x y` 表示点击坐标

说明：边界也算命中。

## 输出格式
一行，按从上到下输出窗口 id，空格分隔。

## 样例输入
```text
3
1 0 0 4 4
2 2 0 6 4
3 5 0 8 4
3
3 2
6 2
1 1
```

## 样例输出
```text
1 3 2
```
"""
    },
    {
        "id": "2026_3",
        "title": "C声明中的变量名提取",
        "summary": "从一行 C 风格变量声明中提取所有变量名，忽略类型和指针/数组修饰。",
        "md": """# 2026_3: C声明中的变量名提取

## 问题描述
给定一行合法的 C 风格变量声明语句（不含分号）。
声明中可能包含 `const`、`unsigned`、`long` 等类型修饰，
也可能有 `*` 和数组下标 `[]`。
请按声明中出现顺序输出所有变量名。

## 输入格式
一行字符串，长度不超过 300。

## 输出格式
每行输出一个变量名。

## 样例输入
```text
const unsigned long int *ptr, arr[10], var_name, **double_ptr
```

## 样例输出
```text
ptr
arr
var_name
double_ptr
```
"""
    },
    {
        "id": "2026_4",
        "title": "三叉树稳定节点",
        "summary": "在三叉树中按孩子数、深度、前序顺序三重规则选出最优节点。",
        "md": """# 2026_4: 三叉树稳定节点

## 问题描述
给定一棵三叉树的父节点输入，要求找出“最稳定”节点。
稳定性规则：
1. 直接孩子数量越多越优先；
2. 若孩子数量相同，深度更大者优先；
3. 若仍相同，按前序遍历先访问者优先。

输出该节点编号和其前序序号（从 1 开始）。

## 输入格式
- 第一行：整数 n（作为父节点出现的节点数）
- 接下来 n 行：`id left mid right`，孩子为 0 表示空

## 输出格式
一行两个整数：`node_id preorder_index`

## 样例输入
```text
4
100 101 102 103
101 1 0 2
102 3 4 5
1 0 0 0
```

## 样例输出
```text
102 5
```
"""
    },
    {
        "id": "2026_5",
        "title": "网络交换机故障扩散",
        "summary": "在树形网络中定位故障交换机，输出受影响设备的先序序列。",
        "md": """# 2026_5: 网络交换机故障扩散

## 问题描述
网络拓扑是一棵树，节点分为交换机和终端设备。
当某交换机故障时，其子树中的所有节点都受影响。
请输出受影响节点编号，按先序遍历顺序。

## 输入格式
- 第一行：整数 n（节点关系条数）
- 接下来 n 行：`parent child`
- 下一行：故障交换机编号 x

保证输入构成一棵树，根节点在关系中只做 parent。

## 输出格式
一行或多行，按先序遍历输出受影响节点编号，空格分隔。

## 样例输入
```text
7
10 11
10 12
11 21
11 22
12 31
12 32
22 221
11
```

## 样例输出
```text
11 21 22 221
```
"""
    },
    {
        "id": "2026_6",
        "title": "素数等差序列筛选",
        "summary": "在区间内找出长度至少为 3 的极大素数等差序列。",
        "md": """# 2026_6: 素数等差序列筛选

## 问题描述
给定区间 [a,b]，请找出所有由素数组成且长度不少于 3 的等差序列。
每个序列要求是“极大”的：不能在两端继续按同公差扩展。

## 输入格式
一行两个整数 a,b（1 <= a < b <= 1000000）。

## 输出格式
每行输出一个序列，数字间空格分隔。
若不存在，输出 `None`。

## 样例输入
```text
1 100
```

## 样例输出
```text
3 5 7
47 53 59
```
"""
    },
    {
        "id": "2026_7",
        "title": "文本关键词删除与空格前移",
        "summary": "不区分大小写删除子串，并将剩余空格全部移动到行首。",
        "md": """# 2026_7: 文本关键词删除与空格前移

## 问题描述
给定 n 行文本和一个待删除字符串 key。
对每一行执行：
1. 删除所有与 key 大小写无关匹配的子串；
2. 将该行剩余的空格字符全部移动到行首，其他字符相对顺序不变。

## 输入格式
- 第一行：整数 n
- 接下来 n 行：文本
- 最后一行：key

## 输出格式
输出 n 行处理后的文本。

## 样例输入
```text
3
#include <stdio.h>
int main()
printf("Hi ")
In
```

## 样例输出
```text
#clude <stdio.h>
 tma()
printf("Hi ")
```
"""
    },
    {
        "id": "2026_8",
        "title": "学生运动记录汇总",
        "summary": "按学号聚合运动时长与项目集合，并按总时长排序输出。",
        "md": """# 2026_8: 学生运动记录汇总

## 问题描述
每条记录包含：学号、运动项目、开始时间、结束时间（HHMMSS）。
请按学号汇总每位学生的：
- 总运动时长（小时，保留 2 位小数）
- 参与项目集合（按字典序，逗号分隔）

输出按总时长降序，若相同按学号升序。

## 输入格式
- 第一行：整数 n
- 接下来 n 行：`stu_id sport start end`

## 输出格式
每行：`stu_id total_hours sports`

## 样例输入
```text
4
1001 run 083000 093000
1002 swim 090000 100000
1001 bike 101500 111500
1002 run 101000 103000
```

## 样例输出
```text
1001 2.00 bike,run
1002 1.50 run,swim
```
"""
    },
    {
        "id": "2026_9",
        "title": "简易脚本解释器",
        "summary": "实现 read/assign/print/exit 指令解释执行，支持括号与四则运算。",
        "md": """# 2026_9: 简易脚本解释器

## 问题描述
实现一个简化解释器，支持四类语句：
- `read a b c`：下一行读取对应整数
- `x=expr`：表达式赋值，支持 `+ - * / ()`
- `print a b c`：输出变量值，保留 2 位小数
- `exit`：结束

变量名均为单个小写字母，输入保证语法合法。

## 输入格式
多行脚本，直到 `exit`。

## 输出格式
每遇到一条 `print`，输出一行对应值。

## 样例输入
```text
read a b
10 20
c=(a+b)/4
print a b c
exit
```

## 样例输出
```text
10.00 20.00 7.50
```
"""
    },
    {
        "id": "2026_10",
        "title": "基站重叠用户统计",
        "summary": "按目标用户和基站统计时间重叠的其他用户列表。",
        "md": """# 2026_10: 基站重叠用户统计

## 问题描述
每条日志形如：`user station start end`。
给定目标用户 u，找出与 u 在同一基站且时间区间有重叠的所有其他用户。
同一用户只输出一次，按用户编号升序。

区间重叠定义：`max(l1,l2) <= min(r1,r2)`。

## 输入格式
- 第一行：整数 n
- 接下来 n 行：`user station start end`（时间为 HHMM）
- 最后一行：目标用户 u

## 输出格式
若存在重叠用户，按升序每行输出一个用户编号；否则输出 `None`。

## 样例输入
```text
5
101 A 0830 0930
102 A 0900 1000
103 B 0900 1100
104 A 0700 0800
105 A 0930 1000
101
```

## 样例输出
```text
102
105
```
"""
    },
    {
        "id": "2026_11",
        "title": "最优中继基站",
        "summary": "在带权无向图中找距离和最小的节点，平局取编号最小。",
        "md": """# 2026_11: 最优中继基站

## 问题描述
给定 n 个基站和 m 条双向链路，每条链路有延迟权值。
选择一个中继基站 k，使得它到所有基站的最短路距离和最小。
若有多个最优解，输出编号最小者。

## 输入格式
- 第一行：n m
- 接下来 m 行：u v w（1 <= u,v <= n, w > 0）

保证图连通。

## 输出格式
输出两个整数：`k total_distance`

## 样例输入
```text
4 4
1 2 1
2 3 1
3 4 1
1 4 10
```

## 样例输出
```text
2 4
```
"""
    },
]

for item in items:
    pid = item["id"]
    pdir = problems_root / pid
    tdir = pdir / "testcases"
    pdir.mkdir(parents=True, exist_ok=True)
    tdir.mkdir(parents=True, exist_ok=True)

    (pdir / "problem.md").write_text(item["md"], encoding="utf-8")

    info = {
        "id": pid,
        "title": item["title"],
        "description": f"## 问题描述\n{item['summary']}\n\n## 输入格式\n见题面。\n\n## 输出格式\n见题面。",
        "time_limit": 1000,
        "memory_limit": 65536,
        "test_cases": []
    }
    (pdir / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    year = {
        "id": pid,
        "year": 2026,
        "title": item["title"],
        "description": info["description"],
        "status": "未解决",
        "submissions": [],
        "solution_file": f"oj/solutions/{pid}_solution.cpp",
        "notes": "",
        "tags": ["2026模拟"],
        "is_favorite": False,
        "annotation": ""
    }
    (years_root / f"{pid}.json").write_text(json.dumps(year, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"Generated {len(items)} mock problems for 2026.")
