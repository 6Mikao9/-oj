#include<bits/stdc++.h>
using namespace std;
int avail[10001] ; 
int sum[10001];
void init(){
	int l;
	for(int m=0;m<=20000;m++)
		for(int n=m+1;n<=10000;n++){
			l=(m+n)*(n-m+1)/2;
			if(l>10000) break;
			avail[l]=1;
		}
	
	for(int i=1;i<10001;i++){
		sum[i]=sum[i-1]+i;
	}
}
int main(){
    int x; 
    cin>>x;
    init();
    if(avail[x]) {
    	for(int i=0;i<x;i++){
    		for(int j=i+1;j<x;j++){
    			if(sum[j]-sum[i]==x){
    				for(int s=i+1;s<=j;s++){
    					cout<<s<<" ";
					}
					cout<<endl;
				}
			}
		}
	}else{
		cout<<"NONE"<<endl;
	}
	return 0;
}