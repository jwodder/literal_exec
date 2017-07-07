"""
Test evaluation of code containing assignments of nonliteral expressions to
variables that were previously assigned literal expressions, i.e., code whose
evaluation changes depending on the value of ``delete_nonliteral`` (and which
fails when ``strict=True``)
"""

from   literal_exec import literal_exec

def test_reassignment(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nfoo = range(42)\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_conditional_reassignment(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\n"
        "if 1 == 1:\n"
        "    foo = 'quux'\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nimport foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_import_as_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nbaz = 'quux'\nimport baz as foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"baz": "quux"}
    else:
        assert vals == {"foo": "bar", "baz": "quux"}

def test_from_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nquux = 'baz'\nfrom quux import foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"quux": "baz"}
    else:
        assert vals == {"foo": "bar", "quux": "baz"}

def test_from_import_as_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\n"
        "quux = 'baz'\n"
        "xyzzy = 'plugh'\n"
        "from quux import foo as xyzzy\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"foo": "bar", "quux": "baz"}
    else:
        assert vals == {"foo": "bar", "quux": "baz", "xyzzy": "plugh"}

def test_from_relative_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nquux = 'baz'\nfrom .quux import foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"quux": "baz"}
    else:
        assert vals == {"foo": "bar", "quux": "baz"}

def test_from_dot_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nfrom . import foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_import_dotted(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nbaz = 'quux'\nimport foo.baz\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"baz": "quux"}
    else:
        assert vals == {"foo": "bar", "baz": "quux"}

def test_import_dotted_as(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nbaz = 'quux'\nxyzzy = 'plugh'\nimport foo.baz as xyzzy\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {"foo": "bar", "baz": "quux"}
    else:
        assert vals == {"foo": "bar", "baz": "quux", "xyzzy": "plugh"}

# multiple variables are assigned literal values, only some are later reassigned nonliterals
# some imported names don't mask any variables
# import foo, bar
# x = y = ...; x = func
# function & class definitions
# `for ... in` variables
# comprehension variables in Python 2?
# `except` variables in Python 2?
# augmented assignment
# splat assignment (Python 3)
# list assignment with a different number of items on the left & right
# list assignment with an actual list on the left
