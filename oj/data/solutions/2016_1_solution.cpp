#include<bits/stdc++.h>
using namespace std;
typedef long long ll; 
int main() {
	ll m;
	cin>>m;
	string s=to_string(m);
	reverse(s.begin(),s.end());
	ll n=stoll(s);
	if(n%m==0){
		cout << m <<"*"<< n/m<<"="<<s; 
	} else{
		cout<< m<<" "<<s; 
	}
	 
		
    return 0;
}