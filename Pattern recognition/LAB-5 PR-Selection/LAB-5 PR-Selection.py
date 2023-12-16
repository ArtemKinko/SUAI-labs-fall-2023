import tabulate


def load_data(file_name):
    with open(file_name) as file:
        numbers = []
        for line in file:
            temp_line = []
            for elem in line.rsplit():
                temp_line.append([float(elem.split(';')[0]), float(elem.split(';')[1])])
            numbers.append(temp_line)
    return numbers


def get_executive_abilities(matrix):
    numbers = []
    row_titles = []
    for first_s in range(len(matrix)):
        for second_s in range(first_s + 1, len(matrix), 1):
            temp_line = []
            for param in range(len(matrix[0])):
                union = max([matrix[first_s][param][1], matrix[second_s][param][1]]) - \
                        min([matrix[first_s][param][0], matrix[second_s][param][0]])
                intersection = min([matrix[first_s][param][1], matrix[second_s][param][1]]) - \
                               max([matrix[first_s][param][0], matrix[second_s][param][0]])
                if max([matrix[first_s][param][0], matrix[second_s][param][0]]) >= \
                        min([matrix[first_s][param][1], matrix[second_s][param][1]]):
                    temp_line.append(1)
                else:
                    temp_line.append(1 - intersection / union)
            numbers.append(temp_line)
            row_titles.append(str(first_s + 1) + " - " + str(second_s + 1))
    return numbers, row_titles


def print_matrix(matrix, row_titles, column_titles, picked_colums):
    titles = ["Признаки →\nСостояния ↓"]
    titles.extend(column_titles)
    print_data = [titles]
    for i in range(len(matrix)):
        temp_line = [row_titles[i]]
        for j in range(len(matrix[0])):
            if j not in picked_colums:
                temp_line.append(matrix[i][j])
        print_data.append(temp_line)
    print(tabulate.tabulate(print_data, tablefmt="grid"))


def recalculate_matrix(matrix, picked):
    new_matrix = []
    for i in range(len(matrix)):
        new_matrix.append([matrix[i][picked] + (1 - matrix[i][picked]) * matrix[i][j] for j in range(len(matrix[0]))])
    return new_matrix

def define_next_param(matrix, row_titles, column_titles, picked):
    r = []
    for param in range(len(matrix[0])):
        if param not in picked:
            r.append(sum([matrix[i][param] for i in range(len(matrix))]))
    picked.append(int(column_titles[r.index(max(r))]) - 1)
    print("Значения показателей R:")
    print(tabulate.tabulate([r]))
    print("Выбираем проверку признака под номером", column_titles[r.index(max(r))])

    new_matrix = []
    new_row_titles = []
    for line_i in range(len(matrix)):
        if matrix[line_i][picked[-1]] != 1:
            new_matrix.append(matrix[line_i])
            new_row_titles.append(row_titles[line_i])
    new_column_titles = []
    for i in range(len(matrix[0])):
        if i not in picked:
            new_column_titles.append(i + 1)

    if len(new_matrix) == 0:
        print("Все строки вычеркнуты.\nПолученный порядок проверок признаков:", [x + 1 for x in picked])
        return picked

    print("Матрица после вычеркивания строк:")
    print_matrix(new_matrix, new_row_titles, column_titles, picked[:-1])

    new_matrix = recalculate_matrix(new_matrix, picked[-1])
    print("Пересчитываем матрицу:")
    print_matrix(new_matrix, new_row_titles, new_column_titles, picked)

    define_next_param(new_matrix, new_row_titles, new_column_titles, picked)


data = load_data("LAB-5_Data.txt")

print("Исходные данные для варианта №12:")
print(tabulate.tabulate(data))

column_labels = ["1", "2", "3", "4", "5", "6"]
executive_abilities, row_labels = get_executive_abilities(data)

print("Матрица разрешающей способности признаков:")
print_matrix(executive_abilities, row_labels, column_labels, [])

define_next_param(executive_abilities, row_labels, column_labels, [])