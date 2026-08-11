#include<bits/stdc++.h>
using namespace std; 

struct Node{
	int id;
	vector<Node*>  ps;
	Node(){
		ps.resize(4,nullptr);
	}
};
using VN= vector<Node*> ;
map<int,Node*> mp;

int maxn=-1;
int maxd=-1;
int kpid;
int kpo;
int go=0;

void porder(Node *root,int d){
	go++;
	int ct=0;
	for(int i=1;i<=3;i++){
		ct+=(root->ps[i]!=nullptr);
	}
	if(ct>maxn||(ct==maxn&&(d>maxd))){
		kpid=root->id;
		kpo=go;
		maxn=ct;
		d=maxd;
	}
	for(int i=1;i<=3;i++){
		if(root->ps[i]){
			porder(root->ps[i],d+1);
		}
	}
	
}

int main(){
	//freopen("input.txt","r",stdin);
	int n;
	cin >> n;

	
	Node * root =new Node();
	int id;
	cin>>id;
	mp[id]=root;
	root->id=id;
	for(int i=1;i<=3;i++){
		int nid;
		cin>>nid;
		if(!nid)continue;
		Node * sub = new Node();
		root->ps[i]=sub;
		sub->id=nid;
		mp[nid]=sub;
	}
	n--;
	
	
	while(n--){
		int id;
		cin>>id;
		Node *par=mp[id];
		for(int i=1;i<=3;i++){
			int nid;
			cin>>nid;
			if(!nid)continue;
			Node * sub = new Node();
			par->ps[i]=sub;
			sub->id=nid;
			mp[nid]=sub;
		}
	}
	
	porder(root,1);
	cout<< kpid<<" "<<kpo;
	
	
	return 0;
}