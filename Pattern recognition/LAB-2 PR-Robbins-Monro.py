import math
import matplotlib.pyplot as plt

import tabulate


def load_data(file_name, var_num):
    current_var = 0
    late_numbers = []
    with open(file_name) as file:
        numbers = []
        for line in file:
            current_var += 1
            temp_line = []
            for elem in line.rsplit():
                temp_line.append(float(elem))
            if current_var > var_num:
                numbers.append(temp_line)
            else:
                late_numbers.append(temp_line)
        numbers.extend(late_numbers)
        return numbers


def get_g_fun(data_list):
    return [math.sin(data_list[0]),
            math.cos(data_list[1]),
            math.sin(2 * data_list[2]),
            math.cos(2 * data_list[3]),
            math.sin(3 * data_list[4])]


def robbins_step(g_list, e_list, data_set, current_step, is_1_done, is_2_done, cond_1, cond_2):
    current_g = get_g_fun(data_set[current_step])
    g_list.append(current_g)
    if current_step == 0:
        current_e = current_g
    else:
        current_e = [e_list[current_step - 1][i] - 1 / (current_step + 1) *
                     (e_list[current_step - 1][i] - current_g[i]) for i in range(5)]
    e_list.append(current_e)
    print("\nДля шага №", current_step)
    print("Вектор наблюдаемого состояния:")
    print(tabulate.tabulate([data_set[current_step]]))
    print("Вектор G-преобразования:")
    print(tabulate.tabulate([current_g]))
    print("Изображение:")
    print(tabulate.tabulate([current_e]))

    if current_step != 0:
        if not is_1_done:
            first_condition = max([abs(e_list[current_step][i] - e_list[current_step - 1][i]) for i in range(5)])
            print("По критерию 1:", first_condition, ("<= 0.01 - условие не выполняется" if first_condition > 0.01
                                                      else "<= 0.01 - условие выполняется."))
            cond_1.append(first_condition)
        else:
            first_condition = 0
        if not is_2_done:
            second_condition = math.sqrt(sum([pow(e_list[current_step][i] - e_list[current_step - 1][i], 2) for i in range(5)]))
            print("По критерию 2:", second_condition, ("<= 0.01 - условие не выполняется" if second_condition > 0.01
                                                       else "<= 0.01 - условие выполняется."))
            cond_2.append(second_condition)
        else:
            second_condition = 0

        if first_condition <= 0.01:
            if second_condition <= 0.01:
                return
            else:
                robbins_step(g_list, e_list, data_set, current_step + 1, True, False, cond_1, cond_2)
        else:
            robbins_step(g_list, e_list, data_set, current_step + 1, False, False, cond_1, cond_2)

    else:
        robbins_step(g_list, e_list, data_set, current_step + 1, False, False, cond_1, cond_2)


data = load_data("LAB-2_Data.txt", 12)
g, e, c1, c2 = [], [], [], []
print(tabulate.tabulate(data))

robbins_step(e, g, data, 0, False, False, c1, c2)

x = list(range(len(c1)))
plt.plot(x, c1, marker='o')
plt.plot(x, c2, marker='o')
plt.plot(x, [0.01 for _ in range(len(c1))])
plt.title("Условия насыщенности")
plt.legend(["Расстояние Чебышева", "Евклидово расстояние", "Пороговое значение"])

plt.show()