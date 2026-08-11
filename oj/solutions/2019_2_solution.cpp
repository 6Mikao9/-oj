#include <bits/stdc++.h>
using namespace std;

struct Node {
    int id;
    int children[3];
    int parent;
};

map<int, Node> tree;
map<int, int> depth_map;

void findPath(int from, int to, vector<int>& result) {
    vector<int> path1, path2;
    
    // 从from向上到根
    int temp = from;
    while (temp != -1) {
        path1.push_back(temp);
        temp = tree[temp].parent;
    }
    
    // 从to向上到根
    temp = to;
    while (temp != -1) {
        path2.push_back(temp);
        temp = tree[temp].parent;
    }
    
    // 找到LCA
    int lca_idx1 = path1.size() - 1;
    int lca_idx2 = path2.size() - 1;
    
    while (lca_idx1 >= 0 && lca_idx2 >= 0 && path1[lca_idx1] == path2[lca_idx2]) {
        lca_idx1--;
        lca_idx2--;
    }
    lca_idx1++;
    lca_idx2++;
    
    // 构造路径：from -> LCA -> to
    result.clear();
    for (int i = 0; i <= lca_idx1; i++) {
        result.push_back(path1[i]);
    }
    for (int i = lca_idx2 - 1; i >= 0; i--) {
        result.push_back(path2[i]);
    }
}

int main() {
    int n;
    cin >> n;
    
    int root = -1;
    
    for (int i = 0; i < n; i++) {
        int p, c1, c2, c3;
        cin >> p >> c1 >> c2 >> c3;
        
        if (i == 0) {
            root = p;
        }
        
        tree[p].id = p;
        tree[p].children[0] = c1;
        tree[p].children[1] = c2;
        tree[p].children[2] = c3;
        
        if (c1 != -1) tree[c1].parent = p;
        if (c2 != -1) tree[c2].parent = p;
        if (c3 != -1) tree[c3].parent = p;
    }
    
    tree[root].parent = -1;

    // BFS 计算层数
    queue<int> q;
    depth_map[root] = 1;
    q.push(root);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int k = 0; k < 3; k++) {
            int v = tree[u].children[k];
            if (v == -1) continue;
            if (!depth_map.count(v)) {
                depth_map[v] = depth_map[u] + 1;
                q.push(v);
            }
        }
    }
    
    int m;
    cin >> m;
    
    vector<pair<int, int>> tasks; // (leaf, priority)
    
    for (int i = 0; i < m; i++) {
        int leaf, prio;
        cin >> leaf >> prio;
        tasks.push_back({leaf, prio});
    }
    
    // 按优先级排序（数值越小优先级越高）
    sort(tasks.begin(), tasks.end(), [](auto& a, auto& b) {
        return a.second < b.second;
    });
    
    int current = root;
    vector<int> path;

    for (int i = 0; i < m; i++) {
        int target = tasks[i].first;

        findPath(current, target, path);

        for (int j = 0; j < (int)path.size(); j++) {
            if (j) cout << " ";
            cout << path[j];
        }
        cout << '\n';

        current = target;
    }

    // 最后回到根节点
    findPath(current, root, path);
    for (int j = 0; j < (int)path.size(); j++) {
        if (j) cout << " ";
        cout << path[j];
    }
    cout << '\n';

    return 0;
}
