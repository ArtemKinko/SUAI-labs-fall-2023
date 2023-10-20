# Вариант №8.
import fractions
import io
import math

from tabulate import tabulate

# C1. Цена
# C2. Партионность и скидки
# C3. Надежность
# C4. Расстояние между складами
# C5. Транспортные расходы
# C6. Сроки поставки
# C7. Место расположения, км

import numpy
from unicodedata import decimal


def calculate_weights(criteria_table_path):
    criteria_table = []
    weights = []

    with open(criteria_table_path) as table:
        for line in table:
            current_criteria = [float(fractions.Fraction(x)) for x in line.rsplit()]
            criteria_table.append(current_criteria)
            weights.append(
                pow(numpy.prod([float(fractions.Fraction(x)) for x in current_criteria]), 1 / len(current_criteria)))
    sum_weights = sum(weights)
    normal_weights = [x / sum_weights for x in weights]
    return criteria_table, normal_weights


def create_weight_alternative_table(cr_table, criteria):
    total_weights = [cr_table]
    for i in range(len(criteria[0])):
        new_line = []
        for j in range(len(criteria)):
            new_line.append(criteria[j][i])
        total_weights.append(new_line)
    return total_weights


def calculate_total_coefs(tl_weights):
    return [sum([tl_weights[0][j] * tl_weights[i][j] for j in range(len(tl_weights[0]))])
            for i in range(1, len(tl_weights))]


def is_consistence(table, weights):
    if len(weights) <= 2:
        return True
    consistence_random = [0, 0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    sum_column = [sum([table[j][i] for j in range(len(table))]) for i in range(len(table))]
    lambda_max = sum([sum_column[i] * weights[i] for i in range(len(table))])
    consistence_index = (lambda_max - len(table)) / (len(table) - 1)
    print('Индекс согласованности:', consistence_index)
    consistence_ratio_index = consistence_index / consistence_random[len(table)]
    print('Индекс отношения согласованности:', consistence_ratio_index)
    return consistence_ratio_index < 0.1

def calculate_mai_plus(cr_weights, al_weights, names):
    locals_table = []
    for table in al_weights:
        locals = []
        for i in range(len(al_weights[0])):
            local_row = []
            for j in range(len(al_weights[0])):
                local_row.append([table[i] / (table[i] + table[j]), table[j] / (table[i] + table[j])])
            locals.append(local_row)
        locals_table.append(locals)

    for i in range(len(locals_table)):
        print("Локальные ВКА первого уровня для критерия:", names[i])
        for local in locals_table[i]:
            test = [" ; ".join([str(round(x, 2)) for x in elem]) for elem in local]
            print("\t | \t".join(test))

    vka_2 = []
    for i in range(len(locals_table[0])):
        temp_row = []
        for j in range(len(locals_table[0])):
            elem_x, elem_y = 0, 0
            for crit in range(len(cr_weights)):
                elem_x += cr_weights[crit] * locals_table[crit][i][j][0]
                elem_y += cr_weights[crit] * locals_table[crit][i][j][1]
            temp_row.append([elem_x, elem_y])
        vka_2.append(temp_row)

    print("\nЛокальные ВКА второго уровня:")
    for local in vka_2:
        test = [" ; ".join([str(round(x, 2)) for x in elem]) for elem in local]
        print("\t | \t".join(test))

    vka_2 = [[[elem[0] / (elem[0] + elem[1]), elem[1] / (elem[0] + elem[1])] for elem in row] for row in vka_2]
    globs = [pow(math.prod([x[0] for x in row]), 1 / len(vka_2)) for row in vka_2]

    print("\nНормированные локальные ВКА второго уровня:")
    for local in vka_2:
        test = [" ; ".join([str(round(x, 2)) for x in elem]) for elem in local]
        print("\t | \t".join(test))

    print("\nГлобальные значения ВКА по геометрическому среднему:")
    print(globs)
    globs = [elem / sum(globs) for elem in globs]
    print("\nНормированные глобальные значения ВКА по геометрическому среднему:")
    print(globs)
    return globs


def solve(criteria_table_path, number_of_criterias):
    criteria_names = []
    with io.open("tables/criteria_names.txt", encoding='utf-8') as names_file:
        for line in names_file:
            criteria_names.append("".join(line.rsplit('\n')))
    names_for_table_criteria = ['Критерии'] + criteria_names + ['Нормированные веса']

    alternative_names = []
    with io.open("tables/alternative_names.txt", encoding='utf-8') as names_file:
        for line in names_file:
            alternative_names.append("".join(line.rsplit('\n')))

    print("Матрица попарных сравнений с нормализованными весами критериев:")
    cr_table, n_weights = calculate_weights(criteria_table_path)
    cr_table_tabulate = []
    for i in range(len(cr_table)):
        temp_line = [criteria_names[i]]
        temp_line += [str(x) for x in cr_table[i]]
        temp_line += [str(n_weights[i])]
        cr_table_tabulate.append(temp_line)
    print(tabulate(cr_table_tabulate, names_for_table_criteria, 'grid'))
    if not is_consistence(cr_table, n_weights):
        print("Матрица не согласована! Невозможно применить МАИ")
        return
    else:
        print("Матрица согласована!\n\n")

    alternative_tables = []
    alternative_weights = []
    for i in range(number_of_criterias):
        a_table, a_weights = calculate_weights("tables/alternative_c" + str(i + 1) + ".txt")
        alternative_tables.append(a_table)
        alternative_weights.append(a_weights)
        names_for_alternative = [criteria_names[i]] + alternative_names + ['Нормированные веса']
        a_table_tabulate = []
        for j in range(len(a_table)):
            temp_line = [alternative_names[j]]
            temp_line += [str(x) for x in a_table[j]]
            temp_line += [str(a_weights[j])]
            a_table_tabulate.append(temp_line)
        print("Матрица парных сравнений с весами для альтернатив по критерию:", criteria_names[i])
        print(tabulate(a_table_tabulate, names_for_alternative, 'grid'))
        if not is_consistence(cr_table, n_weights):
            print("Матрица не согласована! Невозможно применить МАИ")
            return
        else:
            print("Матрица согласована!\n\n")

    print("Расчет с помощью МАИ+")

    globs = calculate_mai_plus(n_weights, alternative_weights, criteria_names)
    total = create_weight_alternative_table(n_weights, alternative_weights)

    result = calculate_total_coefs(total)

    print("\nМатрица локальных весов критериев и альтернатив с глобальными весами (по МАИ):")
    alternative_names.insert(0, "")
    names_for_table_criteria.insert(-1, "Глобальные веса")
    for i in range(len(total)):
        if i != 0:
            total[i] += [result[i - 1]]
        total[i] = [alternative_names[i]] + [str(elem) for elem in total[i]]
    print(tabulate(total, names_for_table_criteria, 'grid'))
    print("Согласно МАИ, лучшая альтернатива:", alternative_names[result.index(max(result)) + 1])

    print()

    print("Согласно МАИ+, лучшая альтернатива:", alternative_names[globs.index(max(globs)) + 1])


solve("tables/criteria_table.txt", 7)
