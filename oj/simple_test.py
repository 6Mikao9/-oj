#!/usr/bin/env python3
"""
Simple test - directly run OJ system
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oj_system import LocalOJ

def main():
    print("="*60)
    print("Local OJ - Simple Test")
    print("="*60)
    print()
    
    oj = LocalOJ()
    
    # Check problem exists
    problem_dir = oj.problems_dir / "tamworth_two"
    testcase_dir = problem_dir / "testcases"
    
    print(f"Checking problem directory: {problem_dir}")
    print(f"  Exists: {problem_dir.exists()}")
    
    print(f"Checking testcases directory: {testcase_dir}")
    print(f"  Exists: {testcase_dir.exists()}")
    
    # List test cases
    if testcase_dir.exists():
        test_files = list(testcase_dir.glob("*.in"))
        print(f"  Test case files: {len(test_files)}")
        for f in test_files:
            print(f"    - {f.name}")
    
    print()
    
    # Create a simple correct solution
    solution_code = r'''#include <bits/stdc++.h>
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
    
    # Save solution
    temp_file = oj.temp_dir / "solution.cpp"
    with open(temp_file, 'w') as f:
        f.write(solution_code)
    
    print(f"Created test solution: {temp_file}")
    print()
    
    # Judge
    print("Starting judge...")
    print("-"*60)
    results = oj.judge("tamworth_two", str(temp_file))
    
    # Cleanup
    if temp_file.exists():
        temp_file.unlink()
    
    print()
    print("="*60)
    print("Test completed!")
    print("="*60)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
