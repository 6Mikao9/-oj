#include<bits/stdc++.h>
using namespace std;
int main(){
int n;
cin >> n;
vector<double> v;
for(int i=0;i<n;i++){
double x;
	cin >> x;
	v.push_back(x);
}
sort(v.begin(),v.end());
double ans;
if (n % 2) ans = v[n / 2];
else ans = (v[n / 2 - 1] + v[n / 2]) / 2.0;
cout << fixed << setprecision(6) << ans;
return 0;
}