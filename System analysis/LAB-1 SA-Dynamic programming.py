# Вариант №8. Динамическое программирование

# Всего 400 млн
# 0:  10 - 15 - 13 - 14
# 1:  13 - 20 - 17 - 16
# 2:  16 - 22 - 21 - 23
# 3:  21 - 25 - 26 - 25
# 4:  25 - 30 - 28 - 27
# 5:  25 - 32 - 30 - 32

profit = [[10, 15, 13, 14],
          [13, 20, 17, 16],
          [16, 22, 21, 23],
          [21, 25, 26, 25],
          [25, 30, 28, 27],
          [25, 32, 30, 32]]

profit_transparent =[[10, 13, 16, 21, 25, 25],
                     [15, 20, 22, 25, 30, 32],
                     [13, 17, 21, 26, 28, 30],
                     [14, 16, 23, 25, 27, 32]]

calculated_profit = [[-1 for _ in range(6)] for _ in range(4)]

max_num = -1
def get_factory_profit(factory_num, money, money_factory_num, list_of_max):
    if factory_num == 0:
        if calculated_profit[0][money] != -1:
            return calculated_profit[0][money]
        else:
            calculated_profit[0][money] = profit[money][0]
            return calculated_profit[0][money]
    else:
        if calculated_profit[factory_num][money] != -1:
            return calculated_profit[factory_num][money]
        if money < money_factory_num:
            return -1
        else:
            list_of_max.append(profit[money_factory_num][factory_num] +
                               get_factory_profit(factory_num - 1, money - money_factory_num, 0, []))
            get_factory_profit(factory_num, money, money_factory_num + 1, list_of_max)
            max_profit = max(list_of_max)
            global max_num
            max_num = list_of_max.index(max_profit)
            if calculated_profit[factory_num][money] == -1:
                calculated_profit[factory_num][money] = max_profit
            return max_profit

maximum_profit = get_factory_profit(3, 5, 0, [])
print("Максимальные прибыли по фирмам:", calculated_profit)
print("Максимальная прибыль равна: ",maximum_profit)

answer = []
for x1 in range(len(profit)):
    for x2 in range(len(profit)):
        for x3 in range(len(profit)):
            for x4 in range(len(profit)):
                if profit_transparent[0][x1] + profit_transparent[1][x2] + \
                    profit_transparent[2][x3] + profit_transparent[3][x4] == maximum_profit and x1 + x2 + x3 + x4 == len(profit) - 1:
                    answer = [x * 80 for x in [x1, x2, x3, x4]]
print("Распределение вложений по предприятиям:", answer)

max_num = -1
for x1 in range(len(profit)):
    for x2 in range(len(profit)):
        for x3 in range(len(profit)):
            for x4 in range(len(profit)):
                if  x1 + x2 + x3 + x4 == len(profit) - 1:
                    if profit_transparent[0][x1] + profit_transparent[1][x2] + \
                    profit_transparent[2][x3] + profit_transparent[3][x4] > max_num:
                        max_num = profit_transparent[0][x1] + profit_transparent[1][x2] + \
                    profit_transparent[2][x3] + profit_transparent[3][x4]
print("Результат, полученный полным перебором:", max_num)