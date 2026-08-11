#include <bits/stdc++.h>
using namespace std;

map<char, double> variables;
string expression;
size_t pos;

double parseExpression();

double parseFactor() {
    if (expression[pos] == '(') {
        pos++;
        double result = parseExpression();
        pos++;
        return result;
    } else if (isdigit(expression[pos])) {
        double num = 0;
        while (pos < expression.length() && isdigit(expression[pos])) {
            num = num * 10 + (expression[pos] - '0');
            pos++;
        }
        return num;
    } else if (isalpha(expression[pos])) {
        char var = expression[pos];
        pos++;
        return variables[var];
    }
    return 0;
}

double parseTerm() {
    double result = parseFactor();
    while (pos < expression.length() && (expression[pos] == '*' || expression[pos] == '/')) {
        char op = expression[pos];
        pos++;
        double right = parseFactor();
        if (op == '*') {
            result *= right;
        } else {
            result /= right;
        }
    }
    return result;
}

double parseExpression() {
    double result = parseTerm();
    while (pos < expression.length() && (expression[pos] == '+' || expression[pos] == '-')) {
        char op = expression[pos];
        pos++;
        double right = parseTerm();
        if (op == '+') {
            result += right;
        } else {
            result -= right;
        }
    }
    return result;
}

int main() {
    string line;
    
    while (getline(cin, line)) {
        if (line == "exit") {
            break;
        } else if (line.find("read") == 0) {
            vector<char> vars;
            for (size_t i = 5; i < line.length(); i++) {
                if (isalpha(line[i])) {
                    vars.push_back(line[i]);
                }
            }
            
            // 读取一行，包含所有值（空格分隔）
            string values_line;
            getline(cin, values_line);
            istringstream iss(values_line);
            
            for (char var : vars) {
                double val;
                iss >> val;
                variables[var] = val;
            }
        } else if (line.find("print") == 0) {
            vector<char> vars;
            for (size_t i = 6; i < line.length(); i++) {
                if (isalpha(line[i])) {
                    vars.push_back(line[i]);
                }
            }
            
            for (size_t i = 0; i < vars.size(); i++) {
                cout << fixed << setprecision(2) << variables[vars[i]];
                if (i != vars.size() - 1) {
                    cout << " ";
                }
            }
            cout << endl;
        } else if (line.find('=') != string::npos) {
            char var = line[0];
            expression = line.substr(2);
            pos = 0;
            double result = parseExpression();
            variables[var] = result;
        }
    }
    
    return 0;
}
