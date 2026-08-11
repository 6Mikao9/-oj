#include<bits/stdc++.h>
using namespace std;
vector<string> split(string o,char sp){
	vector<string> res;
	string tmp;
	stringstream ss(o);
	while(getline(ss,tmp,sp)){
		res.push_back(tmp);
	}
	return res;
}

int main(){
	string s;
getline(cin,s);
	auto ws=split(s,',');
	for(string w:ws){
		
		auto tokens=split(w,' ');
		string lst=tokens.back();
		int pos;
		if((pos=lst.find("["))!=string::npos){
			lst=lst.substr(0,pos);
		}
		
		if((pos=lst.rfind("*"))!=string::npos){
			lst=lst.substr(pos+1);
		}
		cout<<lst<<endl;
	}
}