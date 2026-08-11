#include<bits/stdc++.h>
using namespace std;
int main(){
int ct1=0,ct2=0,ct3=0;
while(1){
char c=getchar();
if(c==' '){
ct1++;
}else if(c=='\n'){
ct2++;
}else if(c=='\t'){
ct3++;
}else if(c==-1){
break;
}
}
cout<<ct1<<','<<ct2<<','<<ct3;
return 0;
}