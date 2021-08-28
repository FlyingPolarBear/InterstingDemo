#include <iostream>
#include <vector>
#include <cmath>
#include <cstdio>
using namespace std;
int main()
{
    vector<double> x = {1, 2, 3, 4};
    vector<double> y = {6, 5, 7, 10};
    vector<double> y_ = {0, 0, 0, 0};
    double a = 0, b = 0;
    int epoch = 200;
    double lr = 0.1;
    int n = x.size();
    for (int i = 0; i < epoch; i++)
    {
        double grad_a = 0, grad_b = 0, loss = 0;
        printf("epoch %3d: ", i + 1);
        for (int j = 0; j < n; j++)
        {
            y_[j] = a * x[j] + b;
            grad_a += 2 * x[j] * (y[j] - y_[j]) / n;
            grad_b += 2 * (y[j] - y_[j]) / n;
            loss += pow(y[j] - y_[j], 2);
            printf("y%d=%.3lf ", j + 1, y_[j]);
        }
        printf(" loss: %.3lf\n", loss);
        a = a + lr * grad_a;
        b = b + lr * grad_b;
    }
    printf("y = a * x + b\n");
    printf("a = %.3lf, b = %.3lf", a, b);
    return 0;
}