#include<bits/stdc++.h>
using namespace std;
int m[20][20];
bool isin(int x,int y){
	return x<20&&y<20&&x>0&&y>0;
}
bool ck1(int x,int y,int o){
	for(int i=0;i<5;i++){
		if(!isin(x+i,y-i))return false;
		if(m[x+i][y-i]!=o)return false;
	}
	return true;
}
bool ck2(int x,int y,int o){
	for(int i=0;i<5;i++){
		if(!isin(x+i,y))return false;
		if(m[x+i][y]!=o)return false;
	}
	return true;
}
bool ck3(int x,int y,int o){
	for(int i=0;i<5;i++){
		if(!isin(x+i,y+i))return false;
		if(m[x+i][y+i]!=o)return false;
	}
	return true;
}
bool ck4(int x,int y,int o){
	for(int i=0;i<5;i++){
		if(!isin(x,y+i))return false;
		if(m[x][y+i]!=o)return false;
	}
	return true;
}
int main(){
	for(int i=1;i<20;i++){
		for(int j=1;j<20;j++){
			cin >> m[i][j];
		}
	}
	bool flag=true;
	for(int i=1;i<20;i++){
		for(int j=1;j<20;j++){
			if(m[i][j]&&(ck1(i,j,m[i][j])||
			ck2(i,j,m[i][j])||
			ck3(i,j,m[i][j])||
			ck4(i,j,m[i][j]))
			){	flag=false;
				cout<<m[i][j]<<":("<<i<<","<<j<<")";
				break;
			}
		}
	}
if(flag)cout<<"no";
}