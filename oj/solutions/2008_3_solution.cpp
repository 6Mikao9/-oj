#include <bits/stdc++.h>
using namespace std;

// 不区分大小写比较字符
bool cmpch(char a, char b) {
    if (a >= 'A' && a <= 'Z') a = a - 'A' + 'a';
    if (b >= 'A' && b <= 'Z') b = b - 'A' + 'a';
    return a == b;
}

// 检查字符c是否在范围[start, end]内（不区分大小写）
bool inRange(char c, char start, char end) {
    if (c >= 'A' && c <= 'Z') c = c - 'A' + 'a';
    if (start >= 'A' && start <= 'Z') start = start - 'A' + 'a';
    if (end >= 'A' && end <= 'Z') end = end - 'A' + 'a';
    return c >= start && c <= end;
}

// 匹配模式串
bool matchPattern(const string& line, const string& pattern, int startPos, int& matchLen) {
    int lineLen = line.length();
    int patLen = pattern.length();
    int i = 0, k = 0;
    
    while (k < patLen && startPos + i < lineLen) {
        if (pattern[k] == '[') {
            // 处理字符范围 [a-c]
            k++;
            char rangeStart = pattern[k];
            k += 2; // 跳过'-' 
            char rangeEnd = pattern[k];
            k += 2; // 跳过']'
            
            if (!inRange(line[startPos + i], rangeStart, rangeEnd)) {
                return false;
            }
            i++;
        } else {
            if (!cmpch(line[startPos + i], pattern[k])) {
                return false;
            }
            i++;
            k++;
        }
    }
    
    if (k == patLen) {
        matchLen = i;
        return true;
    }
    return false;
}

int main() {
    int n;
    cin >> n;
    cin.ignore();
    
    vector<string> lines;
    string line;
    
    for (int i = 0; i < n; i++) {
        getline(cin, line);
        lines.push_back(line);
    }
    
    string pattern;
    getline(cin, pattern);
    
    bool hasMatch = false;
    
    for (int i = 0; i < n; i++) {
        const string& text = lines[i];
        int textLen = text.length();
        int patLen = pattern.length();
        
        // 计算模式串实际长度（不算中括号）
        int actualPatLen = 0;
        for (int k = 0; k < patLen; k++) {
            if (pattern[k] == '[') {
                while (k < patLen && pattern[k] != ']') k++;
            }
            actualPatLen++;
        }
        
        // 遍历所有可能的位置
        for (int start = 0; start <= textLen - actualPatLen + 1; start++) {
            int matchLen;
            if (matchPattern(text, pattern, start, matchLen)) {
                cout << (i + 1) << " " << text.substr(start, matchLen) << endl;
                hasMatch = true;
                break; // 每行只输出第一个匹配
            }
        }
    }
    
    if (!hasMatch) {
        cout << "No match" << endl;
    }
    
    return 0;
}
