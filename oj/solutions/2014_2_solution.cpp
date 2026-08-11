#include <stdio.h>
#include <stdlib.h>

#define SIZE 19

int main() {
    int a[SIZE][SIZE];
    int i, j, k;
    int found = 0;
    int winner = 0;
    int winX = 0, winY = 0;
    
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            if (scanf("%d", &a[i][j]) != 1) return EXIT_FAILURE;
        }
    }
    
    // 检查横向（从左到右）
    for (i = 0; i < SIZE && !found; i++) {
        for (j = 0; j <= SIZE - 5 && !found; j++) {
            int val = a[i][j];
            if (val == 0) continue;
            int count = 1;
            for (k = 1; k < 5; k++) {
                if (a[i][j + k] == val) count++;
                else break;
            }
            if (count == 5) {
                found = 1;
                winner = val;
                winX = i + 1;
                winY = j + 1;
            }
        }
    }
    
    // 检查纵向（从上到下）
    for (i = 0; i <= SIZE - 5 && !found; i++) {
        for (j = 0; j < SIZE && !found; j++) {
            int val = a[i][j];
            if (val == 0) continue;
            int count = 1;
            for (k = 1; k < 5; k++) {
                if (a[i + k][j] == val) count++;
                else break;
            }
            if (count == 5) {
                found = 1;
                winner = val;
                winX = i + 1;
                winY = j + 1;
            }
        }
    }
    
    // 检查主对角线（左上到右下）
    for (i = 0; i <= SIZE - 5 && !found; i++) {
        for (j = 0; j <= SIZE - 5 && !found; j++) {
            int val = a[i][j];
            if (val == 0) continue;
            int count = 1;
            for (k = 1; k < 5; k++) {
                if (a[i + k][j + k] == val) count++;
                else break;
            }
            if (count == 5) {
                found = 1;
                winner = val;
                winX = i + 1;
                winY = j + 1;
            }
        }
    }
    
    // 检查副对角线（右上到左下）
    for (i = 0; i <= SIZE - 5 && !found; i++) {
        for (j = 4; j < SIZE && !found; j++) {
            int val = a[i][j];
            if (val == 0) continue;
            int count = 1;
            for (k = 1; k < 5; k++) {
                if (a[i + k][j - k] == val) count++;
                else break;
            }
            if (count == 5) {
                found = 1;
                winner = val;
                winX = i + 1;
                winY = j + 1;
            }
        }
    }
    
    if (found) {
        printf("%d:(%d,%d)\n", winner, winX, winY);
    } else {
        printf("no\n");
    }
    
    return 0;
}
