#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_WORDS 5000
#define MAX_WORD_LEN 100
#define MAX_TEXT_LEN 1000000

char ch[MAX_TEXT_LEN];
char str[MAX_WORDS][MAX_WORD_LEN];

void Swap(char a[], char b[]) {
    char temp[MAX_WORD_LEN];
    strcpy(temp, a);
    strcpy(a, b);
    strcpy(b, temp);
}

int CompareTo(char a[], char b[]) {
    return strcmp(a, b);
}

int isPunctuation(char c) {
    return c == ',' || c == '.' || c == '?' || c == '!' || c == ';' || c == ':' ||
           c == '\'' || c == '"' || c == '(' || c == ')' || c == '[' || c == ']' ||
           c == '{' || c == '}' || c == '<' || c == '>' || c == ' ' || c == '\n' ||
           c == '\t' || c == '-' || c == '_' || c == '/' || c == '@' || c == '#' ||
           c == '$' || c == '%' || c == '&' || c == '*' || c == '+' || c == '=' ||
           c == '|' || c == '\\';
}

int main() {
    int i = 0, k = 0, j;
    int n, m;
    
    while ((ch[i] = getchar()) != EOF && i < MAX_TEXT_LEN - 1) {
        i++;
    }
    m = i;
    
    for (i = 0; i < m; i++) {
        if (isPunctuation(ch[i])) {
            continue;
        }
        
        if (k >= MAX_WORDS) break;
        
        j = 0;
        while (i < m && !isPunctuation(ch[i])) {
            if (j < MAX_WORD_LEN - 1) {
                str[k][j++] = tolower(ch[i]);
            }
            i++;
        }
        
        if (j > 0) {
            str[k][j] = '\0';
            k++;
        }
        
        i--;
    }
    n = k;
    
    // Selection Sort
    for (i = 0; i < n; i++) {
        int t = i;
        for (j = i + 1; j < n; j++) {
            if (CompareTo(str[t], str[j]) > 0) {
                t = j;
            }
        }
        if (t != i) {
            Swap(str[i], str[t]);
        }
    }
    
    if (n > 0) {
        printf("%s\n", str[0]);
        for (i = 1; i < n; i++) {
            if (CompareTo(str[i], str[i - 1]) != 0) {
                printf("%s\n", str[i]);
            }
        }
    }
    
    return 0;
}
