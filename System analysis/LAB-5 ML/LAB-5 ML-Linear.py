# мажорирующая функция (1 - M)^2
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, simplify, diff


def load_data(path):
    with open(path) as file:
        x = [int(n) for n in file.readline().rsplit()]
        y = [int(n) for n in file.readline().rsplit()]
    return x, y


def calculate(x, y):
    w1 = symbols("w1")
    w0 = symbols("w0")
    m = [y_i * (x_i * w1 + w0) for x_i, y_i in zip(x, y)]

    print("Отступы объектов равны:")
    for m_no, m_i in enumerate(m):
        print("M" + str(m_no) + ":", m_i)

    l = sum([pow(1 - m_i, 2) for m_i in m])
    print("Необходимо минимизировать выражение:", l)
    solution = solve([diff(l, w0), diff(l, w1)])
    print("Решение, полученное через приравнивание частных производных к нулю:", solution)

    x_pass = -solution[w0] / solution[w1]
    if solution[w1] > 0:
        print("Таким образом, если x больше", x_pass, "то объект из класса 1; иначе из класса -1")
    else:
        print("Таким образом, если x меньше", x_pass, "то объект из класса 1; иначе из класса -1")

    return x_pass


def show_plot(x, y, x_pass):
    for i in range(len(x)):
        if y[i] == 1:
            plt.scatter([x[i]], [0], color='green', s=[100])
        else:
            plt.scatter([x[i]], [0], color='red', s=[100])

    plt.axvline(x=x_pass)
    # plt.plot(x_vals, y_vars, color='red')
    plt.show()



x_data, y_data = load_data("LAB-5_2_Data.txt")
print(x_data)
print(y_data)
p = calculate(x_data, y_data)
show_plot(x_data, y_data, p)

