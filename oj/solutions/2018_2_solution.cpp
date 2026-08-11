#include <bits/stdc++.h>
using namespace std;

struct Node {
    int id;
    int children[3];
    int childCount;
    int depth;
};

map<int, int> idToIndex;
vector<Node> nodes;
int traversalTime = 0;
int maxChildCount = -1;
int maxDepth = -1;
int targetId = -1;
int targetOrder = -1;

void preOrder(int idx, int depth) {
    if (idx == -1 || idx >= nodes.size()) return;
    
    traversalTime++;
    nodes[idx].depth = depth;
    
    int currentCount = nodes[idx].childCount;
    int currentDepth = depth;
    
    // 判断是否更优
    bool isBetter = false;
    if (currentCount > maxChildCount) {
        isBetter = true;
    } else if (currentCount == maxChildCount && currentDepth > maxDepth) {
        isBetter = true;
    }
    
    if (isBetter) {
        maxChildCount = currentCount;
        maxDepth = currentDepth;
        targetId = nodes[idx].id;
        targetOrder = traversalTime;
    }
    
    // 递归遍历三个孩子（左、中、右）
    for (int i = 0; i < 3; i++) {
        if (nodes[idx].children[i] != 0) {
            int childId = nodes[idx].children[i];
            if (idToIndex.count(childId)) {
                preOrder(idToIndex[childId], depth + 1);
            }
        }
    }
}

int main() {
    int n;
    cin >> n;
    
    nodes.resize(n);
    int rootId = -1;
    
    // 先读取所有输入，建立id到index的映射
    vector<array<int, 4>> input(n);
    for (int i = 0; i < n; i++) {
        cin >> input[i][0] >> input[i][1] >> input[i][2] >> input[i][3];
        int parentId = input[i][0];
        
        // 第一个出现的节点是根
        if (rootId == -1) rootId = parentId;
        
        if (!idToIndex.count(parentId)) {
            idToIndex[parentId] = idToIndex.size();
        }
    }
    
    // 重新调整nodes大小
    int nodeCount = idToIndex.size();
    nodes.resize(nodeCount);
    
    // 填充节点信息
    for (int i = 0; i < n; i++) {
        int parentId = input[i][0];
        int idx = idToIndex[parentId];
        
        nodes[idx].id = parentId;
        nodes[idx].childCount = 0;
        for (int j = 0; j < 3; j++) {
            nodes[idx].children[j] = input[i][j + 1];
            if (input[i][j + 1] != 0) {
                nodes[idx].childCount++;
                // 创建子节点映射
                if (!idToIndex.count(input[i][j + 1])) {
                    idToIndex[input[i][j + 1]] = idToIndex.size();
                }
            }
        }
    }
    
    // 确保nodes大小足够
    nodes.resize(idToIndex.size());
    // 重新填充所有节点id
    for (auto& p : idToIndex) {
        nodes[p.second].id = p.first;
    }
    for (int i = 0; i < n; i++) {
        int parentId = input[i][0];
        int idx = idToIndex[parentId];
        nodes[idx].childCount = 0;
        for (int j = 0; j < 3; j++) {
            nodes[idx].children[j] = input[i][j + 1];
            if (input[i][j + 1] != 0) {
                nodes[idx].childCount++;
            }
        }
    }
    
    if (rootId != -1 && idToIndex.count(rootId)) {
        preOrder(idToIndex[rootId], 1);
    }
    
    cout << targetId << " " << targetOrder << endl;
    return 0;
}
