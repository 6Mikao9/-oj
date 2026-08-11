#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int N;
    scanf("%d", &N);
    
    int island[100][100];
    int row_left[100], row_right[100];
    int col_top[100], col_bottom[100];
    
    // 初始化
    for (int i = 0; i < N; i++) {
        row_left[i] = -1;
        row_right[i] = -1;
        col_top[i] = -1;
        col_bottom[i] = -1;
    }
    
    // 读入矩阵
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            scanf("%d", &island[i][j]);
        }
    }
    
    // 计算每行最左和最右的1
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (island[i][j] == 1) {
                if (row_left[i] == -1 || j < row_left[i]) {
                    row_left[i] = j;
                }
                if (row_right[i] == -1 || j > row_right[i]) {
                    row_right[i] = j;
                }
            }
        }
    }
    
    // 计算每列最上和最下的1
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            if (island[i][j] == 1) {
                if (col_top[j] == -1 || i < col_top[j]) {
                    col_top[j] = i;
                }
                if (col_bottom[j] == -1 || i > col_bottom[j]) {
                    col_bottom[j] = i;
                }
            }
        }
    }
    
    int area = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (island[i][j] == 0) {
                // 检查是否在行的两个1之间
                if (row_left[i] != -1 && row_right[i] != -1 &&
                    j > row_left[i] && j < row_right[i]) {
                    // 检查是否在列的两个1之间
                    if (col_top[j] != -1 && col_bottom[j] != -1 &&
                        i > col_top[j] && i < col_bottom[j]) {
                        area++;
                    }
                }
            }
        }
    }
    
    printf("%d\n", area);
    return 0;
}
