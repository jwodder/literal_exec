import pytest
from   literal_exec import NonLiteralAssignmentError

def parameter_fixture(*params):
    return pytest.fixture(params=params)(lambda request: request.param)

strict = delete_nonliteral = parameter_fixture(False, True)

strict_xfail = parameter_fixture(
    False,
    pytest.param(
        True,
        marks=pytest.mark.xfail(strict=True, raises=NonLiteralAssignmentError),
    ),
)
