# Вариант 12
import math

lamb = 1.35
tau = 0.5

c_ef = 1.5
c_1 = 15000
c_2 = 2000
c_3 = 1000
c_4 = 200
t = 365


def calculate_money_cost():
    rho = lamb / tau
    money_costs = []
    print("Интенсивность нагрузки", rho)
    for s in range(1, 10):
        print("\n------ Для", s, 'кассиров')
        p_0 = pow(sum([pow(rho, k) / math.factorial(k) for k in range(s + 1)]) + (pow(rho, s + 1) / math.factorial(s) / (s - rho)), -1)
        print("Доля времени простоя узла расчета:", p_0)
        p_q = pow(rho, s + 1) / math.factorial(s) / (s - rho) * p_0
        print("Вероятность того, что клиент окажется в очереди:", p_q)
        m_1 = p_q * s / (s - rho)
        print("Средняя длина очереди:", m_1)
        m_2 = sum([(s - k) / math.factorial(s) * pow(rho, k) * p_0 for k in range(s)])
        print("Среднее число занятых кассиров:", m_2)
        i = c_ef * c_1 * s + c_2 * m_2 + c_3 * (s - m_2) + c_4 * m_1 * t
        print("Затраты:", i)
        money_costs.append(i)


calculate_money_cost()
