#include<bits/stdc++.h>
using namespace std;
int a[10][10];
int b[10][10];
int t1[10][10];
int t2[10][10];
int t3[10][10];
int n;
void rotate(int r[][10],int t[][10]){
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            t[j][n-1-i]=r[i][j];
        }
    }
}
bool compare(int a[][10],int b[][10]){
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(a[i][j]!=b[i][j]){
                return false;
            }
        }
    }
    return true;
}
int main(){
    cin >> n;
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin >> a[i][j];
        }
    }
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin >> b[i][j];
        }
    }
    if(compare(a,b)){
        cout << 0 << endl;
        return 0;
    }
    rotate(a,t1);
    if(compare(t1,b)){
        cout << 90 << endl;
        return 0;
    }
    rotate(t1,t2);
    if(compare(t2,b)){
        cout << 180 << endl;
        return 0;
    }
    rotate(t2,t3);
    if(compare(t3,b)){
        cout << 270 << endl;
        return 0;
    }
    cout<<-1;
    return 0;
}