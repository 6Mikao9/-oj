// 测试 Runtime Error - 匹配 2006_1 题目输入格式
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    
    // 读取第一个数组
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    // 读取第二个数组
    cin >> m;
    vector<int> b(m);
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }
    
    // 故意产生运行时错误 - 数组越界
    vector<int> arr(5);
    arr[1000000] = 999;  // Runtime Error!
    
    cout << "equal!" << endl;
    return 0;
}
