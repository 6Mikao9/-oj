#include<bits/stdc++.h>
using namespace std;
unordered_map<int,int> m;
int main(){
   int M,N;
   cin>>M>>N;
   int found=0; 
   for(int i=M;i<=N;i++){

   		int sum=0;
   		int end = i/2;
	    for(int j=1;j<=end;j++){
	    	if(i%j==0){
	    		sum+=j;
			}
		}

		m[sum]=i;
		
		if(m.count(i)==1&&m[i]==sum&&m[i]!=i){
			found=1;
			cout<<m[i]<<" "<<i<<endl; 
		}
   } 
   if (!found) cout << "NONE" << endl;
}