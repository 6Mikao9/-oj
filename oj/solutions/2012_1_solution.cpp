#include <stdio.h>
#include <math.h>

int main() {
    int n;
    scanf("%d", &n);
    
    int found = 0;
    
    // k表示分解的项数，至少2个数
    // 由于k从大到小枚举时，起始整数a是从小到大的
    // 所以直接输出就满足"按最小整数从小到大"的要求
    for (int k = (int)(sqrt(2*n)); k >= 2; k--) {
        // 2n必须能被k整除
        if ((2 * n) % k != 0) continue;
        
        int temp = (2 * n) / k - k + 1;
        
        if (temp % 2 != 0) continue;
        
        int a = temp / 2; // 起始整数
        if (a > 0) {
            found = 1;
            for (int i = a; i < a + k; i++) {
                printf("%d ", i);
            }
            printf("\n");
        }
    }
    
    if (!found) {
        printf("NONE\n");
    }
    
    return 0;
}
