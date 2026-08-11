#!/usr/bin/env python3
"""
Quick test script - Demo OJ usage
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oj_system import LocalOJ

def test_with_sample():
    """Test with sample"""
    oj = LocalOJ()
    
    # Check if problem exists
    problem_dir = oj.problems_dir / "tamworth_two"
    if not problem_dir.exists():
        print("Problem not found!")
        return
    
    # Create test code
    test_code = '''#include <bits/stdc++.h>
using namespace std;

char grid[10][10];
int fx, fy, cx, cy;
int dirf = 0, dirc = 0;
int dr[] = {-1, 0, 1, 0};
int dc[] = {0, 1, 0, -1};

bool canMove(int r, int c) {
    return r >= 0 && r < 10 && c >= 0 && c < 10 && grid[r][c] != '*';
}

void move(int &r, int &c, int &dir) {
    int nr = r + dr[dir];
    int nc = c + dc[dir];
    if (canMove(nr, nc)) {
        r = nr;
        c = nc;
    } else {
        dir = (dir + 1) % 4;
    }
}

int main() {
    for (int i = 0; i < 10; i++) {
        string line;
        getline(cin, line);
        for (int j = 0; j < 10; j++) {
            grid[i][j] = line[j];
            if (grid[i][j] == 'F') {
                fx = i; fy = j;
                grid[i][j] = '.';
            } else if (grid[i][j] == 'C') {
                cx = i; cy = j;
                grid[i][j] = '.';
            }
        }
    }
    
    for (int t = 1; t <= 1000000; t++) {
        move(fx, fy, dirf);
        move(cx, cy, dirc);
        
        if (fx == cx && fy == cy) {
            cout << t << endl;
            return 0;
        }
    }
    
    cout << 0 << endl;
    return 0;
}
'''
    
    # Save test code
    temp_code = oj.temp_dir / "test_solution.cpp"
    with open(temp_code, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    print("="*60)
    print("Testing correct solution")
    print("="*60)
    results = oj.judge("tamworth_two", str(temp_code))
    
    # Cleanup
    if temp_code.exists():
        temp_code.unlink()

if __name__ == "__main__":
    test_with_sample()
