#include <iostream>
#include <string>
#include <unordered_map>
#include <stack>
#include <sstream>
#include <vector>
#include <cctype>
#include <iomanip>

using namespace std;

// 全局变量存储：变量名 -> 变量值
unordered_map<char, double> vars;

// 运算符优先级：*/ > +- > (
int priority(char c) {
    if (c == '+' || c == '-') return 1;
    if (c == '*' || c == '/') return 2;
    return 0;
}

// 辅助函数：弹出两个操作数和一个运算符，计算后压回结果
void calc(stack<double> &nums, stack<char> &ops) {
    double b = nums.top(); nums.pop();
    double a = nums.top(); nums.pop();
    char op = ops.top(); ops.pop();
    switch (op) {
        case '+': nums.push(a + b); break;
        case '-': nums.push(a - b); break;
        case '*': nums.push(a * b); break;
        case '/': nums.push(a / b); break;
    }
}

// 核心函数：表达式求值（支持 +-*/() 和变量）
double evaluate(const string &expr) {
    stack<double> nums; // 操作数栈
    stack<char> ops;    // 运算符栈
    int n = expr.size();
    
    for (int i = 0; i < n; ) {
        if (isdigit(expr[i]) || expr[i] == '.') { // 读取数字
            int j = i;
            while (j < n && (isdigit(expr[j]) || expr[j] == '.')) j++;
            nums.push(stod(expr.substr(i, j - i)));
            i = j;
        } else if (islower(expr[i])) { // 读取变量
            nums.push(vars[expr[i]]);
            i++;
        } else if (expr[i] == '(') { // 左括号直接入栈
            ops.push(expr[i]);
            i++;
        } else if (expr[i] == ')') { // 右括号：计算到左括号
            while (ops.top() != '(') calc(nums, ops);
            ops.pop(); // 弹出左括号
            i++;
        } else { // 运算符：弹出优先级>=当前的，计算后入栈
            while (!ops.empty() && priority(ops.top()) >= priority(expr[i])) {
                calc(nums, ops);
            }
            ops.push(expr[i]);
            i++;
        }
    }
    
    // 处理栈中剩余的运算符
    while (!ops.empty()) calc(nums, ops);
    return nums.top();
}

int main() {
    string line;
    while (getline(cin, line)) {
        if (line == "exit") break;
        
        // 1. 处理 read 语句
        if (line.substr(0, 5) == "read ") {
            stringstream ss(line.substr(5));
            vector<char> var_list;
            char c;
            while (ss >> c) var_list.push_back(c);
            
            // 读入下一行的数字并赋值
            string num_line;
            getline(cin, num_line);
            stringstream num_ss(num_line);
            double num;
            int idx = 0;
            while (num_ss >> num) vars[var_list[idx++]] = num;
        }
        
        // 2. 处理 print 语句
        else if (line.substr(0, 6) == "print ") {
            stringstream ss(line.substr(6));
            vector<char> var_list;
            char c;
            while (ss >> c) var_list.push_back(c);
            
            // 输出变量值，保留两位小数
            cout << fixed << setprecision(2);
            for (int i = 0; i < var_list.size(); i++) {
                if (i > 0) cout << " ";
                cout << vars[var_list[i]];
            }
            cout << endl;
        }
        
        // 3. 处理赋值语句
        else {
            size_t eq_pos = line.find('=');
            char var = line[0];
            string expr = line.substr(eq_pos + 1);
            vars[var] = evaluate(expr);
        }
    }
    return 0;
}