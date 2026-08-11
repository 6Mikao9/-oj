#include<bits/stdc++.h>
using namespace std;

int sp=0;
int a[100000];

void init(){
    for(int i=2;i<=100000;i++){
        int flag=1;
        for(int j=0;j<sp;j++){
            if(i%a[j]==0) {flag=0;break;}
            if(a[j]*a[j]>i) break;  // 优化：只需试除到sqrt(i)
        }
        if(flag) a[sp++]=i;
    }
}

int main(){
    int n;
    cin>>n;
    init();
    
    bool first = true;  // 控制格式
    bool found = false;
    
    for(int i=0; i<sp && a[i]<=n; i++){
        if(a[i]%10==1){
            if(!first) cout << " ";  // 不是第一个才输出空格
            cout << a[i];
            first = false;
            found = true;
        }
    }
    
    if(!found) cout << -1;
    cout << endl;
    
    return 0;
}