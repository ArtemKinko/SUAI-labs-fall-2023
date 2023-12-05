import math
import matplotlib.pyplot as plt

import tabulate

def load_data(file_name):
    with open(file_name) as file:
        numbers = []
        for line in file:
            temp_line = []
            for elem in line.rsplit():
                temp_line.append(float(elem))
            numbers.append(temp_line)
        return numbers

def get_distance(states):
    numbers = []
    for i in range(len(states)):
        temp_numbers = []
        for j in range(len(states[0])):
            summary = 0
            for i_state in range(len(states)):
                summary += pow(states[i][i_state] - states[j][i_state], 2)
            temp_numbers.append(math.sqrt(summary))
        numbers.append(temp_numbers)
    return numbers

def get_far_classes(distances):
    numbers = []
    for line in distances:
        numbers.append(line.index(max(line)))
    return numbers

def get_incs(states, far):
    numbers = []
    for i in range(len(states)):
        temp_numbers = []
        for j in range(len(states)):
            temp_numbers.append(0.5 * abs(states[i][j] - states[far[i]][j]))
        numbers.append(temp_numbers)
    return numbers

def get_left_right(states, incs):
    numbers = []
    for i in range(len(states)):
        temp_numbers = []
        for j in range(len(states)):
            temp_numbers.append([round(states[i][j] - incs[i][j], 2), round(states[i][j] + incs[i][j], 2)])
        numbers.append(temp_numbers)
    return numbers

s = load_data("LAB-1_Data.txt")
print("Исходные данные:")
print(tabulate.tabulate(s))

d = get_distance(s)
print("Матрица межклассовых расстояний:")
print(tabulate.tabulate(d))

f = get_far_classes(d)
print("Наиболее удаленные классы:")
print(tabulate.tabulate([f]))

inc = get_incs(s, f)
print("Разброс значений:")
print(tabulate.tabulate(inc))


lr = get_left_right(s, inc)
print("Результирующая таблица с границами интервалов")
print(tabulate.tabulate(lr))


plots_y = []
for i in range(len(s)):
    plots_y.append([i, i])

info_states = {}

# для каждого признака определяем информационное состояние
for k in range(len(s)):
    plots_x = []
    points = []
    for j in range(len(s)):
        plots_x.append([lr[j][k][0], lr[j][k][1]])
        points.append(lr[j][k][0])
        points.append(lr[j][k][1])
    points = set(points)
    points = list(points)
    points.sort()
    print(points)

    # находим признаки
    for i in range(len(points) - 1):
        mid = 0.5 * (points[i + 1] - points[i]) + points[i]
        stations = []
        for j in range(len(plots_x)):
            if plots_x[j][0] <= mid <= plots_x[j][1]:
                stations.append(j)
        print("Информационное состояние:", stations)
        if tuple(stations) in info_states.keys():
            temp = info_states.get(tuple(stations))
            temp.append(k)
            info_states[tuple(stations)] = temp
        else:
            info_states[tuple(stations)] = [k]
    # графики
    for i in range(len(s)):
        plt.plot(plots_x[i], plots_y[i], marker='o')
        plt.title("Признак №" + str(k + 1))
    plt.grid(True)
    plt.show()

# сортировка полученных состояний и вывод в таблице
keys = list(info_states.keys())
keys.sort(key=len)
list_info_states = [[i, info_states[i]] for i in keys]
print(tabulate.tabulate(list_info_states))

