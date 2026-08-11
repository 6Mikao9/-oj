#include<bits/stdc++.h>
using namespace std;
struct node{
    int val;
    int pos;
};

bool cmp(const node& n1, const node& n2){
    return n1.val < n2.val;
}

int main(){
    int n; 
    cin >> n;
    vector<node> v(n);
    vector<int> ans(n);
    
    for (int i = 0; i < n; i++){
        cin >> v[i].val;
        v[i].pos = i;
    } 
    
    sort(v.begin(), v.end(), cmp);
    
    // Dense rank：相同值相同次序
    int rank = 1;
    for(int i = 0; i < n; i++){
        if(i > 0 && v[i].val != v[i-1].val){
            rank++;
        }
        ans[v[i].pos] = rank;
    }
    
    for(int i = 0; i < n; i++){
        cout << ans[i];
        if(i < n-1) cout << " ";
    }
    cout << endl;
}