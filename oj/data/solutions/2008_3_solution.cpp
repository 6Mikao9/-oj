#include<bits/stdc++.h>
using namespace std;
struct node{
    unordered_set<char> s;
    node* next;
};

// bool compare(char a,node * b){
//     for(auto it=b->s.begin();it!=b->s.end();it++){
        
//        if(isalpha(*it)){
//            if(a==toupper(*it)) return true;
//            if(a==tolower(*it)) return true;
//        } else{
//            if(a==*it) return true;
//        }
//     }
//     return false;
// }

bool compare(char a, node * b){
    for(char c : b->s){
        if(tolower(a) == tolower(c)) return true;  // 都转小写再比
    }
    return false;
}



int main(){
    int n;
    cin>>n;
    node* head = new node();
    vector<string> v(n);
    for(int i=0;i<n;i++){
        cin>>v[i];
    }
    string  pa;
    cin>>pa;
    node * p= head;
    for(int i=0;i<pa.length();i++){
        node * newnode= new node();
        p->next=newnode;
        p=newnode;
        p->next=NULL;
        if(pa[i]!='['){
            p->s.insert(pa[i]);
        }else{
            if(pa[i+2]=='-'){
                for(char c=pa[i+1];c<=pa[i+3];c++){
                    p->s.insert(c);
                }
                i+=4;
            }else{
                i++;
                for(;pa[i]!=']';i++){
                    p->s.insert(pa[i]);
                }
            }
        }
    }
    int notmatch=1;
    for(int i=0;i<n;i++){
        string t=v[i];
        node * p=head->next;
        int flag=1;
        for(int j=0;j<t.length();j++){
            if(p==NULL){
                flag=0;
                break;
            }
            if(!compare(t[j],p)){
                flag=0;
                break;
            }
            p=p->next;
        }
        if(flag&&p==NULL){
            notmatch=0;
            cout<<i+1<<" "<<v[i]<<endl;
        }
    }
    if(notmatch){
        cout<<"No match"<<endl;
    }
    return 0;
}