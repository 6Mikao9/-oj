# OJ 题目管理系统使用指南

## 目录结构

```
oj/
├── problems/           # 题目目录
│   ├── 2015_1/        # 年份_题号
│   │   ├── problem.md # 题目描述
│   │   └── testcases/ # 测试数据
│   │       ├── 1.in   # 测试点1输入
│   │       ├── 1.out  # 测试点1输出
│   │       ├── 2.in
│   │       └── 2.out
│   └── ...
├── solutions/          # 标准答案
│   ├── 2015_1_solution.cpp
│   └── ...
└── README.md          # 本文件
```

## 添加新题目的步骤

### 1. 创建目录结构

```bash
mkdir -p problems/年份_题号/testcases
```

例如：`problems/2020_1/testcases`

### 2. 编写题目描述 (problem.md)

必须包含以下部分：

```markdown
# 年份_题号: 题目名称

## 问题描述
清晰描述题目要求

## 输入格式
- 第一行：...
- 第二行：...

## 输出格式
说明输出要求

## 样例输入
```
输入数据
```

## 样例输出
```
输出数据
```

## 提示/说明
- 数据范围
- 特殊说明
- 注意事项
```

### 3. 准备测试数据

**文件命名规范：**
- 输入文件：`1.in`, `2.in`, `3.in` ...
- 输出文件：`1.out`, `2.out`, `3.out` ...
- **必须成对出现**

**测试数据要求：**
1. **至少3组测试点**
2. 必须包含：
   - 最小边界情况
   - 一般情况
   - 最大边界/复杂情况
3. 每行末尾必须有换行符（特别是最后一行）
4. **不要使用中文编码**（Windows下UTF-8可能导致字符串匹配失败）

**文件编码：**
- 使用ASCII或GBK编码
- 避免UTF-8中文（如需中文请使用英文替代）

### 4. 编写标准答案 (solutions/年份_题号_solution.cpp)

**代码规范：**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    // 读取输入
    // 处理逻辑
    // 输出结果
    return 0;
}
```

**注意事项：**
1. 使用标准C++库，避免平台特定代码
2. 输出格式必须与 `.out` 文件完全一致
3. 浮点数输出使用 `fixed << setprecision(6)`
4. 每行输出后必须加 `endl` 或 `\n`

### 5. 验证测试

编译并测试标准答案：

```bash
g++ solutions/2020_1_solution.cpp -o test
cat problems/2020_1/testcases/1.in | ./test
cat problems/2020_1/testcases/1.out  # 对比输出
```

## 常见问题与解决方案

### Q1: 输出格式不一致

**现象**：答案正确但被判错误

**原因**：
- 行末缺少换行符
- 空格数量不一致
- 浮点数精度问题

**解决**：
```cpp
// 正确
printf("%.6f\n", ans);  // C风格
// 或
cout << fixed << setprecision(6) << ans << endl;  // C++风格
```

### Q2: 字符串匹配失败

**现象**：中文输入输出匹配失败

**原因**：Windows下UTF-8编码导致中文字符解析错误

**解决**：测试数据使用英文，如用 `ZhangSan` 替代 `张三`

### Q3: 无限递归或TLE

**现象**：程序运行超时或栈溢出

**常见原因**：
- map访问自动创建空键：`if (m.count(key))` 而非 `if (m[key])`
- 忘记标记访问状态导致循环
- 算法复杂度不够

**解决**：
```cpp
// 错误
count = depth[node];  // 会创建空节点

// 正确
if (depth.find(node) != depth.end()) 
    count = depth[node];
```

### Q4: 多测试点覆盖不足

**必须测试的边界情况**：
- n = 0 或 n = 1
- 空输入/空树
- 全相同数据
- 最大值/最小值

## 标准答案模板

### 基础模板

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    
    // 处理逻辑
    
    cout << ans << endl;
    return 0;
}
```

### 图论/树问题模板

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int id;
    vector<int> children;
    int parent = -1;
};

map<int, Node> tree;

void buildTree(int n) {
    // 建树逻辑
}

int main() {
    int n;
    cin >> n;
    buildTree(n);
    // ...
    return 0;
}
```

### 字符串处理模板

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<string> split(const string& s, char delim) {
    vector<string> tokens;
    string token;
    istringstream iss(s);
    while (getline(iss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}

int main() {
    string line;
    getline(cin, line);
    auto tokens = split(line, ' ');
    // ...
    return 0;
}
```

## 题目难度分级

| 星级 | 难度 | 描述 |
|------|------|------|
| ⭐ | 简单 | 基础语法，单循环/条件 |
| ⭐⭐ | 中等 | 排序，查找，简单模拟 |
| ⭐⭐⭐ | 较难 | 树/图遍历，动态规划 |
| ⭐⭐⭐⭐ | 困难 | 复杂数据结构，优化算法 |
| ⭐⭐⭐⭐⭐ | 极难 | 综合应用，高级算法 |

## 提交检查清单

添加题目后，必须完成以下检查：

- [ ] problem.md 包含所有必要部分
- [ ] 至少3组测试数据
- [ ] 标准答案能通过所有测试点
- [ ] 输出格式与 .out 文件完全一致
- [ ] 代码无平台特定依赖
- [ ] 已测试边界情况

## 示例：完整添加一道题

```bash
# 1. 创建目录
mkdir -p problems/2020_1/testcases

# 2. 编写题目描述
cat > problems/2020_1/problem.md << 'EOF'
# 2020_1: 示例题目

## 问题描述
求两个数的和

## 输入格式
两个整数a和b

## 输出格式
一个整数，表示a+b

## 样例输入
```
3 5
```

## 样例输出
```
8
```
EOF

# 3. 准备测试数据
echo "3 5" > problems/2020_1/testcases/1.in
echo "8" > problems/2020_1/testcases/1.out
echo "0 0" > problems/2020_1/testcases/2.in
echo "0" > problems/2020_1/testcases/2.out

# 4. 编写标准答案
cat > solutions/2020_1_solution.cpp << 'EOF'
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
EOF

# 5. 测试
g++ solutions/2020_1_solution.cpp -o test
for i in 1 2; do
    echo "Test $i:"
    cat problems/2020_1/testcases/$i.in | ./test
    echo "Expected:"
    cat problems/2020_1/testcases/$i.out
done
```

---

**维护者**：OJ系统管理团队  
**最后更新**：2026年2月13日
