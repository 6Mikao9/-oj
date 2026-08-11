#include <bits/stdc++.h>
using namespace std;

struct Log {
    string phone;
    string station;
    string login;
    string logout;
};

static bool overlapClosed(const Log &a, const Log &b) {
    return !(a.logout < b.login || a.login > b.logout);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<Log> logs(n);
    for (int i = 0; i < n; ++i) {
        cin >> logs[i].phone >> logs[i].station >> logs[i].login >> logs[i].logout;
    }

    string targetPhone;
    if (!(cin >> targetPhone)) return 0;

    vector<Log> targetLogs;
    for (const auto &lg : logs) {
        if (lg.phone == targetPhone) targetLogs.push_back(lg);
    }

    map<tuple<string, string, string, string>, Log> uniq;
    for (const auto &t : targetLogs) {
        for (const auto &lg : logs) {
            if (lg.phone == targetPhone) continue;
            if (lg.station != t.station) continue;
            if (!overlapClosed(lg, t)) continue;
            uniq[{lg.phone, lg.station, lg.login, lg.logout}] = lg;
        }
    }

    vector<Log> ans;
    ans.reserve(uniq.size());
    for (const auto &kv : uniq) ans.push_back(kv.second);

    sort(ans.begin(), ans.end(), [](const Log &a, const Log &b) {
        if (a.login != b.login) return a.login < b.login;
        if (a.phone != b.phone) return a.phone < b.phone;
        if (a.station != b.station) return a.station < b.station;
        return a.logout < b.logout;
    });

    for (const auto &lg : ans) {
        cout << lg.phone << ' ' << lg.station << ' ' << lg.login << ' ' << lg.logout << "\n";
    }

    return 0;
}
