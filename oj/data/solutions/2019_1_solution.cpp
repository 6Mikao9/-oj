#include<bits/stdc++.h>
using namespace std;
int n=1e7;
vector<int>primes;
vector<bool> isp(n+1,true);
int a,b;
int sindex;
void init(){
	bool flag=true;
	int l=sqrt(n)+1;
	for(int i=2;i<=l;i++){
		if(isp[i]){
			for(int j=2;j*i<=n;j++){
				isp[j*i]=false;
			}
		}
	}
	for(int i=2;i<=n;i++){
		if(isp[i]){
			if(flag&&i>=a){
				flag=false;
				sindex=primes.size();
			}
			primes.push_back(i);
		}
	}
} 
int main(){
	//freopen("input.txt","r",stdin);
	vector<vector<int>> res;
	vector<int> tmp;
	cin>>a>>b;
	init();
	for(int j=1;j<(b-a)/2;j++){
		tmp.clear();
		for(int i=sindex;primes[i]<=b;i++){
			if(tmp.size()==0){
				tmp.push_back(primes[i]);
			}else{
				if(primes[i]-tmp.back()==j){
					tmp.push_back(primes[i]);
				}else{
					if(tmp.size()>2){
						res.push_back(tmp);
					}
					tmp.clear();
					tmp.push_back(primes[i]);
				}
			}
		} 
		if(tmp.size()>2){
		res.push_back(tmp);
		}
	}

					
	for(auto &v: res){
		for(auto &num:v){
			cout<<num<<" " ;
		}
		cout<<endl;
	} 
		
	return 0;
}