#include <bits/stdc++.h>
using namespace std;

struct Record {
    string type;
    string id;
    long long amount = 0;
    long long sales = 0;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    map<pair<string, string>, Record> agg;
    for (int i = 0; i < n; ++i) {
        string type, id;
        long long amount, price;
        cin >> type >> id >> amount >> price;

        auto key = make_pair(type, id);
        if (!agg.count(key)) {
            agg[key] = {type, id, 0, 0};
        }
        agg[key].amount += amount;
        agg[key].sales += amount * price;
    }

    vector<Record> out;
    out.reserve(agg.size());
    for (const auto &kv : agg) out.push_back(kv.second);

    sort(out.begin(), out.end(), [](const Record &a, const Record &b) {
        if (a.sales != b.sales) return a.sales > b.sales;
        if (a.type != b.type) return a.type < b.type;
        return a.id < b.id;
    });

    for (const auto &r : out) {
        cout << r.type << ' ' << r.id << ' ' << r.amount << ' ' << r.sales << "\n";
    }

    return 0;
}
