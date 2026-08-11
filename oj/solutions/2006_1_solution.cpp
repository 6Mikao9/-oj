// 2006年第1题：判断数组元素是否相同
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    
    // 读取数组a
    cin >> n;
    set<int> setA;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        setA.insert(x);
    }
    
    // 读取数组b
    cin >> m;
    set<int> setB;
    for (int i = 0; i < m; i++) {
        int x;
        cin >> x;
        setB.insert(x);
    }
    
    // 比较两个集合
    if (setA == setB) {
        cout << "equal!" << endl;
    } else {
        cout << "not equal!" << endl;
    }
    
    return 0;
}
