#include <bits/stdc++.h>
using namespace std;

// 不区分大小写比较字符
bool charEqual(char a, char b) {
    return tolower(a) == tolower(b);
}

// 删除字符串中所有匹配的子串（不区分大小写）
string deletePattern(string line, const string& pattern) {
    if (pattern.empty()) return line;
    
    string result;
    int n = line.length();
    int m = pattern.length();
    
    for (int i = 0; i < n; ) {
        // 尝试匹配
        bool match = true;
        if (i + m <= n) {
            for (int j = 0; j < m; j++) {
                if (!charEqual(line[i + j], pattern[j])) {
                    match = false;
                    break;
                }
            }
        } else {
            match = false;
        }
        
        if (match) {
            // 跳过匹配的子串
            i += m;
        } else {
            // 保留当前字符
            result += line[i];
            i++;
        }
    }
    
    return result;
}

// 将空格移到行首
string moveSpacesToFront(const string& line) {
    int spaceCount = 0;
    string nonSpaces;
    
    for (char c : line) {
        if (c == ' ') {
            spaceCount++;
        } else {
            nonSpaces += c;
        }
    }
    
    return string(spaceCount, ' ') + nonSpaces;
}

int main() {
    int n;
    cin >> n;
    cin.ignore();
    
    vector<string> lines;
    for (int i = 0; i < n; i++) {
        string line;
        getline(cin, line);
        lines.push_back(line);
    }
    
    string pattern;
    getline(cin, pattern);
    
    for (const string& line : lines) {
        string afterDelete = deletePattern(line, pattern);
        string result = moveSpacesToFront(afterDelete);
        cout << result << endl;
    }
    
    return 0;
}
