#include<bits/stdc++.h>
using namespace std;
using pss = pair<string ,string>;
struct pd{
	pss data;
	int d;
	pd(string a,string b){
		if(a>b) swap(a,b);
		pss dt={a,b};
		data=dt;
		d=0;
		for(int i=0;i<a.size();i++){
			d+=(a[i]==b[i]?0:1);
		}
	}
};
struct cmp{
	const operator()(const pd&a,const pd& b){
		if(a.d==b.d) {
			return a.data>b.data;
		}else{
			return a.d>b.d;
		}
	}
};
int main(){
	int n;
	cin>>n;
	vector<string> v;
	priority_queue<pd,vector<pd>,cmp>  pq;
	for(int i=0;i<n;i++){
		string ns;
		cin >> ns;
		for(auto a:v){
			pd tmp(a,ns);
			pq.push(tmp);
		}
		v.push_back(ns);
	}
	int ct=6;
	while(ct--&&!pq.empty()){
		cout<<pq.top().data.first<< " " <<pq.top().data.second<< " " <<pq.top().d<<endl;
		pq.pop();
	}
	return 0;
}