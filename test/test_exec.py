from   literal_exec import literal_exec
from   six          import text_type

def test_simple():
    assert literal_exec('''
a_string = 'str'
an_int = 42
a_list = ["foo", "bar", "baz", 23]
a_dict = {"foo": "bar", "baz": 23}
a_tuple = ("foo", "bar", "baz", 23)
a_set = {"foo", "bar", "baz", 23}
''') == {
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
''') == {"foo": "value #2"}

def test_semicolons():
    assert literal_exec('foo = "bar"; bar = "baz"') \
        == {"foo": "bar", "bar": "baz"}

def test_multi_assign():
    assert literal_exec('foo = bar = "baz"') == {"foo": "baz", "bar": "baz"}

def test_list_assign():
    assert literal_exec('foo, bar = "baz", "quux"') \
        == {"foo": "baz", "bar": "quux"}

def test_skip_nonliteral():
    assert literal_exec("foo = 'bar'\nbar = range(42)\nbaz = 42\n") \
        == {"foo": "bar", "baz": 42}

def test_list_assign_skip_nonliteral():
    assert literal_exec('foo, bar, baz = "quux", range(42), "glarch"') \
        == {"foo": "quux", "baz": "glarch"}

def test_docstring():
    assert literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
''') == {"__doc__": " This is a module docstring.  It is stored in __doc__. "}

def test_faux_docstring_after_assignment():
    assert literal_exec('''
foo = 'bar'
""" This is not a module docstring.  It is not stored in __doc__. """
''') == {"foo": "bar"}

def test_faux_docstring_after_import():
    assert literal_exec('''
import sys
""" This is not a module docstring.  It is not stored in __doc__. """
''') == {}

def test_faux_docstring_after_future_import():
    assert literal_exec('''
from __future__ import unicode_literals
""" This is not a module docstring.  It is not stored in __doc__. """
''') == {}

def test_unicode_literals():
    vals = literal_exec('''
from __future__ import unicode_literals
foo = 'bar'
''')
    assert vals == {"foo": u"bar"}
    assert isinstance(vals["foo"], text_type)

def test_unicode_literals_docstring():
    vals = literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
from __future__ import unicode_literals
''')
    assert vals == {
        "__doc__": u" This is a module docstring.  It is stored in __doc__. "
    }
    assert isinstance(vals["__doc__"], text_type)

def test_reassignment_delete_nonliteral():
    assert literal_exec('''
foo = 'value #1'
foo = range(42)
''', delete_nonliteral=True) == {}

def test_reassignment_nodelete_nonliteral():
    assert literal_exec('''
foo = 'value #1'
foo = range(42)
''', delete_nonliteral=False) == {"foo": "value #1"}

def test_re_reassignment_delete_nonliteral():
    assert literal_exec('''
foo = 'value #1'
foo = range(42)
foo = 'value #2'
''', delete_nonliteral=True) == {"foo": "value #2"}

def test_re_reassignment_nodelete_nonliteral():
    assert literal_exec('''
foo = 'value #1'
foo = range(42)
foo = 'value #2'
''', delete_nonliteral=False) == {"foo": "value #2"}

# unicode_literals in bad location
# comments
# ignoring imports
# function & class definitions
# concatenation of adjacent string literals
# source file encodings
# exec'ing Unicode in Python 2?
# exec'ing bytes in Python 3?
# raising/causing an error in the middle of the source?
