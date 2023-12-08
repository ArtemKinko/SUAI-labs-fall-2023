import math
import matplotlib.pyplot as plt

import tabulate
from matplotlib import cm


# Вариант №8

# Дано непрерывное отображение Лоренца с эволюционными уравнениями и параметрами s, r, d:
# x*(t) = sy  - sx;
# y*(t) = -y + rx - xz
# z*(t) = -bz + xy

# 1. Построить зависимости x(t), y(t), z(t) в условиях:
# [x, y, z] = [1, -1, 10]
# s, r, b = 10, 28, 8/3
# 2. Построить фазовые портреты (x, y, z) для случаев п.1^0 с разной степенью точности вычисления:
# (2 или 15 знаков в мантиссе)

# 3. Привести примеры практического применения модели Лоренца
# 4. Дать определение устойчивой и неустойчивой динамической системы

def calculate_lorenz(x_start, y_start, z_start, s, r, b, iter_num, dt, precision):
    x = [x_start]
    y = [y_start]
    z = [z_start]
    current_x = x_start
    current_y = y_start
    current_z = z_start
    for _ in range(iter_num):
        x.append(round(current_x + (s * current_y - s * current_x) * dt, precision))
        y.append(round(current_y + (-current_y + r * current_x - current_x * current_z) * dt, precision))
        z.append(round(current_z + (-b * current_z + current_x * current_y) * dt, precision))
        current_x = x[-1]
        current_y = y[-1]
        current_z = z[-1]

    return x, y, z


def show_plots(x, y, z, iter_num):
    t = list(range(iter_num + 1))
    plt.plot(t, x)
    plt.title("График зависимости x(t)")
    plt.show()

    plt.plot(t, y)
    plt.title("График зависимости y(t)")
    plt.show()

    plt.plot(t, z)
    plt.title("График зависимости z(t)")
    plt.show()

    ax = plt.figure().add_subplot(projection='3d')

    ax.plot(x, y, z, lw=0.5)
    ax.set_xlabel("Ось X")
    ax.set_ylabel("Ось Y")
    ax.set_zlabel("Ось Z")
    ax.set_title("Аттрактор Лоренца")
    plt.show()


x_s, y_s, z_s = 1, -1, 10
s_s, r_s, b_s = 10, 28, 8/3
cycles = 10000
dt_s = 0.01
precision_s = 2
x_data, y_data, z_data = calculate_lorenz(x_s, y_s, z_s, s_s, r_s, b_s, cycles, dt_s, precision_s)
print(x_data)
print(y_data)
print(z_data)
show_plots(x_data, y_data, z_data, cycles)
