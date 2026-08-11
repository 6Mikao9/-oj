#include<bits/stdc++.h>
using namespace std;
struct dev{
	int id,type,port,p;
	set<int>sons;
};
map<int , dev> devs;
void dfs(int id) {
    cout << id << " ";
    for (auto &son : devs[id].sons) {  // set 自动升序
        dfs(son);
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        dev d;
        cin >> d.id >> d.type >> d.port >> d.p;
        devs[d.p].sons.insert(d.id);
    }
    int f;
    cin >> f;
    dfs(f);
    cout << endl;
}