#include<bits/stdc++.h>
using namespace std;
struct good{
	string type_id;
	int total_amount,total_sales;
	good(){
		total_amount=total_sales=0;//这能成功初始化吗 
	}
};
map<string , good > kymap;
set<string> ss;
int main(){
	int n;
	cin >> n;
	for(int i=0;i<n;i++){
		string type,id,type_id;
		cin >> type >>id;
		type_id = type+" "+id;
		ss.insert(type_id); 
		int amount,price;
		cin >> amount>>price;
		if(kymap.count(type_id)){
			kymap[type_id].total_amount+=amount;
			kymap[type_id].total_sales+=amount*price;
		}else{
			good g;
			g.type_id = type_id;
			kymap[type_id] = g;
			kymap[type_id].total_amount=amount;
			kymap[type_id].total_sales=amount*price;
		}
	}
	vector<good> vg;
	//map遍历
	for (auto a:ss){
		vg.push_back(kymap[a]);
	}
	sort(vg.begin(),vg.end(),[](const good&a,const good & b){
		if(a.total_sales==b.total_sales){
			return a.type_id<b.type_id;
		}else{
			return a.total_sales>b.total_sales;
		}
	});
	for(auto& a:vg){
		cout<<a.type_id<<" "<<a.total_amount<<" "<<a.total_sales<<endl;
	}
}