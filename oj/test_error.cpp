// 这是一个有错误的测试代码
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    // 故意数组越界，产生运行时错误
    vector<int> arr(5);
    arr[1000000] = 999;  // Runtime Error! 数组越界
    
    cout << "test" << endl;
    return 0;
}
