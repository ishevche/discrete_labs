from expression import Expression

"""
Usage:
    x = Expression('x')
    y = Expression('y')
    print(x ^ y)

Boolean operators:
    not: ~ or -
    or: | or +
    and: & or *
    xor: ^ or != or -
    ->: >= or >
    <-: <= or <
    <=>: ==
    Sheffer stroke: //
    Peirce's arrow: %
"""

a = Expression('a')
b = Expression('b')
c = Expression('c')
d = Expression('d')

print(((a + b) * c).print_fullness())
