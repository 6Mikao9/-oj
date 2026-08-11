#include <bits/stdc++.h>
using namespace std;

class Parser {
public:
    explicit Parser(string s) {
        for (char c : s) {
            if (!isspace(static_cast<unsigned char>(c))) {
                expr.push_back(c);
            }
        }
    }

    double parse() {
        pos = 0;
        return parseExpr();
    }

private:
    string expr;
    size_t pos = 0;

    double parseExpr() {
        double value = parseTerm();
        while (pos < expr.size() && (expr[pos] == '+' || expr[pos] == '-')) {
            char op = expr[pos++];
            double rhs = parseTerm();
            if (op == '+') value += rhs;
            else value -= rhs;
        }
        return value;
    }

    double parseTerm() {
        double value = parseFactor();
        while (pos < expr.size() && (expr[pos] == '*' || expr[pos] == '/')) {
            char op = expr[pos++];
            double rhs = parseFactor();
            if (op == '*') value *= rhs;
            else value /= rhs;
        }
        return value;
    }

    double parseFactor() {
        if (expr[pos] == '(') {
            ++pos;
            double value = parseExpr();
            ++pos;  // consume ')'
            return value;
        }

        long long value = 0;
        while (pos < expr.size() && isdigit(static_cast<unsigned char>(expr[pos]))) {
            value = value * 10 + (expr[pos] - '0');
            ++pos;
        }
        return static_cast<double>(value);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    Parser parser(line);
    double ans = parser.parse();
    cout << fixed << setprecision(2) << ans << "\n";
    return 0;
}
