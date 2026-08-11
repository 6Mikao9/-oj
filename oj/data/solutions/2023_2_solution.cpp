#include<bits/stdc++.h>
#define D first
#define L second
using namespace std;
using pii=pair<int,int>;
int main(){
	//freopen("input.txt","r",stdin);
	int op[5]={0,2,1,4,3};
	vector<pii> v;
	int d,l;
	char c;
	while(1){
		cin >>d>>c>>l;
		if(d==0&&l==0)break;
		if(v.size()){
			auto &lst=v.back();
			if(lst.D==d){
				lst.L+=l;
			}else if(op[d]==lst.D){
				lst.L -=l;
				if(lst.L<0){
					lst.L=-lst.L;
					lst.D=d;
				}else if(lst.L==0){
					v.pop_back();
				}
				
			}else{
				v.push_back({d,l});
			}
		}else{
			v.push_back({d,l});
		}
	}
	reverse(v.begin(),v.end());
	for(auto &a:v){
		cout << op[a.D]<< "-" <<a.L<<" ";
	}
	if(!v.size()){
		cout<<"0-0";
	}
}