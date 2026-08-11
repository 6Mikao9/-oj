#include <stdio.h>
#include <stdlib.h>

int fun(int n) {
    if (n == 0 || n == 1)
        return 1;
    else
        return n * fun(n - 1);
}

int main() {
    int a[10], n, i = 0, j = 0;
    int sum = 0;
    
    if (scanf("%d", &n) != 1 || n < 0) {
        return EXIT_FAILURE;
    }
    
    int m = n;
    printf("%d,", m);
    
    if (n == 0) {
        a[i] = 0;
        i++;
    }
    
    while (n != 0) {
        a[i] = n % 10;
        n = n / 10;
        i++;
    }
    
    for (j = i - 1; j >= 0; j--) {
        printf("%d!", a[j]);
        sum = sum + fun(a[j]);
        if (j != 0) {
            printf("+");
        }
    }
    
    printf("=%d\n", sum);
    
    if (sum == m) {
        printf("Yes\n");
    } else {
        printf("No\n");
    }
    
    return 0;
}
