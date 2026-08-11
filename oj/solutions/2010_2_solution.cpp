#include <bits/stdc++.h>
using namespace std;

int main() {
    string s1, s2;
    cin >> s1 >> s2;
    
    int i = 0, j = 0;
    string result;
    
    // 对两个字符串自身先去重
    string a, b;
    for (char c : s1) {
        if (a.empty() || c != a.back()) a += c;
    }
    for (char c : s2) {
        if (b.empty() || c != b.back()) b += c;
    }
    
    // 归并
    while (i < a.size() && j < b.size()) {
        if (a[i] < b[j]) {
            if (result.empty() || a[i] != result.back())
                result += a[i];
            i++;
        } else if (a[i] > b[j]) {
            if (result.empty() || b[j] != result.back())
                result += b[j];
            j++;
        } else {
            if (result.empty() || a[i] != result.back())
                result += a[i];
            i++; j++;
        }
    }
    
    while (i < a.size()) {
        if (result.empty() || a[i] != result.back())
            result += a[i];
        i++;
    }
    
    while (j < b.size()) {
        if (result.empty() || b[j] != result.back())
            result += b[j];
        j++;
    }
    
    cout << result << endl;
    
    return 0;
}
