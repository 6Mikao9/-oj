#include <stdio.h>

int getSumOfDivisors(int n, int divisors[]) {
    int sum = 0;
    int count = 0;
    for (int i = 1; i <= n / 2; i++) {
        if (n % i == 0) {
            divisors[count] = i;
            sum += i;
            count++;
        }
    }
    divisors[count] = -1;
    return sum;
}

void printDivisors(int n, int divisors[]) {
    printf("%d,", n);
    for (int i = 0; divisors[i] != -1; i++) {
        if (divisors[i + 1] == -1) {
            printf("%d", divisors[i]);
        } else {
            printf("%d+", divisors[i]);
        }
    }
}

int main() {
    int n, m;
    int a[100], b[100];
    int suma, sumb;
    
    scanf("%d,%d", &n, &m);
    
    suma = getSumOfDivisors(n, a);
    sumb = getSumOfDivisors(m, b);
    
    printDivisors(n, a);
    printf("=%d\n", suma);
    
    printDivisors(m, b);
    printf("=%d\n", sumb);
    
    if (suma == m && sumb == n && n != m) {
        printf("1\n");
    } else {
        printf("0\n");
    }
    
    return 0;
}
