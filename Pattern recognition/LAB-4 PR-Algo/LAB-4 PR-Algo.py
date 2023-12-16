import math
import itertools


def load_data(file_name):
    with open(file_name) as file:
        return [float(x) for x in file.readline().rsplit()]


def load_table(file_name):
    with open(file_name) as file:
        numbers = []
        for line in file:
            numbers.append([int(x) for x in line.rsplit()])
        return numbers


def define_s(table):
    numbers = []
    for i in range(len(table[0])):
        temp_line = [[], []]
        for j in range(len(table)):
            temp_line[table[j][i]].append(j)
        numbers.append(temp_line)
    return numbers


def calculate_informative(states, probs):
    p = []
    for i in range(len(states)):
        p.append([sum(probs[j] for j in states[i][0]), sum(probs[j] for j in states[i][1])])
    return [p[i][0] * -math.log2(p[i][0]) + p[i][1] * -math.log2(p[i][1]) for i in range(len(p))]


def calculate_informative_with_picked(states, probs, picked_p):
    p = []
    for i in range(len(states)):
        patterns = list(itertools.product([0, 1], repeat=len(picked_p) + 1))
        temp_line = []
        for pattern in patterns:
            p_states = list(range(len(probs)))
            next_p_states = []
            for p_state in p_states:
                if p_state in states[i][pattern[0]]:
                    next_p_states.append(p_state)
            p_states = next_p_states.copy()
            for pattern_iter in range(len(picked_p)):
                next_p_states = []
                for p_state in p_states:
                    if p_state in states[picked_p[pattern_iter]][pattern[pattern_iter + 1]]:
                        next_p_states.append(p_state)
                p_states = next_p_states.copy()
            temp_line.append(sum([probs[x] for x in p_states]))
        p.append(temp_line)
    i_s = []
    for i in range(len(p)):
        if i in picked_p:
            i_s.append(-1)
        else:
            i_temp = []
            for x in p[i]:
                if x != 0:
                    i_temp.append(x * -1 * math.log2(x))
            i_s.append(sum(i_temp))
    return i_s

def informative_step(s_s, p_s, picked_s, high):
    print("\nУсловная информативность проверки количеством: 1")
    i = calculate_informative_with_picked(s_s, p_s, picked_s)
    picked_s.append(i.index(max(i)))
    print(i)
    print("Выбранные признаки:", picked_s)
    if max(i) == high:
        print("Проверка является последней в искомой совокупности, так как полностью снимает неопределенность")
    else:
        informative_step(s_s, p_s, picked_s, high)



qp = load_data("LAB-4_Data.txt")
pp = [1 - x for x in qp]
qppp = [qp[i] / pp[i] for i in range(len(qp))]
ps = [qppp[i] / (sum(qppp) + 1) for i in range(len(qp))]
ps.append(1 / (sum(qppp) + 1))
print("Вероятности отказа:")
print(qp)
print("Вероятности безотказной работы:")
print(pp)
print("Вероятности нахождения в техническом состоянии:")
print(ps)

h = sum([x * -math.log2(x) for x in ps])
print("Энтропия исходного состояния объекта:", h)

print("\nОпределяем множества S^0_j и S^1_j")
t = load_table("LAB-4_Table.txt")
s = define_s(t)
for i in range(len(s)):
    print(f"Для признака №{i}")
    print(f"S^0_{i}: {s[i][0]}")
    print(f"S^1_{i}: {s[i][1]}")

p_test = [0.2, 0.05, 0.24, 0.15, 0.06, 0.3]
t_test = load_table("test.txt")
s_test = define_s(t_test)

informative_step(s, ps, [], h)
