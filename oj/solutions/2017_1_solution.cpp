#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<double> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    sort(a.begin(), a.end());
    
    double median;
    if (n % 2 == 1) {
        median = a[n / 2];
    } else {
        median = (a[n / 2 - 1] + a[n / 2]) / 2.0;
    }
    
    cout << fixed << setprecision(6) << median << endl;
    return 0;
}
