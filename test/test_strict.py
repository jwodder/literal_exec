from   literal_exec import NonLiteralAssignmentError, literal_exec
import pytest
from   six          import text_type

def test_simple():
    assert literal_exec('''
a_string = 'str'
an_int = 42
a_list = ["foo", "bar", "baz", 23]
a_dict = {"foo": "bar", "baz": 23}
a_tuple = ("foo", "bar", "baz", 23)
a_set = {"foo", "bar", "baz", 23}
''', strict=True) == {
    "a_string": "str",
    "an_int": 42,
    "a_list": ["foo", "bar", "baz", 23],
    "a_dict": {"foo": "bar", "baz": 23},
    "a_tuple": ("foo", "bar", "baz", 23),
    "a_set": {"foo", "bar", "baz", 23},
}

def test_reassignment():
    assert literal_exec('''
foo = 'value #1'
foo = 'value #2'
''', strict=True) == {"foo": "value #2"}

def test_semicolons():
    assert literal_exec('foo = "bar"; bar = "baz"', strict=True) \
        == {"foo": "bar", "bar": "baz"}

def test_multi_assign():
    assert literal_exec('foo = bar = "baz"', strict=True) \
        == {"foo": "baz", "bar": "baz"}

def test_list_assign():
    assert literal_exec('foo, bar = "baz", "quux"', strict=True) \
        == {"foo": "baz", "bar": "quux"}

def test_strict_nonliteral():
    with pytest.raises(NonLiteralAssignmentError):
        literal_exec("foo = 'bar'\nbar = range(42)\nbaz = 42\n", strict=True)

def test_list_assign_strict_nonliteral():
    with pytest.raises(NonLiteralAssignmentError):
        assert literal_exec('foo, bar, baz = "quux", range(42), "glarch"',
                            strict=True)

def test_docstring():
    assert literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
''', strict=True) \
    == {"__doc__": " This is a module docstring.  It is stored in __doc__. "}

def test_faux_docstring_after_assignment():
    assert literal_exec('''
foo = 'bar'
""" This is not a module docstring.  It is not stored in __doc__. """
''', strict=True) == {"foo": "bar"}

def test_faux_docstring_after_import():
    with pytest.raises(NonLiteralAssignmentError):
        literal_exec('''
import sys
""" This is not a module docstring.  It is not stored in __doc__. """
''', strict=True)

def test_faux_docstring_after_future_import():
    assert literal_exec('''
from __future__ import unicode_literals
""" This is not a module docstring.  It is not stored in __doc__. """
''', strict=True) == {}

def test_unicode_literals():
    vals = literal_exec('''
from __future__ import unicode_literals
foo = 'bar'
''', strict=True)
    assert vals == {"foo": u"bar"}
    assert isinstance(vals["foo"], text_type)

def test_unicode_literals_docstring():
    vals = literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
from __future__ import unicode_literals
''', strict=True)
    assert vals == {
        "__doc__": u" This is a module docstring.  It is stored in __doc__. "
    }
    assert isinstance(vals["__doc__"], text_type)

# comments
# imports
# function & class definitions
# concatenation of adjacent string literals
