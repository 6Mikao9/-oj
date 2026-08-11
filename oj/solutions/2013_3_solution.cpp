#include <stdio.h>
#include <string.h>

#define MAX_LEN 205

int main() {
    char s[MAX_LEN];
    if (scanf("%s", s) != 1) return 1;
    
    int len = strlen(s);
    int first_digit = -1;  // 第一个非零数字的位置
    int dot_pos = -1;      // 小数点位置
    
    for (int i = 0; i < len; i++) {
        if (s[i] == '.') {
            dot_pos = i;
        } else if (first_digit == -1 && s[i] != '0') {
            first_digit = i;
        }
    }
    
    // 如果没有非零数字，输出0
    if (first_digit == -1) {
        printf("0e0\n");
        return 0;
    }
    
    // 收集所有有效数字（从first_digit开始，跳过小数点）
    char digits[MAX_LEN];
    int digit_count = 0;
    for (int i = first_digit; i < len; i++) {
        if (s[i] != '.') {
            digits[digit_count++] = s[i];
        }
    }
    
    // 计算指数E（基于原始数字，不去尾随零）
    int E = 0;
    if (dot_pos == -1) {
        // 整数：E = 原始数字位数 - 1
        E = digit_count - 1;
    } else if (first_digit < dot_pos) {
        // 小数点在非零数字之后：如123.456
        E = dot_pos - first_digit - 1;
    } else {
        // 小数点在非零数字之前：如0.0002
        E = dot_pos - first_digit;
    }
    
    // 去除尾随零
    while (digit_count > 1 && digits[digit_count - 1] == '0') {
        digit_count--;
    }
    
    // 输出第一个有效数字
    printf("%c", digits[0]);
    
    // 如果还有其他有效数字，输出小数点和剩余数字
    if (digit_count > 1) {
        printf(".");
        for (int i = 1; i < digit_count; i++) {
            printf("%c", digits[i]);
        }
    }
    
    printf("e%d\n", E);
    
    return 0;
}
