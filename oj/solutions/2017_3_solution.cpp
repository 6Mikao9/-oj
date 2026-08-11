#include <bits/stdc++.h>
using namespace std;

map<string, string> parent;
map<string, int> depth;

int getDepth(const string& node) {
    if (depth.count(node)) return depth[node];
    // 如果节点没有父节点记录，或者是根节点（父节点为空），深度为0
    if (parent.find(node) == parent.end() || parent[node].empty()) {
        return depth[node] = 0;
    }
    return depth[node] = getDepth(parent[node]) + 1;
}

string findLCA(string a, string b) {
    int da = getDepth(a), db = getDepth(b);
    
    if (da < db) {
        swap(a, b);
        swap(da, db);
    }
    
    // 把较深的节点提升到同一层
    while (da > db && parent.find(a) != parent.end() && !parent[a].empty()) {
        a = parent[a];
        da--;
    }
    
    // 同时向上查找公共祖先
    while (a != b) {
        if (parent.find(a) != parent.end() && !parent[a].empty()) {
            a = parent[a];
        } else {
            break;  // a 已经是根节点
        }
        if (parent.find(b) != parent.end() && !parent[b].empty()) {
            b = parent[b];
        } else {
            break;  // b 已经是根节点
        }
    }
    
    return a;
}

int main() {
    int n;
    cin >> n;
    cin.ignore();
    
    string root;
    getline(cin, root);
    // 根节点的父节点设为空字符串标记
    parent[root] = "";
    
    for (int i = 1; i < n; i++) {
        string line;
        getline(cin, line);
        istringstream iss(line);
        string fa, ch;
        iss >> fa >> ch;
        parent[ch] = fa;
    }
    
    // 读取查询行
    string queryLine;
    getline(cin, queryLine);
    istringstream qss(queryLine);
    string q1, q2;
    qss >> q1 >> q2;
    
    string lca = findLCA(q1, q2);
    int d1 = getDepth(q1), d2 = getDepth(q2);
    int diff = abs(d1 - d2);
    
    cout << "公共祖先：" << lca << "，两节点相差层数：" << diff << endl;
    
    return 0;
}
