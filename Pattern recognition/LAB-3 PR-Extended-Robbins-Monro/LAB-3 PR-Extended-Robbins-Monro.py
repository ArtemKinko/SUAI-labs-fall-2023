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


def robbins_generate(data_set):
    e_data = [data_set[0]]
    for k in range(2, len(data_set) + 1, 1):
        e_data.append([round(e_data[-1][i] - 1 / k * (e_data[-1][i] - data_set[k - 1][i]), 6) for i in range(len(e_data[-1]))])
    return e_data


data = load_data("LAB-3_Data.txt", 12)

print("Исходные данные")
print(tabulate.tabulate(data, tablefmt="grid"))

e = robbins_generate(data)
print("Полученные изображения на каждом шагу:")
print(tabulate.tabulate(e, tablefmt="grid"))
