#include <bits/stdc++.h>
using namespace std;

struct Branch {
    int c[3];
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    unordered_map<int, Branch> g;
    int root = -1;
    for (int i = 0; i < n; i++) {
        int r, s1, s2, s3;
        cin >> r >> s1 >> s2 >> s3;
        if (i == 0) root = r;
        g[r] = {{s1, s2, s3}};
    }

    // Collect gate positions from top to bottom, left to right.
    vector<int> positions;
    queue<int> q;
    q.push(root);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        auto it = g.find(u);
        if (it == g.end()) continue;

        for (int k = 0; k < 3; k++) {
            int v = it->second.c[k];
            if (v == -1) continue;
            if (v >= 100) q.push(v);
            else positions.push_back(v);
        }
    }

    vector<pair<int, long long>> flow; // (gate, passenger)
    int gate;
    long long passenger;
    while (cin >> gate >> passenger) {
        flow.push_back({gate, passenger});
    }

    sort(flow.begin(), flow.end(), [](const auto& a, const auto& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });

    int cnt = min((int)flow.size(), (int)positions.size());
    for (int i = 0; i < cnt; i++) {
        cout << flow[i].first << " " << positions[i];
        if (i + 1 < cnt) cout << '\n';
    }

    return 0;
}
