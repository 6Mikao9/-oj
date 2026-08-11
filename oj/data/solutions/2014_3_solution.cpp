#include<bits/stdc++.h>
using namespace std;
vector<string> parse(string s){
	vector<string> v;
	int f=1;
	string t="";

	for(char c: s){
		if(isalpha(c)){
			f=0;
			t+=c;
		}else if(!f){
			v.push_back(t);
			t="";
			f=1;
		}
	}
	if(!t.empty())v.push_back(t);
	return v;
}
string build(vector<string> v,int pos){
	string tmp="";
	string s="";
	for(auto a:v){
		s+=a+" ";
	}
	return tmp.append(pos-s.size(),' ')+s; 
} 
int main() {
	//freopen("input.txt","r",stdin) ;
	int p;char cc;
	cin>>p;
	string s;
	while(getline(cin,s)){
		if(s=="")continue;
		int m=s.find(":");
		string f=s.substr(0,m);
		string scd=s.substr(m+1);
		cout<<build(parse(f),p)<<": ";
		auto v=parse(scd);
		for(int i=0;i<v.size();i++){
			cout << v[i];
			cout<< (i==(v.size()-1)?"\n":" ");
		}
		s="";
	}

    return 0;
}