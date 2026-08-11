// USACO 2.4 两只塔姆沃斯牛 - 正确解答
#include <bits/stdc++.h>
using namespace std;

char grid[10][10];
int fx, fy, cx, cy;  // FJ 和牛的位置
int dirf = 0, dirc = 0;  // 方向: 0=北, 1=东, 2=南, 3=西

// 方向数组: 北、东、南、西
dr[] = {-1, 0, 1, 0};
dc[] = {0, 1, 0, -1};

bool canMove(int r, int c) {
    return r >= 0 && r < 10 && c >= 0 && c < 10 && grid[r][c] != '*';
}

void move(int &r, int &c, int &dir) {
    int nr = r + dr[dir];
    int nc = c + dc[dir];
    if (canMove(nr, nc)) {
        r = nr;
        c = nc;
    } else {
        dir = (dir + 1) % 4;  // 顺时针转90度
    }
}

int main() {
    // 读取输入
    for (int i = 0; i < 10; i++) {
        string line;
        getline(cin, line);
        for (int j = 0; j < 10; j++) {
            grid[i][j] = line[j];
            if (grid[i][j] == 'F') {
                fx = i; fy = j;
                grid[i][j] = '.';
            } else if (grid[i][j] == 'C') {
                cx = i; cy = j;
                grid[i][j] = '.';
            }
        }
    }
    
    // 模拟
    for (int t = 1; t <= 1000000; t++) {
        move(fx, fy, dirf);
        move(cx, cy, dirc);
        
        if (fx == cx && fy == cy) {
            cout << t << endl;
            return 0;
        }
    }
    
    cout << 0 << endl;
    return 0;
}
