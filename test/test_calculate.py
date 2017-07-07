import pytest
from   literal_exec import calculate

@pytest.mark.parametrize('expr,value', [
    ('2 + 3', 5),
    ('2 * 3', 6),
    ('2 // 3', 0),
    ('2 - 3', 1),
    ('2 % 3', 2),
    ('2 & 3', 2),
    ('2 | 3', 3),
    ('2 ^ 3', 1),
    ('2 << 3', 16),
    ('2 >> 3', 0),
    ('2 ** 3', 8),
    ('2 + 3 * 5 + 7', 24),
    ('(2 + 3) * 5 + 7', 32),
    ('2 + 3 * (5 + 7)', 38),
    ('(2 + 3) * (5 + 7)', 60),
    ('-2', -2),
    ('2 + - 3', -1),
    ('- 2 + 3', 1),
    ('~2', -3),
    ('2 + ~ 3', -2),
    ('~ 2 + 3', 0),
    ('+2', -3),
    ('2++3', 5),
    ('+2+3', 5),
])
def test_calculate(expr, value):
    assert calculate(expr) == value

def test_divzero():
    with pytest.raises(ZeroDivisionError):
        calculate('1 / 0')

# __div__ with & without future-division
# __matmul__ ?
# operations on strings
# operations on sets
