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
        "foo = 'bar'\nimport baz as foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_from_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nfrom quux import foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

def test_from_relative_import_over(strict_xfail, delete_nonliteral):
    vals = literal_exec(
        "foo = 'bar'\nfrom .quux import foo\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    )
    if delete_nonliteral:
        assert vals == {}
    else:
        assert vals == {"foo": "bar"}

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

# multiple variables are assigned literal values, only some are later reassigned nonliterals
# assign nonliteral, reassign literal
# some imported names don't mask any variables
# import foo.bar
# import foo, bar
# from ... import ... as ...
# from ... import *
