#include <bits/stdc++.h>
using namespace std;

struct Block {
    long long start;
    long long len;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<Block> free_list(n);
    for (int i = 0; i < n; i++) {
        cin >> free_list[i].start >> free_list[i].len;
    }

    int cur = 0; // starts at the smallest-address block

    while (true) {
        long long req;
        cin >> req;
        if (!cin || req == -1) break;
        if (free_list.empty()) continue;

        int m = (int)free_list.size();
        int best = -1;
        long long best_len = (1LL << 62);

        for (int step = 0; step < m; step++) {
            int idx = (cur + step) % m;
            if (free_list[idx].len >= req) {
                if (free_list[idx].len < best_len) {
                    best_len = free_list[idx].len;
                    best = idx;
                }
            }
        }

        if (best == -1) {
            // request failed, current unchanged
            continue;
        }

        if (free_list[best].len == req) {
            // remove block, current moves to next block of removed node
            free_list.erase(free_list.begin() + best);
            if (!free_list.empty()) {
                cur = best % (int)free_list.size();
            }
        } else {
            // split block, current remains on this block
            free_list[best].len -= req;
            cur = best;
        }
    }

    if (free_list.empty()) return 0;

    for (int i = 0; i < (int)free_list.size(); i++) {
        int idx = (cur + i) % (int)free_list.size();
        cout << free_list[idx].start << " " << free_list[idx].len;
        if (i + 1 < (int)free_list.size()) cout << '\n';
    }

    return 0;
}
