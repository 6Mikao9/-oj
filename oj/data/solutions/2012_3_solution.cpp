#include<bits/stdc++.h>
using namespace std;
bool judge(char c){
	return isdigit(c)||isalpha(c)||c=='_';
}
bool check(string s,string cmp,int i){
	if(judge(s[i-1])||judge(s[i+cmp.length()])){
		return false;
	}else{
		if(s.substr(i,cmp.length())==cmp)return true; 
		else return false;
	}
} 


int main(){
	string s;
	getline(cin,s);
	for(int i=0;i<s.length();i++){
		if(s[i]=='\"'){
			i++;
			while(s[i]!='\"') s[i++]='#';
		} 
	} 
	
	for(int i=0;i<s.length();i++){
		if(check(s,"if",i)){
			cout<<"if:"<<i<<endl;
			i+=1;
		}else if(check(s,"while",i)){
			cout<<"while:"<<i<<endl;
			i+=4;
		}else if(check(s,"for",i)){
			cout<<"for:"<<i<<endl;
			i+=2;
		}
	} 
	
	return 0;
}