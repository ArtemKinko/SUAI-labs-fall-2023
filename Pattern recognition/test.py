epsilon = 1
step = 1

a = 0
b = 5

x_0 = 0.05

def first_derivative(x):
    return 2 * x - 36 / x / x / x / x

def second_derivative(x):
    return 2 + 144 / x / x / x / x / x

def new_x(x, first_der, second_der):
    return x - first_der/second_der

counter = 1

while x_0 < b:
    d1 = first_derivative(x_0)
    d2 = second_derivative(x_0)
    nx = new_x(x_0, d1, d2)
    if abs(first_derivative(nx)) < epsilon:
        print("D1", d1)
        print("D2", d2)
        print("nx", nx)
        print("FOUND!", x_0, nx)
        print(counter)
        break
    else:
        counter += 1
        x_0 += step