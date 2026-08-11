#include<bits/stdc++.h>
using namespace std;
int c[8], d[100], b[100];
int sum;

void dfs(int l) {  // l是当前行
    for(int i = 0; i < 8; i++) {  // i是列
        // 检查列、左对角线、右对角线
        if(!c[i] && !d[l-i+50] && !b[l+i+50]) {
            c[i] = 1;
            d[l-i+50] = 1;
            b[l+i+50] = 1;
            
            if(l != 7)      // ? 第0-7行，l==7说明8个都放完了
                dfs(l+1);
            else
                sum++;
            
            // 回溯
            c[i] = 0;
            d[l-i+50] = 0;
            b[l+i+50] = 0;
        }
    }
}

int main() {
    dfs(0);
    cout << sum;
    return 0;
}