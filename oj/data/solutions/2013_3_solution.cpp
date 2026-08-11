#include<bits/stdc++.h>
using namespace std;
void prt(string c,int exp){
	while(c.size()!=1&&c.back()=='0') c.pop_back();
	if(c.size()==1){
		cout<<c<<"e"<<exp;
	}else{
		c.insert(1,".");
		cout<<c<<"e"<<exp;
	}
}
int main(){
	string n;
	cin >> n;
	int exp=0;int ppos;
	if((ppos=n.find("."))==string::npos){
		exp=n.size()-1;
		prt(n,exp);
	}else{
		string a=n.substr(0,ppos);
		string b=n.substr(ppos+1);
		if(a=="0"){
			int i;
			for(i=0;i<b.size();i++){
				if(b[i]!='0')break;
			}
			exp=-i-1;
			b=b.substr(i);
			prt(b,exp);
		}else{
			exp=a.size()-1;
			prt(a+b,exp);
		}
	}
}