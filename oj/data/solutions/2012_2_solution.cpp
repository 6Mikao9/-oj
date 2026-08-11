#include<bits/stdc++.h>
using namespace std;
int m[100][100]; 
int vis[100][100];
int n; 
//int dir[4][2]={{0}}
bool dfs(int x,int y){
	if(x==-1||y==-1||x==n||y==n) return false;
	if(vis[x][y]) return true;
	vis[x][y]=1;
	if(m[x][y]==1||m[x][y]==-1) return true;
	if(dfs(x-1,y)&&dfs(x+1,y)&&dfs(x,y-1)&&dfs(x,y+1)){
		m[x][y]=-1;
		return true;
	}else{
		m[x][y]=0;
		return false;
	}
}

int main(){
	cin>>n;
	for(int i=0;i<n;i++)
		for(int j=0;j<n;j++)
			cin>>m[i][j];
	for(int i=0;i<n;i++)
		for(int j=0;j<n;j++)
			dfs(i,j);
	int sum =0;
	for(int i=0;i<n;i++)
		for(int j=0;j<n;j++)
			if(m[i][j]==-1)	sum++;
	
	cout<<sum;
	return 0;
}