#include<bits/stdc++.h>
using namespace std;

int main(){
    double x, eps;
    cin >> x >> eps;
    
    double sum = 0.0;
    double term = 1.0;
    int n = 0;
    
    while(fabs(term) >= eps) {
        sum += term;
        double divisor = (2.0 * n + 2.0) * (2.0 * n + 1.0);
        term = -term * x * x / divisor;
        n++;
    }
    
    cout << fixed << setprecision(10) << sum << endl;
}