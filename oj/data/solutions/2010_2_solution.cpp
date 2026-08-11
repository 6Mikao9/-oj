#include<bits/stdc++.h>
using namespace std;
int main(){
	//freopen("D:\\Program Files\\devcpp\\input.txt","r",stdin);
	string a,b;
	cin >> a>> b;
	int n=a.size();
	int m=b.size();
	int i=0,j=0;
	string res;
	while(i<n&&j<m){
		char ad;
		if(a[i]<b[j]){
			ad=a[i++];
		}else{
			ad=b[j++];
		}
		if(res.empty()||ad>res.back())res.push_back(ad);
	} 

	while(i<n){
		char ad;
		ad=a[i++];
	
		if(res.empty()||ad>res.back())res.push_back(ad);
	}
	while(j<m){
		char ad;

		ad=b[j++];
		if(res.empty()||ad>res.back())res.push_back(ad);
	}
	cout<<res;
}