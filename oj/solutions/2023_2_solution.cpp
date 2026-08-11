#include <bits/stdc++.h>
using namespace std;

struct Action {
    int dir;
    long long steps;
};

static bool isOpposite(int a, int b) {
    return (a == 1 && b == 2) || (a == 2 && b == 1) ||
           (a == 3 && b == 4) || (a == 4 && b == 3);
}

static int oppositeDir(int d) {
    if (d == 1) return 2;
    if (d == 2) return 1;
    if (d == 3) return 4;
    return 3;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<Action> st;
    string token;
    while (cin >> token) {
        size_t pos = token.find('-');
        if (pos == string::npos) continue;

        int d = stoi(token.substr(0, pos));
        long long s = stoll(token.substr(pos + 1));
        if (d == 0 && s == 0) break;
        if (s == 0) continue;

        Action cur{d, s};

        if (st.empty()) {
            st.push_back(cur);
            continue;
        }

        if (st.back().dir == cur.dir) {
            st.back().steps += cur.steps;
            continue;
        }

        if (isOpposite(st.back().dir, cur.dir)) {
            if (cur.steps == st.back().steps) {
                st.pop_back();
            } else if (cur.steps > st.back().steps) {
                cur.steps -= st.back().steps;
                st.pop_back();
                st.push_back(cur);
            } else {
                st.back().steps -= cur.steps;
            }
            continue;
        }

        st.push_back(cur);
    }

    vector<Action> ans;
    for (int i = (int)st.size() - 1; i >= 0; --i) {
        Action back{oppositeDir(st[i].dir), st[i].steps};
        if (!ans.empty() && ans.back().dir == back.dir) {
            ans.back().steps += back.steps;
        } else {
            ans.push_back(back);
        }
    }

    if (ans.empty()) {
        cout << "0-0";
        return 0;
    }

    for (size_t i = 0; i < ans.size(); ++i) {
        cout << ans[i].dir << '-' << ans[i].steps;
        if (i + 1 != ans.size()) cout << ' ';
    }

    return 0;
}
