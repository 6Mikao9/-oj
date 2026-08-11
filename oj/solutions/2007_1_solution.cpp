#include <bits/stdc++.h>
using namespace std;

int main() {
    int space_count = 0, enter_count = 0, tab_count = 0;
    char ch;
    
    // 读取字符直到EOF
    while ((ch = getchar()) != EOF) {
        if (ch == ' ') {
            space_count++;
        } else if (ch == '\n') {
            enter_count++;
        } else if (ch == '\t') {
            tab_count++;
        }
    }
    
    printf("%d,%d,%d\n", space_count, enter_count, tab_count);
    return 0;
}
