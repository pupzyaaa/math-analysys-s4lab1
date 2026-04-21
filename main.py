import numpy as np
import matplotlib.pyplot as plt
import time

# Исследуемая функция f(x)
def f(x):
    return np.sin(x)


# Функция F(x)
def F(x):
    return np.ceil(x)


# Простая функция, построенная в аналитической части
def f_n(x, n):
    return (np.ceil(2.0**n * f(x)) - 1) / 2.0**n


# Функция вычисления меры Лебега
def measure_lebesgue(x_vals, i):
    return x_vals[i] - x_vals[i-1]


# Функция вычисления меры Лебега-Стилтьеса
def measure_stieltjes(x_vals, i):
    return F(x_vals[i]) - F(x_vals[i-1])


# Функция для вычисления интеграла, считаем как сумму $\sum_{k=1}^{N} C_k \cdot \mu A_k$
def compute_lebesgue_integral(x_vals, f_vals, measure_function):
    I = 0.0
    # Пройдемся по каждому множеству
    for i in range(1, len(x_vals)):
        # Считаем меру с помощью переданной функции: мера Лебега или мера Лебега-Стилтьеса
        mu = measure_function(x_vals, i)
        # Считаем сумму для интеграла
        I += f_vals[i-1] * mu

    return I


# Значения интегралов, вычесленные аналитически
analytical_lebesgue = 1 - np.cos(4)
analytical_stieltjes = sum(np.sin(k) for k in range(5))

# Разобьем отрезок [0, 4] на 5000 точек для вычисления интегралов
x_points = np.linspace(0, 4, 5000)

# 1. График аппроксимации простыми функциями
def plot_f_n():
    plt.figure(figsize=(12, 8))

    # Нарисуем оригинальную функцию
    plt.plot(x_points, f(x_points), label='$f(x) = \sin(x)$', color='black', linewidth=2)

    # Теперь нарисуем f_n при разных n
    for n in [2, 5, 10]:
        plt.plot(x_points, f_n(x_points, n), label=f'$f_{n}(x)$', linestyle='--')

    plt.title('Аппроксимация функции $f(x)=\sin(x)$ простыми функциями $f_n(0)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.savefig('fn_plot.png')

plot_f_n()


# 2. Численное вычисление интеграла Лебега
print("Численное вычисление интеграла Лебега")
print(f"Аналитическое значение: {analytical_lebesgue:.7f}")

# добавляем точку 4+dx, иначе 4 не учтется
dx = x_points[1] - x_points[0]
x_points = np.append(x_points, x_points[-1] + dx)

# Считаем время работы
start = time.perf_counter()

# Значения n для последовательности функций для вычисления интегралов
# Количество учатков при этом 2^n, то есть [8, 128, 1024]
N = [5, 10, 20]


# Для каждого значения n вычислим значения функций и посчитаем интеграл Лебега
for n in N:
    y_points = f_n(x_points, n)
    integral_num = compute_lebesgue_integral(x_points, y_points, measure_lebesgue)
    # Вычислим погрешность
    error = abs(analytical_lebesgue - integral_num)
    print(f"n = {n}, количество участков = {2**n}: Численный интеграл: {integral_num:.7f}, ошибка: {error:.7f}")

end = time.perf_counter()
print(f"Время работы: {end - start:.7f}")
print()

# 3. Численное вычисление интеграла Лебега-Стилтьеса
print("Численное вычисление интеграла Лебега-Стилтьеса")
print(f"Аналитическое значение: {analytical_stieltjes:.7f}")

start = time.perf_counter()
# Для каждого значения n вычислим значения функций и посчитаем интеграл Лебега-Стилтьеса
for n in N:
    y_points = f_n(x_points, n)
    integral_num = compute_lebesgue_integral(x_points, y_points, measure_stieltjes)

    # считаем погрешность
    error = abs(analytical_stieltjes - integral_num)
    print(f"n={n}, количество участков = {2**n}: Численный интеграл: {integral_num:.7f} | Ошибка: {error:.7f}")

end = time.perf_counter()
print(f"Время работы: {end - start:.7f}")

