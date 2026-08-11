#include <bits/stdc++.h>
using namespace std;

struct Result {
    string small_str;
    string big_str;
    int distance;
};

int calculateDistance(const string &a, const string &b) {
    int dist = 0;
    for (size_t i = 0; i < a.length(); i++) {
        if (a[i] != b[i]) dist++;
    }
    return dist;
}

bool compare(const Result &a, const Result &b) {
    if (a.distance != b.distance) return a.distance < b.distance;
    if (a.small_str != b.small_str) return a.small_str < b.small_str;
    return a.big_str < b.big_str;
}

int main() {
    int n;
    cin >> n;
    
    vector<string> strs(n);
    for (int i = 0; i < n; i++) {
        cin >> strs[i];
    }
    
    vector<Result> results;
    
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            Result res;
            if (strs[i] < strs[j]) {
                res.small_str = strs[i];
                res.big_str = strs[j];
            } else {
                res.small_str = strs[j];
                res.big_str = strs[i];
            }
            res.distance = calculateDistance(strs[i], strs[j]);
            results.push_back(res);
        }
    }
    
    sort(results.begin(), results.end(), compare);

    int count = min(6, (int)results.size());

    for (int i = 0; i < count; i++) {
        cout << results[i].small_str << " " << results[i].big_str << " " << results[i].distance << endl;
    }
    
    return 0;
}
