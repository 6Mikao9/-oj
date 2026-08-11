#include <bits/stdc++.h>
using namespace std;

// 多项式节点结构
typedef struct PolyNode {
    int coef;       // 系数
    int expn;       // 指数
    PolyNode *next; // 下一个节点
} PolyNode, *PolyList;

// 创建多项式（按指数降序）
PolyList createPoly(int n) {
    PolyList head = new PolyNode;
    head->next = NULL;
    PolyNode *tail = head;
    
    for (int i = 0; i < n; i++) {
        int coef, expn;
        scanf("%d %d", &coef, &expn);
        
        PolyNode *node = new PolyNode;
        node->coef = coef;
        node->expn = expn;
        node->next = NULL;
        
        tail->next = node;
        tail = node;
    }
    return head;
}

// 多项式相加：pa = pa + pb
void addPoly(PolyList pa, PolyList pb) {
    PolyNode *p = pa->next;
    PolyNode *q = pb->next;
    PolyNode *pre = pa;
    
    while (p && q) {
        if (p->expn > q->expn) {  // p指数大，保留p
            pre = p;
            p = p->next;
        } else if (p->expn < q->expn) {  // q指数大，插入q
            PolyNode *node = new PolyNode;
            node->coef = q->coef;
            node->expn = q->expn;
            node->next = p;
            pre->next = node;
            pre = node;
            q = q->next;
        } else {  // 指数相等，系数相加
            p->coef += q->coef;
            if (p->coef == 0) {  // 系数为0，删除该节点
                pre->next = p->next;
                delete p;
                p = pre->next;
            } else {
                pre = p;
                p = p->next;
            }
            q = q->next;
        }
    }
    
    // 处理pb剩余节点
    while (q) {
        PolyNode *node = new PolyNode;
        node->coef = q->coef;
        node->expn = q->expn;
        node->next = NULL;
        pre->next = node;
        pre = node;
        q = q->next;
    }
}

// 输出多项式
void printPoly(PolyList head) {
    PolyNode *p = head->next;
    bool first = true;
    bool hasOutput = false;
    
    while (p) {
        if (p->coef == 0) {
            p = p->next;
            continue;
        }
        
        if (!first) printf("+");
        
        // 系数
        if (p->coef != 1 && p->coef != -1) {
            printf("%d", p->coef);
        } else if (p->coef == -1) {
            printf("-");
        }
        // 系数为1或-1时，如果指数为0要输出1或-1
        if (p->expn == 0 && (p->coef == 1 || p->coef == -1)) {
            printf("1");
        }
        
        // 指数部分
        if (p->expn > 0) {
            printf("x");
            if (p->expn > 1) {
                printf("^%d", p->expn);
            }
        }
        
        first = false;
        hasOutput = true;
        p = p->next;
    }
    
    if (!hasOutput) {
        printf("0");
    }
    printf("\n");
}

int main() {
    int n, m;
    
    // 读第一个多项式
    scanf("%d", &n);
    PolyList pa = createPoly(n);
    
    // 读第二个多项式
    scanf("%d", &m);
    PolyList pb = createPoly(m);
    
    // 相加
    addPoly(pa, pb);
    
    // 输出结果
    printPoly(pa);
    
    return 0;
}
