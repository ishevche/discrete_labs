from random import randrange, getrandbits


def check_prime(number, tests):
    """
    Test if number is prime by Miller-Rabin test
    :param number: number which we check if it is prime
    :param tests: number of tests, accuracy > 1/4 ** tests
    :return: bool
    """
    if number == 2 or number == 3:
        return True
    if number % 2 == 0:
        return False
    m = (number - 1) // 2
    t = 0
    while m & 1 == 0:
        m = m // 2
        t += 1
    for _ in range(tests):
        a = randrange(2, number - 1)
        u = pow(a, m, number)
        if u != 1 and u != number - 1:
            j = 1
            while j < t and u != number - 1:
                u = pow(u, 2, number)
                if u == 1:
                    return False
                j += 1
            if u != number - 1:
                return False
    return True


def generate_prime(length):
    """
    Generate prime number by length of it bitwise
    :param length: length of prime number bitwise
    :return: prime number
    """
    while True:
        number = ((getrandbits(length - 2) + (1 << (length - 2))) << 1) + 1
        prime = check_prime(int(number), 128)
        if prime:
            return number
