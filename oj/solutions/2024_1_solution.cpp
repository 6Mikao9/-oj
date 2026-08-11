#include <bits/stdc++.h>
using namespace std;

struct StudentOut {
    string id;
    long long totalSeconds;
    string sports;
};

static int toSeconds(const string &t) {
    int hh = stoi(t.substr(0, 2));
    int mm = stoi(t.substr(2, 2));
    int ss = stoi(t.substr(4, 2));
    return hh * 3600 + mm * 60 + ss;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    map<string, long long> total;
    map<string, set<string>> sportsSet;

    for (int i = 0; i < n; ++i) {
        string id, sport, start, end;
        cin >> id >> sport >> start >> end;
        long long d = toSeconds(end) - toSeconds(start);
        total[id] += d;
        sportsSet[id].insert(sport);
    }

    map<char, vector<StudentOut>> groups;
    for (const auto &kv : total) {
        const string &id = kv.first;
        long long sec = kv.second;

        string sports;
        bool first = true;
        for (const string &sp : sportsSet[id]) {
            if (!first) sports += ",";
            sports += sp;
            first = false;
        }

        groups[id[0]].push_back({id, sec, sports});
    }

    for (char cat : string("BSM")) {
        auto it = groups.find(cat);
        if (it == groups.end()) continue;

        auto &v = it->second;
        sort(v.begin(), v.end(), [](const StudentOut &a, const StudentOut &b) {
            if (a.totalSeconds != b.totalSeconds) return a.totalSeconds < b.totalSeconds;
            return a.id < b.id;
        });

        for (const auto &st : v) {
            double hours = static_cast<double>(st.totalSeconds) / 3600.0;
            cout << st.id << ' ' << fixed << setprecision(2) << hours << ' ' << st.sports << "\n";
        }
    }

    return 0;
}
