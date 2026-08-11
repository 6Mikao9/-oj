#include<bits/stdc++.h>
using namespace std;
struct Node{
	vector<int> cld;
	int id;
	int re;
	Node(){
		cld.resize(3,-1);
	}
}; 
struct Tmp{
	int id,c,pair;
	Tmp(int i,int cc){
		id=i;
		c=cc;
	}
};
map<int,Node> tree;
int main(){
	//freopen("D:\\Program Files\\devcpp\\input.txt","r",stdin);
	int n; 
	cin>>n;
	int root=-1;
	while(n--){
		int id;
		cin>>id;
		if(root==-1)root =id;
		for(int i=0;i<3;i++){
			cin >> tree[id].cld[i];
		}
	}
	int id,c;
	vector<Tmp> v;
	while(cin >> id >>c){
		Tmp t(id,c);
		v.push_back(t);
	}
	sort(v.begin(),v.end(),[](const Tmp&a,const Tmp& b){
		if(a.c==b.c){
			return a.id<b.id;
		}else return a.c>b.c;
	});
	
	int index=0;
	queue<int> q;
	q.push(root);
	while(!q.empty()){
		int tp=q.front();
		q.pop();
		if(tp<100) v[index++].pair=tp;
		for(auto &a:tree[tp].cld){
			if(a!=-1)q.push(a);
		}
	} 
	
	for(auto &a:v){
		cout<<a.id<<" "<<a.pair<<endl;
	}
}