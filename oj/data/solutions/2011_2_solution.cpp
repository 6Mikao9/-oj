#include<bits/stdc++.h>
using namespace std;
unordered_map<int,int> m;
int main(){
   int n1,n2;
   cin>>n1>>n2;
   vector<vector<int>> v1(n1,vector<int>(n2));
   for(int i=0;i<n1;i++){
   	for(int j=0;j<n2;j++){
   		cin >> v1[i][j];
	   }
   } 
   
   int m1,m2;
   cin >>m1>>m2;
   vector<vector<int>> v2(m1,vector<int>(m2));
   for(int i=0;i<m1;i++){
   	for(int j=0;j<m2;j++){
   		cin >> v2[i][j];
	   }
   }
   int x,y;
   cin >> x>> y;
	for(int i=0;i<m1;i++){
   		for(int j=0;j<m2;j++){
   			if(x-1+i<n1&&y-1+j<n2)
   			  v1[x-1+i][y-1+j]=v2[i][j];
	   	}
   	}
   	
   for(int i=0; i<n1; i++){
    for(int j=0; j<n2; j++){
        cout << v1[i][j];
        if(j < n2-1) cout << " ";  // 不是最后一个才加空格
    }
    cout << endl;   
}


}