#include <bits/stdc++.h>
using namespace std;

int main() {
    long double x, epsilon;
    cin >> x >> epsilon;
    
    long double sum = 0.0;
    long double term = 1.0;  // T_0 = 1
    int n = 0;
    
    while (fabsl(term) >= epsilon) {
        sum += term;
        long double divisor = (2.0L * n + 2.0L) * (2.0L * n + 1.0L);
        long double x_squared = x * x;
        term = -term * x_squared / divisor;
        n++;
    }
    
    cout << fixed << setprecision(10) << (double)sum << endl;
    
    return 0;
}
