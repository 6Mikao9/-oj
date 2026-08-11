#include<bits/stdc++.h>
using namespace std;
struct LOG{
	string p;
	string station;
	string start;
	string ed;
	void in(){
		cin>>p>>station>>start>>ed;
	}
	void out(){
		cout<<p<<" "<<station<<" "<<start<<" "<<ed<<endl;
	}
};
int main(){
	//freopen("input.txt","r",stdin);
	int n;
	cin>>n;
	vector<LOG> logs;
	for(int i=0;i<n;i++){
		LOG l;
		l.in();
		logs.push_back(l);
	}
	string t;
	cin >> t;
	sort(logs.begin(),logs.end(),[](const LOG&a,const LOG &b){
		if(a.start==b.start){
			return a.p<b.p;
		}else return a.start<b.start;
	});
	vector<LOG> targets;
	for(auto& a:logs){
		if(a.p==t){
			targets.push_back(a);
		}
	}
	for(auto& a:logs){
		for(LOG &target:targets)
		if(a.p!=t&&a.station==target.station&&(a.start<=target.ed&&a.ed>=target.start||target.start<=a.ed&&target.ed>=a.start)){
			a.out();
		}
	}
	
}