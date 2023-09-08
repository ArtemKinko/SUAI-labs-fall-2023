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

calculated_profit = [[-1 for _ in range(6)] for _ in range(4)]

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
            list_of_max.append(profit[money_factory_num][factory_num] + get_factory_profit(factory_num - 1, money - money_factory_num, 0, []))
            get_factory_profit(factory_num, money, money_factory_num + 1, list_of_max)
            max_profit = max(list_of_max)
            if calculated_profit[factory_num][money] == -1:
                calculated_profit[factory_num][money] = max_profit
            return max_profit

print(get_factory_profit(3, 5, 0, []))
print(calculated_profit)

