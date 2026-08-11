#include <bits/stdc++.h>
using namespace std;

int getType(char ch) {
    if (ch >= 'a' && ch <= 'z') return 0;  // 小写字母
    if (ch >= '0' && ch <= '9') return 1;  // 数字
    if (ch >= 'A' && ch <= 'Z') return 2;  // 大写字母
    return -1;  // 其他
}

int main() {
    string s;
    cin >> s;
    
    string result;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == '-' && i > 0 && i < s.length() - 1) {
            char left = s[i - 1];
            char right = s[i + 1];
            int typeLeft = getType(left);
            int typeRight = getType(right);
            
            // 检查是否可以扩展
            if (typeLeft != -1 && typeLeft == typeRight && left < right) {
                // 扩展为中间字符
                for (char c = left + 1; c < right; c++) {
                    result += c;
                }
            } else {
                result += s[i];  // 不能扩展，保留'-'
            }
        } else {
            result += s[i];
        }
    }
    
    cout << result << endl;
    
    return 0;
}
