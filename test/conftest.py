import pytest
from   literal_exec import NonLiteralAssignmentError

def pytest_generate_tests(metafunc):
    if 'strict' in metafunc.fixturenames:
        metafunc.parametrize("strict", [False, True])
    if 'strict_xfail' in metafunc.fixturenames:
        metafunc.parametrize("strict_xfail", [
            False,
            pytest.param(True, marks=pytest.mark.xfail(strict=True, raises=NonLiteralAssignmentError)),
        ])
    if 'delete_nonliteral' in metafunc.fixturenames:
        metafunc.parametrize("delete_nonliteral", [False, True])
