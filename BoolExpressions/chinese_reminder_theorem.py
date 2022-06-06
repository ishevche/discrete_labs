from euclid import *


def find_number(data: list):
    multiply = 1
    for rem, mod in data:
        if gcd(multiply, mod) != 1:
            raise ValueError('Not all modules are co-prime')
        multiply = lcd(multiply, mod)
    result_sum = 0
    multipliers = []
    for rem, mod in data:
        modulo = multiply // mod
        inverse = back_euclid(mod, modulo % mod, False)[1] % mod
        multipliers += [f'{inverse}*{modulo}*{rem}']
        result_sum += inverse * modulo * rem
        result_sum %= multiply
    print(f"({' + '.join(multipliers)}) mod {multiply} = {result_sum}")
