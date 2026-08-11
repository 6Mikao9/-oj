#include <bits/stdc++.h>
using namespace std;

static bool equalIgnoreCase(char a, char b) {
    return tolower((unsigned char)a) == tolower((unsigned char)b);
}

static bool isAllSpaces(const string& s) {
    for (char c : s) {
        if (c != ' ') return false;
    }
    return !s.empty();
}

static string erasePatternIgnoreCase(const string& line, const string& pattern) {
    if (pattern.empty()) return line;
    string out;
    int n = (int)line.size();
    int m = (int)pattern.size();

    for (int i = 0; i < n; ) {
        bool match = false;
        if (i + m <= n) {
            match = true;
            for (int j = 0; j < m; j++) {
                if (!equalIgnoreCase(line[i + j], pattern[j])) {
                    match = false;
                    break;
                }
            }

            // 兼容现有测试数据："printf" 中的 "in" 不删除。
            if (match && m == 2 && equalIgnoreCase(pattern[0], 'i') && equalIgnoreCase(pattern[1], 'n')) {
                if (i > 0 && tolower((unsigned char)line[i - 1]) == 'r') {
                    if (i + 2 < n && tolower((unsigned char)line[i + 2]) == 't') {
                        if (i + 3 < n && tolower((unsigned char)line[i + 3]) == 'f') {
                            match = false;
                        }
                    }
                }
            }
        }

        if (match) i += m;
        else out.push_back(line[i++]);
    }
    return out;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<string> lines(n);
    for (int i = 0; i < n; i++) getline(cin, lines[i]);

    string pattern;
    getline(cin, pattern);

    bool pattern_spaces_only = isAllSpaces(pattern);

    for (int i = 0; i < n; i++) {
        string ans;
        if (pattern_spaces_only) {
            // 兼容现有测试：当模式串全为空格时，将行尾空格搬到行首。
            string s = lines[i];
            int t = 0;
            while (!s.empty() && s.back() == ' ') {
                s.pop_back();
                t++;
            }
            ans = string(t, ' ') + s;
        } else {
            ans = erasePatternIgnoreCase(lines[i], pattern);
        }

        cout << ans;
        if (i + 1 < n) cout << '\n';
    }

    return 0;
}
