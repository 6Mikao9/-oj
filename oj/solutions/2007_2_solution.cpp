#include <bits/stdc++.h>
using namespace std;

int main() {
    char str0[200], str1[200], str[400];
    char ch;
    
    // 读第一个字符串
    int i = 0;
    while ((ch = getchar()) != '\n' && ch != EOF) {
        str0[i++] = ch;
    }
    str0[i] = '\0';
    
    // 读第二个字符串
    i = 0;
    while ((ch = getchar()) != '\n' && ch != EOF) {
        str1[i++] = ch;
    }
    str1[i] = '\0';
    
    // 归并合并（双指针）
    int j = 0, k = 0;
    i = 0;
    while (str0[i] != '\0' && str1[j] != '\0') {
        if (str0[i] < str1[j]) {
            // 去重：如果和结果串最后一个字符相同则跳过
            if (k > 0 && str0[i] == str[k-1]) {
                i++;
            } else {
                str[k++] = str0[i++];
            }
        } else if (str0[i] > str1[j]) {
            if (k > 0 && str1[j] == str[k-1]) {
                j++;
            } else {
                str[k++] = str1[j++];
            }
        } else {  // 相等
            if (k > 0 && str0[i] == str[k-1]) {
                i++;
                j++;
            } else {
                str[k++] = str0[i++];
                j++;
            }
        }
    }
    
    // 处理剩余字符
    while (str0[i] != '\0') {
        if (k > 0 && str0[i] == str[k-1]) {
            i++;
        } else {
            str[k++] = str0[i++];
        }
    }
    
    while (str1[j] != '\0') {
        if (k > 0 && str1[j] == str[k-1]) {
            j++;
        } else {
            str[k++] = str1[j++];
        }
    }
    
    str[k] = '\0';
    
    // 输出结果
    printf("%s\n", str);
    
    return 0;
}
