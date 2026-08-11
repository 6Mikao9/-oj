#include <bits/stdc++.h>
using namespace std;

struct Device {
    int id = -1;
    int type = 0;
    int port = 0;
    int parent = -1;
    vector<int> children;
};

static void dfs(int u, unordered_map<int, Device> &devs, vector<int> &out) {
    auto it = devs.find(u);
    if (it == devs.end()) return;

    out.push_back(u);
    auto &ch = it->second.children;
    sort(ch.begin(), ch.end());
    for (int v : ch) dfs(v, devs, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    unordered_map<int, Device> devs;
    devs.reserve(static_cast<size_t>(n) * 2 + 8);

    for (int i = 0; i < n; ++i) {
        int id, type, port, parent;
        cin >> id >> type >> port >> parent;

        if (!devs.count(id)) devs[id] = Device();
        devs[id].id = id;
        devs[id].type = type;
        devs[id].port = port;
        devs[id].parent = parent;

        if (parent != -1) {
            if (!devs.count(parent)) devs[parent] = Device();
            devs[parent].children.push_back(id);
        }
    }

    int faultySwitchId;
    if (!(cin >> faultySwitchId)) return 0;

    vector<int> ans;
    dfs(faultySwitchId, devs, ans);

    for (size_t i = 0; i < ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << "\n";

    return 0;
}
