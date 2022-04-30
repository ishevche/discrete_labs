class Expression:
    """
    Class used to generate truth tables of expressions

    Usage:
        x = Expression('x')
        y = Expression('y')
        print(x ^ y)

    Boolean operators:
        not - ~ or -
        or - | or +
        and - & or *
        xor - ^ or != or -
        -> - >= or >
        <- - <= or <
        <=> - ==
        Sheffer stroke - //
        Peirce's arrow - %
    """

    def __init__(self, variables_name: str, truth_table: str = '01'):
        if 2 ** len(variables_name) != len(truth_table):
            raise ValueError('Wrong truth table length')
        self.__variables = variables_name
        self.__truth_table = truth_table

    def __add_fiction_variable(self, variables_name: str):
        variables = self.__variables
        truth_table = self.__truth_table
        for variable in variables_name:
            if variable in variables:
                continue
            back_insert_idx = 0
            while back_insert_idx < len(variables) and \
                    variable < variables[-back_insert_idx - 1]:
                back_insert_idx += 1
            if back_insert_idx == 0:
                variables += variable
            else:
                variables = variables[:-back_insert_idx] + \
                            variable + variables[-back_insert_idx:]
            step = 2 ** back_insert_idx
            copy = truth_table
            truth_table = ''
            while copy:
                table_part, copy = copy[:step], copy[step:]
                truth_table += table_part * 2
        return Expression(variables, truth_table)

    def __generate_truth_table(self, other, func):
        if not isinstance(other, Expression):
            raise ValueError('Can perform operation only with '
                             'Expression object')
        first = self.__add_fiction_variable(other.__variables)
        second = other.__add_fiction_variable(self.__variables)
        truth_table = ''
        for i in range(len(first.__truth_table)):
            if func(first.__truth_table[i], second.__truth_table[i]):
                truth_table += '1'
            else:
                truth_table += '0'
        return Expression(first.__variables, truth_table)

    def print_saves_0(self) -> bool:
        """
        Prints info about belonging to a class that saves 0
        """
        print(f'f = {self.__truth_table} => '
              f'f({0:0{len(self.__variables)}}) '
              f'{"!" if self.__truth_table[0] == "1" else ""}= 0\n'
              f'T_0 {"-" if self.__truth_table[0] == "1" else "+"}')
        return self.__truth_table[0] == "0"

    def print_saves_1(self) -> bool:
        """
        Prints info about belonging to a class that saves 1
        """
        print(f'f = {self.__truth_table} => '
              f'f({1:1<{len(self.__variables)}}) '
              f'{"!" if self.__truth_table[-1] == "0" else ""}= 1\n'
              f'T_1 {"-" if self.__truth_table[-1] == "0" else "+"}')
        return self.__truth_table[-1] == "1"

    def print_self_dual(self) -> bool:
        """
        Prints info about belonging to a class that is self-dual
        """
        invert_table = ''.join(list(map(lambda a: '1' if a == '0' else '0',
                                        self.__truth_table)))[::-1]
        print(f'f = {self.__truth_table} => f* = {invert_table}\n'
              f'S {"+" if self.__truth_table == invert_table else "-"}')
        return self.__truth_table == invert_table

    def print_monotonous(self) -> bool:
        """
        Prints info about belonging to a class that is monotonous
        """
        for idx1, value1 in enumerate(self.__truth_table):
            if value1 == '0':
                continue
            idx1_bin = f'{bin(idx1)[2:]:0>{len(self.__variables)}}'
            for idx0, value0 in enumerate(self.__truth_table[idx1:]):
                idx0 += idx1
                if value0 == '1':
                    continue
                idx0_bin = f'{bin(idx0)[2:]:0>{len(self.__variables)}}'
                is_idx0_grater = True
                for i in range(len(self.__variables)):
                    if idx0_bin[i] < idx1_bin[i]:
                        is_idx0_grater = False
                        break
                if is_idx0_grater:
                    print(f'{idx0_bin} > {idx1_bin}, '
                          f'0 = f({idx0_bin}) < f({idx1_bin}) = 1\n'
                          f'M -')
                    return False
        print('M +')
        return True

    def print_linear(self) -> bool:
        """
        Prints info about belonging to a class that is linear
        """
        def get_coefficients(table: str) -> str:
            if len(table) == 1:
                return table
            if len(table) % 2 != 0:
                raise ValueError("Truth table length is not a power of 2")
            part_length = len(table) // 2
            xor_part = ''
            for idx in range(part_length):
                xor_part += '1' if table[idx] != table[idx + part_length] \
                    else '0'
            return (get_coefficients(table[:part_length]) +
                    get_coefficients(xor_part))

        coefficients = get_coefficients(self.__truth_table)
        print('f = ', end='')
        was_one = False
        is_linear = True
        for idx, value in enumerate(coefficients):
            if value == '0':
                continue
            if idx == 0:
                print(1, end='')
                was_one = True
                continue
            if was_one:
                print(' + ', end='')
            idx_bin = f'{bin(idx)[2:]:0>{len(self.__variables)}}'
            var = ''
            for var_idx in range(len(self.__variables)):
                if idx_bin[var_idx] == '1':
                    var += self.__variables[var_idx]
            if len(var) > 1:
                is_linear = False
            print(var, end='')
            was_one = True
        if not was_one:
            print(0, end='')
        print(f'\nL {"+" if is_linear else "-"}')
        return is_linear

    def print_fullness(self):
        """
        Prints info about belonging to classes of boolean functions
        """
        t0 = '+' if self.print_saves_0() else '-'
        print()
        t1 = '+' if self.print_saves_1() else '-'
        print()
        s = '+' if self.print_self_dual() else '-'
        print()
        m = '+' if self.print_monotonous() else '-'
        print()
        l = '+' if self.print_linear() else '-'
        print()
        print(f' 0 | 1 | S | M | L \n'
              f'---+---+---+---+---\n'
              f' {t0} | {t1} | {s} | {m} | {l} ')

    def __repr__(self):
        return self.__truth_table

    def __str__(self):
        ans = f' {self.__variables} | exp \n' \
              f'{"-" * (8 + len(self.__variables))}'
        for idx, val in enumerate(self.__truth_table):
            ans += f'\n {bin(idx)[2:]:{0}>{len(self.__variables)}} | ' \
                   f' {val} '
        return ans

    def __invert__(self):
        truth_table = ''
        for i in range(len(self.__truth_table)):
            if self.__truth_table[i] == '0':
                truth_table += '1'
            else:
                truth_table += '0'
        return Expression(self.__variables, truth_table)

    def __neg__(self):
        return ~self

    def __and__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '1' and
                                                                b == '1'))

    def __mul__(self, other):
        return self & other

    def __or__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '1' or
                                                                b == '1'))

    def __add__(self, other):
        return self | other

    def __ne__(self, other):
        return self.__generate_truth_table(other, lambda a, b: a != b)

    def __xor__(self, other):
        return self != other

    def __sub__(self, other):
        return self != other

    def __ge__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '0' or
                                                                b == '1'))

    def __gt__(self, other):
        return self >= other

    def __le__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '1' or
                                                                b == '0'))

    def __lt__(self, other):
        return self <= other

    def __eq__(self, other):
        return self.__generate_truth_table(other, lambda a, b: a == b)

    def __floordiv__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '0' or
                                                                b == '0'))

    def __mod__(self, other):
        return self.__generate_truth_table(other, lambda a, b: (a == '0' and
                                                                b == '0'))


if __name__ == '__main__':
    x = Expression('x')
    y = Expression('y')
    # not
    assert repr(-x) == '10'
    assert repr(~x) == '10'
    # or
    assert repr(x | y) == '0111'
    assert repr(x + y) == '0111'
    # and
    assert repr(x & y) == '0001'
    assert repr(x * y) == '0001'
    # xor
    assert repr(x ^ y) == '0110'
    assert repr(x != y) == '0110'
    assert repr(x - y) == '0110'
    # implication (->)
    assert repr(x >= y) == '1101'
    assert repr(x > y) == '1101'
    # inverse implication (<-)
    assert repr(x <= y) == '1011'
    assert repr(x < y) == '1011'
    # equivalent (<=>)
    assert repr(x == y) == '1001'
    # Sheffer stroke
    assert repr(x // y) == '1110'
    # Peirce's arrow
    assert repr(x % y) == '1000'

    z = Expression('z')
    ((-x - -y) == ((x + z) > (y > z))).print_fullness()
