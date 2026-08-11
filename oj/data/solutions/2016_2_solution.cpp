#include<bits/stdc++.h>
using namespace std;
int main() {
	char c;
	int flag=0;
	string s="";
	int n=0; 
	while((c=getchar())!=EOF){
		if(c=='{'){
			flag=1;
			continue; 
		}
		if(flag){
			if(c==','||c=='}'){
				int pos=s.find("=");
				if(pos==-1){
					cout<<s<<" "<<n++<<endl;
				}else{
					string v=s.substr(pos+1);
					n=stoi(v);
					cout<< s.substr(0,pos)<<" "<<n++<<endl;
					//if(c=='}')break;
				}
				s="";
			}else{
				s+=c;
			} 
			
		} 
	} 
		
	 
		
    return 0;
}