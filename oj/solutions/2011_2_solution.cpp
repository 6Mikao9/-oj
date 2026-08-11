#include <bits/stdc++.h>
using namespace std;

int main() {
    int r1, c1;
    cin >> r1 >> c1;
    
    vector<vector<int>> A(r1, vector<int>(c1));
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c1; j++) {
            cin >> A[i][j];
        }
    }
    
    int r2, c2;
    cin >> r2 >> c2;
    
    vector<vector<int>> B(r2, vector<int>(c2));
    for (int i = 0; i < r2; i++) {
        for (int j = 0; j < c2; j++) {
            cin >> B[i][j];
        }
    }
    
    int x, y;
    cin >> x >> y;
    
    // 转换为0-based索引
    int startX = x - 1;
    int startY = y - 1;
    
    // 替换
    for (int i = 0; i < r2 && startX + i < r1; i++) {
        for (int j = 0; j < c2 && startY + j < c1; j++) {
            A[startX + i][startY + j] = B[i][j];
        }
    }
    
    // 输出
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c1; j++) {
            if (j > 0) cout << " ";
            cout << A[i][j];
        }
        cout << endl;
    }
    
    return 0;
}
