#include <stdio.h>

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int numerator, denominator;
    if (scanf("%d %d", &numerator, &denominator) != 2) return 1;
    
    int common_divisor = gcd(numerator, denominator);
    
    int reduced_numerator = numerator / common_divisor;
    int reduced_denominator = denominator / common_divisor;
    
    printf("%d %d\n", reduced_numerator, reduced_denominator);
    
    return 0;
}
