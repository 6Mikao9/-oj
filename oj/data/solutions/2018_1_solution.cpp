#include<bits/stdc++.h>
using namespace std;
vector<vector<int>> vs; 
vector<int> build(){
	vector<int> v(5);
	v[4]=1;
	return v; 
}
bool check(vector<int> l,vector<int> r){
	if(r[0]==l[2]&&r[1]==l[3]){ return true;
	}
	return false;
}
void connect(vector<int> nv){
	int flag=1;
	while(flag){
		flag=0;
		auto iter=vs.begin();
		while(iter!=vs.end()){
			auto ov=*iter;
			if(check(ov,nv)){
				nv[0]=ov[0];
				nv[1]=ov[1];
				nv[4]+=ov[4];
				flag=1;
				vs.erase(iter);
				break;
			}else if(check(nv,ov)){
				nv[2]=ov[2];
				nv[3]=ov[3];
				nv[4]+=ov[4];
				flag=1;
				vs.erase(iter);
				break;
			}else
			iter++;
		}
	}
	vs.push_back(nv);
}
int main(){
	//freopen("input.txt","r",stdin);
	int N;
	cin>>N;
	for(int i=0;i<N;i++){
		auto v=build();
		cin>>v[0]>>v[1]>>v[2]>>v[3];
		connect(v);
	}
	
	int kp=-1,x,y;
	for(auto vv:vs){
		if(vv[4]>kp){
			kp=vv[4];
			x=vv[0];
			y=vv[1];
		}
	}
	cout<<kp<<" "<<x<<" "<<y;
	
	
}