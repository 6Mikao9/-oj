#include<bits/stdc++.h>
using namespace std;
int gcd(int a,int  b){
	if(a<b){
		swap(a,b);
	}
	for(int i=b;i>0;i--){
		if(b%i==0&&a%i==0){
			return i;
		}
	}
	return -1;
} 

int main(){
	int x,y;
	cin>>x>>y;
	int d=gcd(x,y);
	cout<<x/d<<" "<<y/d; 
	return 0;
}