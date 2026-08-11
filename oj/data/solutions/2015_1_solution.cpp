#include<bits/stdc++.h>
using namespace std;
int ggg(int a){
	vector<int> v;
	for(int i=1;i<a;i++){
		if(a%i==0){
			v.push_back(i);		
		}
	} 
	int sum=0;
	for(int i=0;i<v.size();i++){
		sum+=v[i];
		cout<<v[i];
		if(i==v.size()-1)cout<<"=";
		else cout<<"+";
	}
	cout<<sum<<endl;
	return sum;
}
int main() {
	int a,b;
	char c;
	cin>> a>>c>>b;
	int sum1=0,sum2=0;
	cout<<a<<",";
	sum1=ggg(a);
	cout<<b<<",";
	sum2=ggg(b);
	if(sum1==b && sum2==a && a!=b) cout << 1;
else cout << 0;

	
    return 0;
}