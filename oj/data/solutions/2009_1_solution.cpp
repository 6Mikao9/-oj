#include<bits/stdc++.h>
using namespace std;
typedef long double ld;
ld cal(ld x,ld y){
	y = y * 2.0 / 3.0 + x / (3.0 * y * y);
	return y;
}
int main(){
	ld x;
	int n; 
	while(cin >> x >>n) {
		ld yn=x;
		for(int i=0;i<n;i++){
			yn=cal(x,yn);
		}
		cout<<fixed<<setprecision(6)<<yn<<endl;
	}
}