#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_LINES 50
#define MAX_LINE_LEN 101

char ch[MAX_LINES][MAX_LINE_LEN];

void cleanStr(char *src, char *dest) {
    int i = 0, j = 0;
    
    // 跳过开头的空格和制表符
    while (src[i] != '\0' && (src[i] == ' ' || src[i] == '\t')) {
        i++;
    }
    
    while (src[i] != '\0') {
        if (src[i] == ' ' || src[i] == '\t') {
            if (j > 0 && dest[j-1] != ' ') {
                dest[j++] = ' ';
            }
        } else {
            dest[j++] = src[i];
        }
        i++;
    }
    
    // 去除末尾的空格
    if (j > 0 && dest[j-1] == ' ') {
        dest[j-1] = '\0';
    } else {
        dest[j] = '\0';
    }
}

void formatLine(char *line, int colonPos, char *formatted) {
    char pos[MAX_LINE_LEN] = {0}, name[MAX_LINE_LEN] = {0};
    
    char *colon = strchr(line, ':');
    
    if (!colon) {
        strcpy(formatted, line);
        return;
    }
    
    int posLen = colon - line;
    strncpy(pos, line, posLen);
    pos[posLen] = '\0';
    strcpy(name, colon + 1);
    
    char cleanPos[MAX_LINE_LEN], cleanName[MAX_LINE_LEN];
    cleanStr(pos, cleanPos);
    cleanStr(name, cleanName);
    
    int posLenClean = strlen(cleanPos);
    int spaceLeft = colonPos - 1 - posLenClean;
    
    memset(formatted, 0, MAX_LINE_LEN * 2);
    
    // 填充前导空格
    for (int i = 0; i < spaceLeft && i < MAX_LINE_LEN * 2 - 1; i++) {
        formatted[i] = ' ';
    }
    
    if (spaceLeft < MAX_LINE_LEN * 2 - 1) {
        strcat(formatted, cleanPos);
        strcat(formatted, " : ");
        strcat(formatted, cleanName);
    }
}

int main() {
    int n, m = 0;
    
    if (scanf("%d", &n) != 1) return EXIT_FAILURE;
    
    getchar(); //  consume newline
    
    while (m < MAX_LINES && fgets(ch[m], MAX_LINE_LEN, stdin) != NULL) {
        // 去除换行符
        ch[m][strcspn(ch[m], "\n")] = '\0';
        
        // 空行结束
        if (strlen(ch[m]) == 0) break;
        
        m++;
    }
    
    char formatted[MAX_LINES][MAX_LINE_LEN * 2];
    for (int i = 0; i < m; i++) {
        formatLine(ch[i], n, formatted[i]);
    }
    
    for (int i = 0; i < m; i++) {
        printf("%s\n", formatted[i]);
    }
    
    return 0;
}
