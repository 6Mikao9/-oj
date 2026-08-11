// 2006年第2题：学生成绩排序
#include <bits/stdc++.h>
using namespace std;

struct Student {
    string name;
    int score;
    int index;  // 记录输入顺序，用于稳定排序
};

bool compare(const Student& a, const Student& b) {
    if (a.score != b.score) {
        return a.score > b.score;  // 成绩高的在前
    }
    return a.index < b.index;  // 成绩相同，先输入的在前
}

int main() {
    int n;
    cin >> n;
    
    vector<Student> students;
    
    for (int i = 0; i < n; i++) {
        Student s;
        cin >> s.name >> s.score;
        s.index = i;
        students.push_back(s);
    }
    
    // 排序
    sort(students.begin(), students.end(), compare);
    
    // 输出
    for (const auto& s : students) {
        cout << s.name << " " << s.score << endl;
    }
    
    return 0;
}
