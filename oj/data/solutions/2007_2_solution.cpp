#include<bits/stdc++.h>
using namespace std;
int main(){
string s1;
string s2;
string t="";
string res="";
cin>>s1;
cin>>s2;
int len1=s1.length();

int len2=s2.length();
int pt1=0,pt2=0,i=0;
while(pt1<s1.length()&&pt2<s2.length()){
if(s1[pt1]<s2[pt2]){
t=t+s1[pt1++];
}else{
t=t+s2[pt2++];
}
}
while(pt1<s1.length()){
    t=t+s1[pt1++];
}
while(pt2<s2.length()){
    t=t+s2[pt2++];
}
int j=0;
for(i=0;i<t.length();i++){
    if(i==0){
        res+=t[i];
        continue;
    }else if(t[i]==res[res.length()-1]){
        continue;
    }else{
        res+=t[i];
    }
}
cout<<res;
return 0;
}