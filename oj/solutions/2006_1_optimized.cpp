// 2006_1 优化解法 - 更简洁高效
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m, x;
    
    // 读取第一个集合
    cin >> n;
    set<int> setA;  // 使用 set 自动排序去重
    for (int i = 0; i < n; i++) {
        cin >> x;
        setA.insert(x);
    }
    
    // 读取第二个集合
    cin >> m;
    set<int> setB;
    for (int i = 0; i < m; i++) {
        cin >> x;
        setB.insert(x);
    }
    
    // 直接比较两个 set（自动处理大小和元素比较）
    if (setA == setB) {
        cout << "equal!" << endl;
    } else {
        cout << "not equal!" << endl;
    }
    
    return 0;
}
