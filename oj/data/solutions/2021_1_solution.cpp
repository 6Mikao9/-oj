#include<bits/stdc++.h>
using namespace std;
#define X first 
#define Y second 
using pii = pair<int,int> ;//开始 大小 
vector<pii> vp; 

void pt(int kp){
	bool f=true; 
	for(int i=kp;f||i!=kp;i=(i+1)%vp.size()){
		f=false;
		cout<<vp[i].X<<" "<<vp[i].Y<<endl;
	} 
	cout<<endl;
}

int main(){
	//freopen("D:\\Program Files\\devcpp\\input.txt","r",stdin);
	int n ;
	cin >> n;
	for(int i=0;i<n;i++){
		int s,l;
		cin >> s>>l;
		vp.push_back({s,l});
	}
//	pt(0);//
	int kp=0;
	while(1){
		int all;
		cin >> all;
		if(all==-1) break;
		bool f=true; 
		int kpsize=1e9;
		int kpindex=-1;
		for(int i=kp;f||i!=kp;i=(i+1)%vp.size()){
			f=false;
			if(vp[i].Y>=all){
				if(vp[i].Y<kpsize){
					kpsize= vp[i].Y;
					kpindex=i;
				}
			}
		} 
		if(kpindex==-1){
			continue;
		}else{
			
			if(vp[kpindex].Y==all){
				vp.erase(vp.begin()+kpindex);
				kp=(kpindex)%vp.size();
			} else{
				vp[kpindex].Y-=all;
				kp=(kpindex)%vp.size();
			}
		}
//		cout<<"jp:"<<kpindex<<endl;
//		pt(kp);
	}
	pt(kp);
}