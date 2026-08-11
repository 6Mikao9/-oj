#include <bits/stdc++.h>
using namespace std;

const int MAX_B = 40000;
int isPrime[MAX_B + 1];

void sieve(int b) {
    memset(isPrime, 1, sizeof(isPrime));
    isPrime[0] = isPrime[1] = 0;
    
    for (int p = 2; p * p <= b; p++) {
        if (isPrime[p]) {
            for (int i = p * p; i <= b; i += p) {
                isPrime[i] = 0;
            }
        }
    }
}

int main() {
    int a, b;
    cin >> a >> b;
    
    if (b > MAX_B) b = MAX_B;
    
    sieve(b);
    
    vector<int> primes;
    for (int i = a; i <= b; i++) {
        if (isPrime[i]) {
            primes.push_back(i);
        }
    }

    int n = (int)primes.size();
    if (n < 3) return 0;

    // 题目测试数据要求：输出“连续素数序列”里公差相同且长度>=3的极大段。
    vector<int> diff(n - 1);
    for (int i = 0; i + 1 < n; i++) diff[i] = primes[i + 1] - primes[i];

    for (int i = 0; i + 1 < (int)diff.size(); ) {
        int j = i;
        while (j + 1 < (int)diff.size() && diff[j + 1] == diff[i]) j++;

        int run_len = j - i + 1;           // number of equal diffs
        int prime_count = run_len + 1;     // number of primes in this run
        if (prime_count >= 3) {
            for (int k = i; k <= j + 1; k++) {
                if (k > i) cout << " ";
                cout << primes[k];
            }
            cout << '\n';
        }
        i = j + 1;
    }

    return 0;
}
