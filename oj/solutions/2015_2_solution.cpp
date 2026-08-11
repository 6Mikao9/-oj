#include <stdio.h>
#include <stdlib.h>

#define MAX_WIN 100

typedef struct {
    int id;
    int x1, y1, x2, y2;
    int priority;
} Window;

int isInWindow(Window win, int x, int y) {
    int minX = (win.x1 < win.x2) ? win.x1 : win.x2;
    int maxX = (win.x1 > win.x2) ? win.x1 : win.x2;
    int minY = (win.y1 < win.y2) ? win.y1 : win.y2;
    int maxY = (win.y1 > win.y2) ? win.y1 : win.y2;
    
    return (x >= minX && x <= maxX) && (y >= minY && y <= maxY);
}

void sortWindows(Window wins[], int n) {
    int i, j;
    Window temp;
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (wins[j].priority < wins[j + 1].priority) {
                temp = wins[j];
                wins[j] = wins[j + 1];
                wins[j + 1] = temp;
            }
        }
    }
}

int main() {
    int n, m, i, j;
    Window wins[MAX_WIN];
    int clickX, clickY;
    
    if (scanf("%d", &n) != 1 || n < 1 || n > MAX_WIN) return EXIT_FAILURE;
    
    for (i = 0; i < n; i++) {
        if (scanf("%d %d %d %d %d", &wins[i].id, &wins[i].x1, &wins[i].y1, &wins[i].x2, &wins[i].y2) != 5)
            return EXIT_FAILURE;
        wins[i].priority = n - i;
    }
    
    if (scanf("%d", &m) != 1) return EXIT_FAILURE;
    
    for (i = 0; i < m; i++) {
        if (scanf("%d %d", &clickX, &clickY) != 2) return EXIT_FAILURE;
        
        sortWindows(wins, n);
        
        int maxPrio = 0;
        for (j = 0; j < n; j++) {
            if (wins[j].priority > maxPrio) maxPrio = wins[j].priority;
        }
        
        for (j = 0; j < n; j++) {
            if (isInWindow(wins[j], clickX, clickY)) {
                wins[j].priority = maxPrio + 1;
                break;
            }
        }
    }
    
    sortWindows(wins, n);
    
    for (i = 0; i < n; i++) {
        if (i > 0) printf(" ");
        printf("%d", wins[i].id);
    }
    printf("\n");
    
    return 0;
}
