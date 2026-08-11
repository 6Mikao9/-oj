#include<bits/stdc++.h>
using namespace std;
int a[10000],b[10000];
unordered_set<int> s1;
unordered_set<int> s2;
int main(){
int n,m;
cin>>n;
int t;
for(int i=0;i<n;i++){
	cin>>t;
    s1.insert(t);
}
cin>>m;
for(int i=0;i<m;i++){
	cin>>t;
    s2.insert(t);
}
if(s1.size()!=s2.size()){
	cout<<"not equal!"<<endl;
	return 0;
}
int i=0;
for(int t:s1){
    a[i++]=t;
}
i=0;
for(int t:s2){
    b[i++]=t;
}
sort(a,a+s1.size());
sort(b,b+s1.size());
for(int i=0;i<s1.size();i++){
    if(a[i]!=b[i]){
        cout<<"not equal!"<<endl;
        return 0;
    }
}
cout<<"equal!"<<endl;
return 0;
}