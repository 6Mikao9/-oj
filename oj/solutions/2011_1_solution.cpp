#include <bits/stdc++.h>
using namespace std;

int divisorSum(int x) {
    if (x == 1) return 0;
    int sum = 1;
    for (int i = 2; i * i <= x; i++) {
        if (x % i == 0) {
            sum += i;
            if (i != x / i) sum += x / i;
        }
    }
    return sum;
}

int main() {
    int M, N;
    cin >> M >> N;
    
    bool found = false;
    
    // 预处理所有数的约数和
    vector<int> sumDiv(N + 1);
    for (int i = 1; i <= N; i++) {
        sumDiv[i] = divisorSum(i);
    }
    
    for (int a = M; a <= N; a++) {
        int b = sumDiv[a];
        if (b > a && b <= N && sumDiv[b] == a) {
            cout << a << " " << b << endl;
            found = true;
        }
    }
    
    if (!found) {
        cout << "NONE" << endl;
    }
    
    return 0;
}
