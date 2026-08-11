#include <bits/stdc++.h>
using namespace std;

struct Node {
    string name;
    bool isDir;
    long long size;                 // 仅文件有效
    Node* parent;
    unordered_map<string, Node*> children;
    Node(string n, bool d, long long s, Node* p)
        : name(n), isDir(d), size(s), parent(p) {}
};

Node* root;

// "/a/b" -> ["a","b"]; "/" -> []
vector<string> splitPath(const string& p) {
    vector<string> comps;
    string cur;
    for (char c : p) {
        if (c == '/') {
            if (!cur.empty()) { comps.push_back(cur); cur.clear(); }
        } else {
            cur += c;
        }
    }
    if (!cur.empty()) comps.push_back(cur);
    return comps;
}

Node* findNode(const string& path) {
    vector<string> comps = splitPath(path);
    Node* cur = root;
    for (auto& c : comps) {
        auto it = cur->children.find(c);
        if (it == cur->children.end()) return nullptr;
        cur = it->second;
    }
    return cur;
}

// 返回 path 的父目录,并通过 name 带回最后一级名字;找不到父目录返回 nullptr
Node* findParent(const string& path, string& name) {
    vector<string> comps = splitPath(path);
    if (comps.empty()) return nullptr;   // 根路径
    name = comps.back();
    Node* cur = root;
    for (size_t i = 0; i + 1 < comps.size(); ++i) {
        auto it = cur->children.find(comps[i]);
        if (it == cur->children.end()) return nullptr;
        cur = it->second;
    }
    return cur;
}

long long calcSize(Node* node) {
    if (!node->isDir) return node->size;
    long long sum = 0;
    for (auto& kv : node->children) sum += calcSize(kv.second);
    return sum;
}

bool isDescendant(Node* anc, Node* node) {
    while (node) {
        if (node == anc) return true;
        node = node->parent;
    }
    return false;
}

void printTree(Node* node, int depth) {
    if (node == root) {
        cout << "/\n";
    } else {
        for (int i = 0; i < depth; ++i) cout << "  ";
        if (node->isDir) cout << node->name << "/\n";
        else cout << node->name << " " << node->size << "\n";
    }
    vector<string> names;
    for (auto& kv : node->children) names.push_back(kv.first);
    sort(names.begin(), names.end());
    for (auto& nm : names) printTree(node->children[nm], depth + 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    root = new Node("/", true, 0, nullptr);

    int n;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        string path, type;
        long long sz;
        cin >> path >> type >> sz;
        string name;
        Node* parent = findParent(path, name);
        if (!parent) continue;            // 根记录,已存在
        bool isDir = (type == "D");
        parent->children[name] = new Node(name, isDir, isDir ? 0 : sz, parent);
    }

    int m;
    cin >> m;
    for (int i = 0; i < m; ++i) {
        string op;
        cin >> op;
        if (op == "mkdir") {
            string path;
            cin >> path;
            string name;
            Node* parent = findParent(path, name);
            if (parent && parent->isDir && !parent->children.count(name)) {
                parent->children[name] = new Node(name, true, 0, parent);
            }
        } else if (op == "create") {
            string path;
            long long sz;
            cin >> path >> sz;
            string name;
            Node* parent = findParent(path, name);
            if (parent && parent->isDir && !parent->children.count(name)) {
                parent->children[name] = new Node(name, false, sz, parent);
            }
        } else if (op == "rm") {
            string path;
            cin >> path;
            Node* node = findNode(path);
            if (node && node != root && node->parent) {
                node->parent->children.erase(node->name);
            }
        } else if (op == "mv") {
            string src, dst;
            cin >> src >> dst;
            Node* srcNode = findNode(src);
            if (!srcNode || srcNode == root) continue;
            Node* dstNode = findNode(dst);
            Node* newParent;
            string newName;
            if (dstNode && dstNode->isDir) {
                newParent = dstNode;
                newName = srcNode->name;
                if (newParent->children.count(newName)) continue;   // 目标下已存在同名
            } else {
                newParent = findParent(dst, newName);
                if (!newParent || !newParent->isDir) continue;
                if (newParent->children.count(newName)) continue;   // dst 已存在(文件或目录)
            }
            if (srcNode->isDir && isDescendant(srcNode, newParent)) continue;  // 移入自身
            srcNode->parent->children.erase(srcNode->name);
            srcNode->parent = newParent;
            srcNode->name = newName;
            newParent->children[newName] = srcNode;
        } else if (op == "size") {
            string path;
            cin >> path;
            Node* node = findNode(path);
            if (!node) cout << -1 << "\n";
            else cout << calcSize(node) << "\n";
        }
    }

    printTree(root, 0);
    return 0;
}
