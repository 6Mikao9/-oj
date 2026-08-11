#include <bits/stdc++.h>
using namespace std;

int main() {
    double x;
    int n;
    
    while (cin >> x >> n) {
        double y = x;  // 初始值 y0 = x
        
        for (int i = 0; i < n; i++) {
            y = y * 2.0 / 3.0 + x / (3.0 * y * y);
        }
        
        printf("%.6f\n", y);
    }
    
    return 0;
}
