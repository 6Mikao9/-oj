#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 300

// 将引号内的字符替换为#
void replaceQuota(char buf[]) {
    int len = strlen(buf);
    int inQuota = 0;
    for (int i = 0; i < len; i++) {
        if (buf[i] == '"') {
            inQuota = !inQuota;
        } else if (inQuota) {
            buf[i] = '#';
        }
    }
}

// 检查从位置pos开始是否是关键字（考虑单词边界）
int isKeywordAt(char input[], int pos, const char *keyword) {
    int len = strlen(keyword);
    // 检查是否匹配关键字
    if (strncmp(&input[pos], keyword, len) != 0) {
        return 0;
    }
    // 检查前面是否是单词字符（如果是，则这是变量名的一部分，不算独立关键字）
    if (pos > 0) {
        char prev = input[pos - 1];
        if ((prev >= 'a' && prev <= 'z') || (prev >= 'A' && prev <= 'Z') || (prev >= '0' && prev <= '9') || prev == '_') {
            return 0;
        }
    }
    // 检查后面是否是单词字符
    char next = input[pos + len];
    if ((next >= 'a' && next <= 'z') || (next >= 'A' && next <= 'Z') || (next >= '0' && next <= '9') || next == '_') {
        return 0;
    }
    return 1;
}

int main() {
    char input[MAX_LEN];
    
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 0;
    }
    
    input[strcspn(input, "\n")] = '\0';
    replaceQuota(input);
    
    int len = strlen(input);
    for (int i = 0; i < len; i++) {
        if (isKeywordAt(input, i, "if")) {
            printf("if:%d\n", i);
        } else if (isKeywordAt(input, i, "while")) {
            printf("while:%d\n", i);
        } else if (isKeywordAt(input, i, "for")) {
            printf("for:%d\n", i);
        }
    }
    
    return 0;
}
