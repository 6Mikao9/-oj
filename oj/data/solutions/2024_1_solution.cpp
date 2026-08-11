#include<bits/stdc++.h>
using namespace std;
//substr第二个参数含义忘了
map<char ,int>order;
struct stu{
	string id;
	double total;
	set<string> sports;
	stu(){
		total=0.0;
	}
	bool operator < (const stu&b) const{
		if(id[0]==b.id[0]){
			if(total!=b.total)return total<b.total;
			//num1=id.substr(1);
			//num2=b.id.substr(1);
			return id<b.id;
		}else return order[id[0]]<order[b.id[0]];
	}
	void out(){
		cout<<id<<" ";
		cout<<fixed<<setprecision(2)<<total<<" ";
		vector<string>tmp;
		for(auto &s:sports)tmp.push_back(s);
		sort(tmp.begin(),tmp.end());
		for(int i=0;i<tmp.size()-1;i++){
			cout<<tmp[i]<<",";
		} 
		cout<<tmp[tmp.size()-1]<<endl;
		
	}
}; 
map<string ,stu> stus;
int main(){
	//freopen("input.txt","r",stdin);
	order['B']=0;
	order['S']=1;
	order['M']=2;
	int n;
	cin >> n;
	for(int i=0;i<n;i++){
		string id,sport;
		int start,end;
		cin>>id>>sport>>start>>end;
		double h = (end%100-start%100)/3600.0+((end/100)%100-(start/100)%100)/60.0+((end/10000-start/10000));
		stus[id].total+=h;
		stus[id].id=id;
		stus[id].sports.insert(sport);
	}
	vector<stu> vstus;
	for(auto &a:stus){
		vstus.push_back(a.second);
	}
	sort(vstus.begin(),vstus.end());
	for(auto &s:vstus){
		s.out();
	}
	
}