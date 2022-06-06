def back_euclid(first, second, verbose=True):
    """
    Prints the backward euclid algorithm:

    Example:
         back_euclid(12, 29)
         29 = 12 * 2 + 5
         12 = 5 * 2 + 2
         5 = 2 * 2 + 1

         1 = 5 - 2 * 2
         2 = 12 - 5 * 2
         5 = 29 - 12 * 2

         1 == 5 * 1 - (12 - 5 * 2) * 2 == - 12 * 2 + 5 * 5
         1 == - 12 * 2 + (29 - 12 * 2) * 5 == 29 * 5 - 12 * 12
    """
    reminders = {}
    if first < second:
        first, second = second, first
    while first % second != 0:
        if verbose:
            print(f'{first} = {second} * {first // second} + '
                  f'{first % second}')
        reminder = first % second
        reminders[reminder] = (first, second, first // second)
        first, second = second, first % second
    if verbose:
        print()
    steps = sorted(reminders.items(), key=lambda x: x[0])
    last = 1
    first_num = -1
    first_coefficient = 1
    second_coefficient = 1
    for reminder, data in steps:
        if first_num == -1:
            first_num = data[0]
            second_coefficient = -data[2]
            last = reminder
        if verbose:
            print(f'{reminder} = {data[0]} - {data[1]} * {data[2]}')
    if verbose:
        print()
    for reminder, data in steps[1:]:
        first_sign = ' -' if first_coefficient < 0 else ''
        second_sign = '-' if second_coefficient < 0 else '+'
        if verbose:
            print(f'{last} =={first_sign} {first_num} * '
                  f'{abs(first_coefficient)} {second_sign} ({data[0]} - '
                  f'{data[1]} * {data[2]}) * {abs(second_coefficient)}',
                  end=' ==')
        first_num, first_coefficient, second_coefficient = \
            data[0], \
            second_coefficient, \
            first_coefficient - second_coefficient * data[2]
        first_sign = ' -' if first_coefficient < 0 else ''
        second_sign = '-' if second_coefficient < 0 else '+'
        if verbose:
            print(f'{first_sign} {data[0]} * {abs(first_coefficient)} '
                  f'{second_sign} {data[1]} * {abs(second_coefficient)}')
    return first_coefficient, second_coefficient


def gcd(first, second):
    if first < second:
        first, second = second, first
    while second:
        first, second = second, first % second
    return first


def lcd(first, second):
    return first * second // gcd(first, second)
