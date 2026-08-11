#include<bits/stdc++.h>
using namespace std;
struct node{
	string n;
	string p;
	node(string tmp=""){
		n=tmp;
	}
};
map<string,node> mp;
vector<string> findpath(string x,string root){
	vector<string>path;
	while(x!=root){
		path.push_back(x);
		x=mp[x].p;
	}
	path.push_back(root);
	reverse(path.begin(),path.end());
	return path;
}
int main(){
	//freopen("input.txt","r",stdin);
	int n;
	cin>>n;
	string tmp;
	cin>>tmp;
	node root(tmp);
	mp[tmp] =root;
	for(int i=0;i<n-1;i++){
		string p;
		cin >> p;	
		string s;
		cin >>s;
		node son(s);
		son.p=p; 
		mp[s]=son;
	}
	string x,y;
	vector<string>pathx,pathy;
	cin>>x>>y;
	pathx=findpath(x,tmp);
	pathy=findpath(y,tmp);
if(x==y){cout<<"公共祖先："<<x<<"，两节点相差层数：0";return 0;}
	cout<<"公共祖先：";
	for(int i=1;i<min(pathx.size(),pathy.size());i++) {
		if(pathx[i]!=pathy[i]){
			cout<<pathx[i-1];
			break;
		}
	}
	//if(pathx.size()==1||pathy.size()==1)cout<<pathx[0];
	cout<<"，两节点相差层数："<<abs((int)pathx.size()-(int)pathy.size());
	
	return 0;
}