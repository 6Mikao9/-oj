#include <bits/stdc++.h>
using namespace std;

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    int limit = sqrt(n);
    for (int i = 3; i <= limit; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

int main() {
    int n;
    scanf("%d", &n);
    
    bool found = false;
    bool first = true;
    
    for (int i = 11; i <= n; i++) {
        if (i % 10 == 1 && isPrime(i)) {
            if (!first) printf(" ");
            printf("%d", i);
            found = true;
            first = false;
        }
    }
    
    if (!found) {
        printf("-1");
    }
    printf("\n");
    
    return 0;
}
