#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define INVALID -99999
#define LEN 200

char name[LEN][LEN];
int num[LEN];
int cur_Index = 0;
char TypeContent[LEN];
int TypeContentLen = 0;

void getTypeContent(char enumStr[], int len) {
    int i = 0, pos = 0;
    while (i < len) {
        if (enumStr[i] == '{') {
            i++;
            while (i < len && enumStr[i] != '}') {
                TypeContent[pos++] = enumStr[i];
                i++;
            }
            TypeContent[pos] = '\0';
            TypeContentLen = pos;
            break;
        }
        i++;
    }
}

void skipSpace(char str[], int *pos) {
    while (*pos < TypeContentLen && (str[*pos] == ' ' || str[*pos] == '\t' || str[*pos] == '\n')) {
        (*pos)++;
    }
}

void parseItem(char str[], int *pos) {
    skipSpace(str, pos);
    if (*pos >= TypeContentLen) return;
    
    int i = 0;
    while (*pos < TypeContentLen && (isalpha(str[*pos]) || isdigit(str[*pos]) || str[*pos] == '_')) {
        name[cur_Index][i++] = str[*pos];
        (*pos)++;
    }
    name[cur_Index][i] = '\0';
    
    if (i == 0) return;
    
    num[cur_Index] = INVALID;
    
    skipSpace(str, pos);
    if (*pos < TypeContentLen && str[*pos] == '=') {
        (*pos)++;
        skipSpace(str, pos);
        
        char *endptr;
        num[cur_Index] = (int)strtol(&str[*pos], &endptr, 10);
        
        *pos += (int)(endptr - &str[*pos]);
    }
    
    skipSpace(str, pos);
    if (*pos < TypeContentLen && str[*pos] == ',') {
        (*pos)++;
    }
    
    cur_Index++;
}

void parseAllItems() {
    int pos = 0;
    while (pos < TypeContentLen) {
        int old_cur_Index = cur_Index;
        parseItem(TypeContent, &pos);
        if (cur_Index == old_cur_Index) break;
    }
}

void printResult() {
    int last_val = -1;
    
    for (int i = 0; i < cur_Index; i++) {
        int current_val;
        
        if (num[i] != INVALID) {
            current_val = num[i];
        } else {
            current_val = last_val + 1;
        }
        
        last_val = current_val;
        
        printf("%s %d\n", name[i], current_val);
    }
}

int main() {
    char enumStr[LEN * 2];
    
    if (fgets(enumStr, sizeof(enumStr), stdin) == NULL) {
        return EXIT_FAILURE;
    }
    
    int len = strlen(enumStr);
    if (len > 0 && enumStr[len - 1] == '\n') {
        enumStr[len - 1] = '\0';
        len--;
    }
    
    getTypeContent(enumStr, len);
    parseAllItems();
    printResult();
    
    return 0;
}
