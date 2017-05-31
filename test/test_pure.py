# -*- coding: utf-8 -*-
"""
Test evaluation of code containing only literal assignments, literal
expressions, and/or `__future__` imports; such code should be evaluated the
same way regardless of the values of ``strict`` and ``delete_nonliteral``
"""

import pytest
from   six          import PY2, text_type
from   literal_exec import literal_exec

def test_empty(strict, delete_nonliteral):
    assert literal_exec(
        '',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_simple(strict, delete_nonliteral):
    assert literal_exec('''
a_string = 'str'
an_int = 42
a_list = ["foo", "bar", "baz", 23]
a_dict = {"foo": "bar", "baz": 23}
a_tuple = ("foo", "bar", "baz", 23)
''', strict=strict, delete_nonliteral=delete_nonliteral) == {
    "a_string": "str",
    "an_int": 42,
    "a_list": ["foo", "bar", "baz", 23],
    "a_dict": {"foo": "bar", "baz": 23},
    "a_tuple": ("foo", "bar", "baz", 23),
}

def test_set_literal(strict, delete_nonliteral):
    # Python 2's `ast.literal_eval` doesn't handle set literals, so they need
    # to be tested separately.
    assert literal_exec(
        'a_set = {"foo", "bar", "baz", 23}',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"a_set": {"foo", "bar", "baz", 23}}

def test_reassignment(strict, delete_nonliteral):
    assert literal_exec('''
foo = 'value #1'
foo = 'value #2'
''', strict=strict, delete_nonliteral=delete_nonliteral) == {"foo": "value #2"}

def test_semicolons(strict, delete_nonliteral):
    assert literal_exec(
        'foo = "bar"; bar = "baz"',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar", "bar": "baz"}

def test_multi_assign(strict, delete_nonliteral):
    assert literal_exec(
        'foo = bar = "baz"',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "baz", "bar": "baz"}

def test_list_assign(strict, delete_nonliteral):
    assert literal_exec(
        'foo, bar = "baz", "quux"',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "baz", "bar": "quux"}

def test_docstring(strict, delete_nonliteral):
    assert literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
''',
    strict=strict,
    delete_nonliteral=delete_nonliteral,
) == {"__doc__": " This is a module docstring.  It is stored in __doc__. "}

def test_faux_docstring_after_assignment(strict, delete_nonliteral):
    assert literal_exec('''
foo = 'bar'
""" This is not a module docstring.  It is not stored in __doc__. """
''',
    strict=strict,
    delete_nonliteral=delete_nonliteral,
) == {"foo": "bar"}

def test_faux_docstring_after_future_import(strict, delete_nonliteral):
    assert literal_exec('''
from __future__ import unicode_literals
""" This is not a module docstring.  It is not stored in __doc__. """
''',
    strict=strict,
    delete_nonliteral=delete_nonliteral,
) == {}

def test_unicode_literals(strict, delete_nonliteral):
    vals = literal_exec('''
from __future__ import unicode_literals
foo = 'bar'
''',
    strict=strict,
    delete_nonliteral=delete_nonliteral,
)
    assert vals == {"foo": u"bar"}
    assert isinstance(vals["foo"], text_type)

def test_unicode_literals_docstring(strict, delete_nonliteral):
    vals = literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
from __future__ import unicode_literals
''',
    strict=strict,
    delete_nonliteral=delete_nonliteral,
)
    assert vals == {
        "__doc__": u" This is a module docstring.  It is stored in __doc__. "
    }
    assert isinstance(vals["__doc__"], text_type)

def test_concat_str_literals(strict, delete_nonliteral):
    assert literal_exec(
        'foo = "bar" "baz"',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "barbaz"}

def test_ignore_literal_expr(strict, delete_nonliteral):
    assert literal_exec(
        '42',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_ignore_arithmetic_expr(strict, delete_nonliteral):
    assert literal_exec(
        '6*9',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_ignore_set_literal_expr(strict, delete_nonliteral):
    assert literal_exec(
        '{"foo", "bar", "baz", 23}',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_ignore_divzero_expr(strict, delete_nonliteral):
    assert literal_exec(
        '1 / 0',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_error_divzero_assign(strict, delete_nonliteral):
    with pytest.raises(ZeroDivisionError):
        literal_exec(
            'x = 1 / 0',
            strict=strict,
            delete_nonliteral=delete_nonliteral,
        )

@pytest.mark.skipif(PY2, reason='Python 3 only')
def test_ellipsis(strict, delete_nonliteral):
    assert literal_exec(
        'elision = ...',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"elision": Ellipsis}

def test_comment(strict, delete_nonliteral):
    assert literal_exec(
        'foo = "bar"\n'
        '#bar = "baz"\n'
        'baz = "quux"\n',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar", "baz": "quux"}

def test_unicode_input(strict, delete_nonliteral):
    vals = literal_exec(
        u'snowman = "☃"',
        strict=strict,
        delete_nonliteral=delete_nonliteral,
    )
    assert vals == {"snowman": "☃"}
    assert isinstance(vals["snowman"], str)

# error on __future__ import in bad location
# source file encodings
# exec'ing bytes in Python 3?
# a, *b, c = ... (Python 3.0+)
# concatenation of a bytes literal with an adjacent unicode literal?
# unicode literals
# bytes literals
# variable annotations?
# complex number literals
