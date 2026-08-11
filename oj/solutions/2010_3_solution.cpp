#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n;
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    cin >> m;
    vector<int> b(m);
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }
    
    // 长度不同直接不等
    if (n != m) {
        cout << "not equal!" << endl;
        return 0;
    }
    
    // 统计频次
    map<int, int> cnt1, cnt2;
    for (int x : a) cnt1[x]++;
    for (int x : b) cnt2[x]++;
    
    // 比较频次
    if (cnt1 == cnt2) {
        cout << "equal!" << endl;
    } else {
        cout << "not equal!" << endl;
    }
    
    return 0;
}
