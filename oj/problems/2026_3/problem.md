# 2026_3: C声明中的变量名提取

## 问题描述
给定一行合法的 C 风格变量声明语句（不含分号）。
声明中可能包含 `const`、`unsigned`、`long` 等类型修饰，
也可能有 `*` 和数组下标 `[]`。
请按声明中出现顺序输出所有变量名。

## 输入格式
一行字符串，长度不超过 300。

## 输出格式
每行输出一个变量名。

## 样例输入
```text
const unsigned long int *ptr, arr[10], var_name, **double_ptr
```

## 样例输出
```text
ptr
arr
var_name
double_ptr
```
