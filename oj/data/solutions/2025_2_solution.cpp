#include<bits/stdc++.h>
using namespace std;
using pis=pair<int,string> ;
using pss = pair<string,string>;
using ll=long long;
const int INF =1e9;
set<string> cts;
map<pss,int> edges;

int main(){
	int n;
	cin >> n;
	int t=0;
	while(n--){
		string s,t;int d;
		cin >> s>> t>> d;
		cts.insert(s);
		cts.insert(t);
		edges[{s,t}]=d;
		edges[{t,s}]=d;
	}
	map<pss,int> dist;

	string kp;
	for(auto a:cts){
		for(auto b:cts){
			if(a==b)dist[{a,b}]=0;
			else{
				dist[{a,b}]=INF;
				dist[{b,a}]=INF;
			}
		}
	}
	for(auto edge:edges){
		dist[edge.first]=edge.second;
	}
	int MIN =INF;
	for(auto k:cts){
		for(auto i:cts){
			for(auto j:cts){
				if(dist[{i,k}]!=INF&&dist[{k,j}]!=INF)
					dist[{i,j}]=min(dist[{i,k}]+dist[{k,j}],dist[{i,j}]);
			}
		}
	}

	for(auto i:cts){
		int sum=0;
		for(auto j:cts){
			sum+=dist[{i,j}];	
		}
		if(sum<MIN){
			kp=i;
			MIN=sum;
		}
	}
	
	cout<<kp<<" "<<MIN;
}