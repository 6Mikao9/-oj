#include <stdio.h>
#include <string.h>

void reverseStr(char *src, char *dest) {
    int len = strlen(src);
    for (int i = 0; i < len; i++) {
        dest[i] = src[len - 1 - i];
    }
    dest[len] = '\0';
}

int strToInt(char *str) {
    int num = 0;
    int len = strlen(str);
    for (int i = 0; i < len; i++) {
        num = num * 10 + (str[i] - '0');
    }
    return num;
}

int main() {
    char numStr[20];
    char revStr[20];
    
    scanf("%s", numStr);
    
    reverseStr(numStr, revStr);
    
    int num = strToInt(numStr);
    int revNum = strToInt(revStr);
    
    if (revNum % num == 0) {
        int k = revNum / num;
        printf("%s*%d=%s\n", numStr, k, revStr);
    } else {
        printf("%s %s\n", numStr, revStr);
    }
    
    return 0;
}
