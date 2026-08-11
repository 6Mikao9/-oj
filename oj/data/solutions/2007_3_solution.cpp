#include<bits/stdc++.h>
using namespace std;

int main(){
	int n,m;
	map<int,int,greater<int>> exp;  //e-xi
	cin >> n;
	for(int i=0;i<n;i++){
		int x,e;
		cin >> x>>e;
		exp[e]=x;
	} 
	cin >> m;
	for(int i=0;i<m;i++){
		int x,e;
		cin >> x>>e;
		exp[e]+=x;
	} 
	bool first=true;
	bool output=false; 
	for(auto p:exp){
		if(p.second==0)continue;
		output=true;
		if(first){
			first=false;
		}else {
			cout<<"+";
		}
		if(p.second!=1){
			cout<<p.second;
		}
		
		
		if(p.first==0){
			if(p.second==1){
				cout<<p.second;
			}
		}else if(p.first==1){
			cout<<"x";
		}else{
			cout<<"x"<<"^" <<p.first;
		}
	} 
	if(!output)cout<<"0";
}