import pytest
from   literal_exec import NonLiteralAssignmentError, literal_exec

def test_reassignment_delete_nonliteral():
    assert literal_exec(
        "foo = 'value #1'\nfoo = range(42)\n",
        delete_nonliteral=True,
    ) == {}

def test_reassignment_strict_delete_nonliteral():
    with pytest.raises(NonLiteralAssignmentError):
        literal_exec(
            "foo = 'value #1'\nfoo = range(42)\n",
            strict=True,
            delete_nonliteral=True,
        )

def test_reassignment_nodelete_nonliteral():
    assert literal_exec(
        "foo = 'value #1'\nfoo = range(42)\n",
        delete_nonliteral=False,
    ) == {"foo": "value #1"}

def test_reassignment_strict_nodelete_nonliteral():
    with pytest.raises(NonLiteralAssignmentError):
        literal_exec(
            "foo = 'value #1'\nfoo = range(42)\n",
            strict=True,
            delete_nonliteral=False,
        )
