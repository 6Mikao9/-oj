#include<bits/stdc++.h>
using namespace std;
struct Win{
	int pos[5];
	Win(){
		for(int i=0;i<5;i++)cin>> pos[i];
	}
	bool check(int x,int y){
		return x>=pos[1]&&y>=pos[2] &&x<=pos[3]&&y<=pos[4];
	}
}; 
vector<Win> vw;
int main(){
	//freopen("D:\\Program Files\\devcpp\\input.txt","r",stdin);
	int n ;
	cin >> n;
	for(int i=0;i<n;i++){
		Win w;
		vw.push_back(w);
	}
	//cout<< vw.size();
	cin >> n;
	for(int i=0;i<n;i++){
		int x,y;
		cin >> x>>y;
		for(auto it=vw.begin();it!=vw.end();it++){
			Win w=*it;
			if(w.check(x,y)){
				vw.erase(it);
				vw.insert(vw.begin(),w);
				break;
			}
		}
	}
	for(Win &w:vw)cout<<w.pos[0]<<" ";
}