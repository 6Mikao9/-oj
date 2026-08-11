#include<bits/stdc++.h>
using namespace std;
set<string> ss;
int main() {
	char c;
	string s="";
	while((c=getchar())!=EOF){
		if(!isalpha(c)){
			if(s.empty())continue;
			ss.insert(s);
			s="";	
		} else{
			s+=tolower(c);
		}
	} 
	
	for(auto a:ss){
		cout<<a<<endl;	
	}	
    return 0;
}