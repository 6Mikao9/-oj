#include<bits/stdc++.h>
using namespace std;
struct Node{
	int p;
	Node(){
		p=-1;
	}
};
map<int,Node> i2n;
vector<int> findp(int s){
	vector<int> res;
	while(s!=-1){
		res.push_back(s);
		s=i2n[s].p;
	}
//			for(auto i:res)cout<<i<<" ";
//		cout<<endl;
	return res;
}

vector<int> getl(int s,int e){
	auto p1= findp(s);
	auto p2= findp(e);
	reverse(p2.begin(),p2.end());
	int kp;
	while(p1.back()==p2.front()){
		kp=p1.back();
		p1.pop_back();
		p2.erase(p2.begin());
	}
	p1.push_back(kp);
	for(auto i:p2){
		p1.push_back(i);
	}
	return p1;
}

int main(){
	//freopen("input.txt","r",stdin);
	int n;
	cin >> n; 
	int root;
//	cin >> root;
//	int t=3;
//	while(3--){
//		int x;
//		cin >> x;
//		if(x==-1)coutinue;
//		i2n[x].p=root;
//	}
//	
	for(int i=0;i<n;i++){
		int t=3;
		int np;
		cin >> np;
		if(i==0) root = np; 
		while(t--){
			int x;
			cin >> x;
			if(x==-1)continue;
			i2n[x].p=np;
		}
	}
	
	cin >> n;
	vector<pair<int,int>>vis;
	for(int i=0;i<n;i++){
		int x,pri;
		cin >> x>> pri;
		vis.push_back({pri,x});
	}
	sort(vis.begin(),vis.end());
	int st=root;int ed;
	vis.push_back({0,root});
	for(auto a:vis){
		ed=a.second;
		auto v=getl(st,ed);
		st=ed;
		for(auto i:v)cout<<i<<" ";
		cout<<endl;
	}
}