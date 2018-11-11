import itertools
from fractions import Fraction
import matplotlib.pyplot as plt
import pylab
from math import sqrt


def calculate_data(a, b, function):
    dict = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            key = function(k1, k2)
            if key in dict:
                dict[key] += v1 * v2
            else:
                dict.update({key: v1 * v2})
    return dict


def calculate_lcm(a, b):
    return lcm(a + 2, a * b)


def calculate_gcd(a, b):
    return gcd(a * a, 3 * b)


def calculate_lcm_multiply_gcd(a, b):
    return calculate_lcm(a, b) * calculate_gcd(a, b)


def get_sum(m, n):
    return calculate_data(m, n, lambda n1, n2: n1 + n2)


def get_composition(m, n):
    return calculate_data(m, n, lambda n1, n2: n1 * n2)


def get_gcd(m, n):
    return calculate_data(m, n, calculate_gcd)


def get_lcm(m, n):
    return calculate_data(m, n, calculate_lcm)


def get_lcm_multiply_gcd(m, n):
    return calculate_data(m, n, calculate_lcm_multiply_gcd)


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return int(a * b / gcd(a, b))


def get_expv(data):
    sum = 0
    for k, v in data.items():
        sum += k * v
    return sum


def get_dispersion(distribution):
    expected_value = get_expv(distribution)
    new_distribution = {k ** 2: v for k, v in distribution.items()}
    expected_value_of_squared_random_value = get_expv(new_distribution)
    squared_expected_value = expected_value ** 2
    return expected_value_of_squared_random_value - squared_expected_value


def get_median(data):
    sum = 0
    items = sorted(tuple(data.items()), key=lambda keys: keys[0])
    for k, v in items:
        sum += v
        if sum >= 0.5:
            return k


def get_standart_deviation(distribution):
    return sqrt(get_dispersion(distribution))


def get_covariance(distribution1, distribution2, composition):
    return get_expv(composition) - get_expv(distribution1) * get_expv(distribution2)


def get_correlation(distribution1, distribution2, composition):
    return get_covariance(distribution1, distribution2, composition) / \
           (get_standart_deviation(distribution1) * get_standart_deviation(distribution2))


def convert_fractions(data):
    for k, v in data.items():
        data[k] = v.limit_denominator()
    return data


def str2fraction(data):
    return [Fraction(int(e[0]), int(e[2:])).limit_denominator() for e in data.split()]


def print_distribution(data):
    print_distr = ''
    for element in data.keys():
        element = str(element)
        print_distr += element + ' ' * (7 - len(element)) + '|'

    print_prob = ''
    for element in data.values():
        element = str(element)
        print_prob += element + ' ' * (7 - len(element)) + '|'

    print()
    print(print_distr)
    print('-' * (8 * len(data)))
    print(print_prob)
    print()


def create_graphic(data):
    keys = list(data.keys())
    keys.sort()
    values = [round(data[key].numerator / data[key].denominator, 5) for key in keys]
    values_for_graphic = list(itertools.accumulate(values))
    pylab.xlim(0, max(keys))
    pylab.ylim(0, 1.01)
    plt.grid(True)
    min_coef = 0
    coefs = []
    for i in range(len(keys) - 1):
        coefs.append(min_coef)
        max_coef = keys[i + 1] / keys[-1]
        pylab.axhline(xmin=min_coef, xmax=max_coef, y=values_for_graphic[i], color='r')
        min_coef = max_coef
    pylab.axhline(xmin=min_coef, xmax=1, y=1, color='r')
    plt.show()


def check_on_equals_1(distribution, operation):
    print()
    print('############ ПРОВЕРКИ НА РАВЕНСТВО ЕДИНИЦЕ #############')
    print()
    print(f'Проверим {operation}: 1 == {list(itertools.accumulate(distribution.values()))[-1].limit_denominator()}')
    print()
    print('########################################################')
    print()


def print_start_data(m, n):
    print('\n######################### ДАНО #########################\n')
    print_distribution(m)
    print_distribution(n)
    print('\n########################################################\n')


def print_information(distribution, draw_graphic):
    print('\n############### МАТОЖИДАНИЕ И ДИСПЕРСИЯ ################\n')

    expected_value = get_expv(distribution)
    print(f'Матожидание равно: {round(expected_value.numerator / expected_value.denominator, 5)}')

    dispersion = get_dispersion(distribution)
    print(f'Дисперсия равна: {round(dispersion.numerator / dispersion.denominator, 5)}')

    print('\n########################################################\n')

    print('\n####### МЕДИАНА И СРЕДНЕКВАДРАТИЧНОЕ ОТКЛОНЕНИЕ ########\n')

    median = get_median(distribution)
    print(f'Медиана равна: {median}')

    standart_deviation = get_standart_deviation(distribution)
    print(f'Среднеквадратичное отклонение равно: {round(standart_deviation, 5)}')

    print('\n########################################################\n')

    if draw_graphic:
        create_graphic(distribution)


def print_covariance_and_correlation(distribution_1, distribution_2, composition, formula_1, formula_2):
    print('\n###################### КОВАРИАЦИЯ #######################\n')

    covariance = get_covariance(distribution_1, distribution_2, composition)
    print(f'Ковариация {formula_1} и {formula_2} равна: {covariance.numerator / covariance.denominator}')

    correlation = get_correlation(distribution_1, distribution_2, composition)
    print(f'Корреляция {formula_1} и {formula_2} равна: {correlation}')

    print('\n########################################################\n')


def func_for_my_task(m, n, print_results, draw_graphic):
    """ lcm(m + 2, m * n)"""

    print('\n################### РАСПРЕДЕЛЕНИЯ ######################\n')

    result_lcm = get_lcm(m, n)
    distribution = convert_fractions(result_lcm)
    print(f'Распределение \"LCM(m + 2, m * n)\":')
    print_distribution(result_lcm)

    print('\n########################################################\n')

    if print_results:
        check_on_equals_1(distribution, 'НОК')
        print_information(distribution, draw_graphic)

    return distribution


def func_for_other_task(m, n, print_results, draw_graphic):
    """ gcd(m ^ 2, 3 * n)"""

    print('\n################### РАСПРЕДЕЛЕНИЯ ######################\n')

    result_gcd = get_gcd(m, n)
    distribution = convert_fractions(result_gcd)
    print(f'Распределение \"GCD(m ^ 2, 3 * n)\":')
    print_distribution(result_gcd)

    print('\n########################################################\n')

    if print_results:
        check_on_equals_1(distribution, 'НОД')
        print_information(distribution, draw_graphic)

    return distribution


helper = """
Код вычисляет характеристики СВ с точностью до 5 знака после запятой указанных формул: 
        О=lcm(m + 2, m * n), О=gcd(m ^ 2, 3 * n), где m и n - СВ.

Правила ввода: все значения вводятся через пробел. Сколько значений СВ, столько и вероятностей этих СВ.

Пример ввода:
1 2 3 4 5 6                     # значения m
1/6 1/6 1/6 1/6 1/6 1/6         # распределение m
1 2 3 4 5 6                     # значения n
1/12 1/12 1/3 1/3 1/12 1/12     # распределение n

######################## Пояснения к коду! ###########################

Fraction - дробь типа m/n. Записывается как Fraction(m, n).
В коде используются распределения - словари {key: value}, 
                                        где key - значение СВ (тип int), 
                                            value - её вероятность (тип Fraction).

Есть функции:
1. get_sum - сумма двух СВ, на входе - распределения двух СВ, на выходе - словарь СВ;
2. get_multiply - произведение двух СВ, на входе - распределения двух СВ, на выходе - словарь СВ;
3. get_lcm - наименьшее общее кратное двух СВ, на входе - распределения двух СВ, на выходе - словарь СВ;
4. get_gcd - наибольший общий делитель двух СВ, на входе - распределения двух СВ, на выходе - словарь СВ;
5. get_expv - вычисление матожидания СВ, на входе - распределение СВ, на выходе - десятичное число;
6. get_dispersion - вычисление дисперсии СВ, на входе - распределение СВ, на выходе - десятичное число.
7. get_median - вычисление медианы СВ, на входе - распределение СВ, на выходе - десятичное число.
8. get_standart_deviation - вычисление среднекв. отклонение СВ, на входе - распределение СВ, на выходе - десятич. число.
9. get_covariance - вычисление ковариации двух СВ, на входе - распределения двух СВ, на выходе - десятичное число.
10. get_correlation - вычисление корреляции двух СВ, на входе - распределения двух СВ, на выходе - десятичное число.
"""

if __name__ == '__main__':
    print(helper + '\n\n')

    m = list(map(int, input('Введите значения СВ m через пробел: ').split()))
    m_p = str2fraction(input('Введите начальное распределение m через пробел: '))
    n = list(map(int, input('Введите значения СВ n через пробел: ').split()))
    n_p = str2fraction(input('Введите начальное распределение n через пробел: '))

    m = convert_fractions({m[i]: Fraction(m_p[i]) for i in range(len(m))})
    n = convert_fractions({n[i]: Fraction(n_p[i]) for i in range(len(n))})

    print_start_data(m, n)
    distribution_1 = func_for_my_task(m, n, print_results=False, draw_graphic=False)
    distribution_2 = func_for_other_task(m, n, print_results=False, draw_graphic=False)

    composition = get_lcm_multiply_gcd(m, n)
    print(f'Распределение LCM(m + 2, m * n) * GCD(m ^ 2, 3 * n):')
    print_distribution(composition)
    check_on_equals_1(composition, f'LCM(m + 2, m * n) * GCD(m ^ 2, 3 * n)')

    print_covariance_and_correlation(
        get_lcm(m, n),
        get_gcd(m, n),
        composition,
        f'LCM(m + 2, m * n)',
        f'GCD(m ^ 2, 3 * n)'
    )

    """
    # Для дебага:

    m = [1, 2, 3, 4, 5, 6]
    n = [1, 2, 3, 4, 5, 6]
    m_p = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
    n_p = [1/12, 1/12, 1/3, 1/3, 1/12, 1/12]
    """
