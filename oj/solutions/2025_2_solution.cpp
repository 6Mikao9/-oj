#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<tuple<string, string, long long>> edges;
    edges.reserve(n);

    unordered_map<string, int> idx;
    vector<string> city;

    auto getId = [&](const string &name) {
        auto it = idx.find(name);
        if (it != idx.end()) return it->second;
        int id = static_cast<int>(city.size());
        idx[name] = id;
        city.push_back(name);
        return id;
    };

    for (int i = 0; i < n; ++i) {
        string a, b;
        long long w;
        cin >> a >> b >> w;
        edges.push_back({a, b, w});
        getId(a);
        getId(b);
    }

    int V = static_cast<int>(city.size());
    vector<vector<pair<int, long long>>> g(V);
    for (auto &e : edges) {
        string a, b;
        long long w;
        tie(a, b, w) = e;
        int u = idx[a], v = idx[b];
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }

    const long long INF = (long long)4e18;
    long long bestSum = INF;
    string bestCity;

    for (int s = 0; s < V; ++s) {
        vector<long long> dist(V, INF);
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
        dist[s] = 0;
        pq.push({0, s});

        while (!pq.empty()) {
            auto cur = pq.top();
            pq.pop();
            long long d = cur.first;
            int u = cur.second;
            if (d != dist[u]) continue;
            for (auto &nx : g[u]) {
                int v = nx.first;
                long long w = nx.second;
                if (dist[v] > d + w) {
                    dist[v] = d + w;
                    pq.push({dist[v], v});
                }
            }
        }

        long long sum = 0;
        for (int i = 0; i < V; ++i) sum += dist[i];

        if (sum < bestSum || (sum == bestSum && city[s] < bestCity)) {
            bestSum = sum;
            bestCity = city[s];
        }
    }

    cout << bestCity << ' ' << bestSum << "\n";
    return 0;
}
