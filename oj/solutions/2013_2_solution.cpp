#include <stdio.h>
#include <stdlib.h>

int count = 0;
int column[9]; // column[row] = col，记录第row行皇后所在的列

int is_safe(int row, int col) {
    for (int prev_row = 1; prev_row < row; prev_row++) {
        int prev_col = column[prev_row];
        // 同一列
        if (prev_col == col) return 0;
        // 同一对角线（主对角线或副对角线）
        if (abs(prev_row - row) == abs(prev_col - col)) return 0;
    }
    return 1;
}

void solve(int row) {
    if (row > 8) {
        count++;
        return;
    }
    
    for (int col = 1; col <= 8; col++) {
        if (is_safe(row, col)) {
            column[row] = col;
            solve(row + 1);
        }
    }
}

int main() {
    solve(1);
    printf("%d\n", count);
    return 0;
}
