#include<bits/stdc++.h>
using namespace std;

bool sameType(char a, char b) 
{
    bool aLower = islower(a), bLower = islower
(b);
    bool aUpper = isupper(a), bUpper = isupper(b);  // 修复：isupper(a)
    bool aDigit = isdigit(a), bDigit = isdigit
(b);
    return
 (aLower && bLower) || (aUpper && bUpper) || (aDigit && bDigit);
}


int main(){
    string s;
    cin >> s;
    
    string result;
    for(int i = 0; i < s.size(); i++) {
        if(s[i] == '-' && i > 0 && i < s.size()-1) {
            char left = s[i-1];
            char right = s[i+1];
            
            // 检查是否同类型且可以扩展
            if(sameType(left, right) && left < right) {
                // 扩展：添加 left+1 到 right 的所有字符
                for(char c = left + 1; c < right; c++) {
                    result += c;
                }
            } else {
                // 不同类型或逆序，保留'-'
                result += '-';
            }
        } else {
            result += s[i];
        }
    }
    
    cout << result << endl;
}