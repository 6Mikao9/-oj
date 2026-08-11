#include <bits/stdc++.h>
using namespace std;

struct Element {
    int value;
    int index;
};

bool compare(const Element& a, const Element& b) {
    return a.value < b.value;
}

int main() {
    int n;
    cin >> n;
    
    vector<Element> arr(n);
    vector<int> result(n);
    
    // 读取输入并保存原始索引
    for (int i = 0; i < n; i++) {
        cin >> arr[i].value;
        arr[i].index = i;
    }
    
    // 排序
    sort(arr.begin(), arr.end(), compare);
    
    // 计算每个元素的次序（考虑重复元素，使用dense rank）
    int rank = 1;
    for (int i = 0; i < n; i++) {
        if (i > 0 && arr[i].value != arr[i-1].value) {
            rank++;
        }
        result[arr[i].index] = rank;
    }
    
    // 输出结果
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << " ";
        cout << result[i];
    }
    cout << endl;
    
    return 0;
}
