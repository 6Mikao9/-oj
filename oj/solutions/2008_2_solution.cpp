#include <bits/stdc++.h>
using namespace std;

int judge(int a[9][9], int b[9][9], int n) {
    int i, j, count;
    
    // 检查0度
    count = 0;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (a[i][j] == b[i][j]) count++;
    if (count == n * n) return 0;
    
    // 检查90度
    count = 0;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (a[i][j] == b[j][n - 1 - i]) count++;
    if (count == n * n) return 90;
    
    // 检查180度
    count = 0;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (a[i][j] == b[n - 1 - i][n - 1 - j]) count++;
    if (count == n * n) return 180;
    
    // 检查270度
    count = 0;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (a[i][j] == b[n - 1 - j][i]) count++;
    if (count == n * n) return 270;
    
    return -1;
}

int main() {
    int n;
    while (scanf("%d", &n) != EOF) {
        int a[9][9], b[9][9];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                scanf("%d", &a[i][j]);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                scanf("%d", &b[i][j]);
        printf("%d\n", judge(a, b, n));
    }
    return 0;
}
