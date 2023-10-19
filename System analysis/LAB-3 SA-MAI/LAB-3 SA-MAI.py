# Вариант №8.
import fractions
import io
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
    print('tl_weights:', tl_weights)
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
        a_table, a_weights = calculate_weights("tables/alternative_c1.txt")
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

    total = create_weight_alternative_table(n_weights, alternative_weights)
    print('total', total)
    result = calculate_total_coefs(total)
    print(result)


solve("tables/criteria_table.txt", 7)
