#include<bits/stdc++.h>
using namespace std;

int main(){
   int n;
   cin>>n; 
   unordered_map<int,int> m1;
   for(int i=0;i<n;i++){
   	int c;
   	cin >> c;
   	m1[c]=m1.count(c)==0?1:m1[c]+1;
   }  
   int m;
   cin>>m;
   if (m!=n){
   	cout<<"not equal!"; 
   	return 0;
   }
   unordered_map<int,int> m2;
   for(int i=0;i<m;i++){
   	int c;
   	cin >> c;
   	m2[c]=m2.count(c)==0?1:m2[c]+1;
   }  
   for(auto a:m1){
   	if(m2[a.first]!=a.second){
   		cout<<"not equal!"; 
   		return 0;		
	}
   }
   cout<<"equal!"; 
}