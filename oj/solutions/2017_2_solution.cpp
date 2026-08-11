#include <bits/stdc++.h>
using namespace std;

set<string> keywords = {"const", "unsigned", "signed", "short", "long", "int", "char", "float", "double", "void"};

int main() {
    string line;
    getline(cin, line);
    
    vector<string> vars;
    int i = 0;
    int n = line.size();
    bool inVarSection = false;  // 是否已进入变量声明区
    
    while (i < n) {
        // 跳过空格
        while (i < n && line[i] == ' ') i++;
        if (i >= n) break;
        
        // 跳过指针符号
        while (i < n && line[i] == '*') i++;
        while (i < n && line[i] == ' ') i++;
        if (i >= n) break;
        
        // 读取一个标识符
        string token;
        while (i < n && (isalnum(line[i]) || line[i] == '_')) {
            token += line[i];
            i++;
        }
        
        if (token.empty()) {
            // 可能是逗号或其他符号
            if (i < n && line[i] == ',') {
                inVarSection = true;  // 逗号后面一定是变量
                i++;
            } else {
                i++;
            }
            continue;
        }
        
        // 判断是类型关键字还是变量名
        if (keywords.find(token) != keywords.end()) {
            // 是类型关键字，继续跳过
        } else {
            // 是变量名
            vars.push_back(token);
            inVarSection = true;
        }
        
        // 跳过数组 [...]
        while (i < n && line[i] == ' ') i++;
        while (i < n && line[i] == '[') {
            int cnt = 1;
            i++;
            while (i < n && cnt > 0) {
                if (line[i] == '[') cnt++;
                else if (line[i] == ']') cnt--;
                i++;
            }
            while (i < n && line[i] == ' ') i++;
        }
        
        // 跳过逗号
        if (i < n && line[i] == ',') {
            i++;
        }
    }
    
    for (string& v : vars) {
        cout << v << endl;
    }
    
    return 0;
}
