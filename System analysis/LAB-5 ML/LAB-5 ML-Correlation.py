import math
import numpy as np
from scipy.stats import t
from sympy import symbols, Eq, solve

import matplotlib.pyplot as plt


def load_data(path):
    with open(path) as file:
        x = [int(n) for n in file.readline().rsplit()]
        y = [int(n) for n in file.readline().rsplit()]
    return x, y


def show_scatter_plot(x, y, coefs):
    plt.scatter(x, y)
    plt.grid(True)

    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vars = coefs.get(symbols('b')) + coefs.get(symbols('a')) * x_vals
    plt.plot(x_vals, y_vars, color='red')
    plt.legend(["Исходные данные", "Линия, представляющая уравнение регрессии y=ax+b"])
    plt.title("Диаграмма рассеивания")
    plt.show()


def get_correlation_coefficient(x, y):
    x2 = [pow(x_i, 2) for x_i in x]
    y2 = [pow(y_i, 2) for y_i in y]
    xy = [x[i] * y[i] for i in range(len(x))]
    up = sum(xy) - len(x) * sum(x) / len(x) * sum(y) / len(x)
    down = math.sqrt(sum(x2) - len(x) * pow(sum(x) / len(x), 2)) * math.sqrt(sum(y2) - len(y) * pow(sum(y) / len(y), 2))
    return up / down


def get_student_observ(c, n):
    return c * math.sqrt(n - 2) / math.sqrt(1 - pow(c, 2))


def get_student_real(alpha, d):
    return t.ppf(q=alpha, df=d)


def find_line(x, y):
    a = symbols('a')
    b = symbols('b')
    eq1 = a * sum([pow(x_i, 2) for x_i in x]) + b * sum(x) - sum([x[i] * y[i] for i in range(len(x))])
    eq2 = a * sum(x) + b * len(x) - sum(y)
    sol = solve([eq1, eq2], a, b)
    return sol


x_data, y_data = load_data("LAB-5_1_Data.txt")
corr = get_correlation_coefficient(x_data, y_data)
print("Коэффициент корреляции Пирсона:", corr)
s_corr = get_student_observ(corr, len(x_data))
print("Наблюдаемое значение критерия Стьюдента:", s_corr)

alpha = 0.05
s_real = get_student_real(alpha, len(x_data) - 2)
print("Табличное значение критерия Стьюдента для уровня значимости", alpha, "равно:", s_real)
if abs(s_corr) > abs(s_real):
    print("Так как наблюдаемое значение больше табличного, коэффициент корреляции статистически значим")

line_coefs = find_line(x_data, y_data)
print("Коэффициенты уравнения регрессии y = ax + b:", line_coefs)

show_scatter_plot(x_data, y_data, line_coefs)