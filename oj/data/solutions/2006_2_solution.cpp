#include<bits/stdc++.h>
using namespace std;
struct stu{
    string name;
    int score;
    int order;
    bool operator<(const stu& rhs) const{
        return score > rhs.score?true:order<rhs.order;
    }
};
int main(){
    int n;
    cin >> n;
    vector<stu> sts(n);
    for(int i=0;i<n;i++){
        cin >> sts[i].name >> sts[i].score;
        sts[i].order = i;
    }
    sort(sts.begin(),sts.end());

    for(int i=0;i<n;i++){
        cout << sts[i].name << " " << sts[i].score << endl;
    }
}