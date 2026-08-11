#include<bits/stdc++.h>
using namespace std;
int n[10]; 
 void init(){
 	n[0]=1;
 	for(int i=1;i<10;i++){
 		n[i]=n[i-1]*i;
	}
 }
 string build(string s,int sum){
 	string res=",";
 	for(int i=0;i<s[i];i++){
 		res=res+s[i]+(i==s.length()-1?"!=":"!+"); 
	 }
	 return res+to_string(sum)+"\n";
 }
int main() {
	init();
    string s;
    cin >> s;
    int x=stoi(s);
    int sum=0;
	for(int i=0;i<s.length();i++){
		sum+=n[s[i]-'0'];		
	}
	
	if(sum==x){
		cout<<s<<build(s,sum); 
		cout<<"Yes"; 
	}else{
		cout<<s<<build(s,sum); 
		cout<<"No";
	}
    return 0;
}