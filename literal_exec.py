__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'literal-exec@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/literal_exec'

import ast

def literal_execfile(path, strict=False, delete_nonliteral=True):
    with open(path) as fp:
        src = fp.read()
    return literal_exec(src, strict=strict, delete_nonliteral=delete_nonliteral)

def literal_exec(src, strict=False, delete_nonliteral=True):
    """
    :param bool strict: If true, statements other than literal value
        assignments, constant expressions, and `__future__` imports will cause
        a `NonLiteralAssignmentError` to be raised
    :param bool delete_nonliteral: If true, an assignment of the form ``x =
        nonliteral_expression`` will cause any previous assignments to ``x`` to
        be discarded
    """
    top_level = ast.parse(src)
    result = {}
    for statement in top_level.body:
        if not isinstance(statement, ast.Assign):
            if strict:
                raise NonLiteralAssignmentError()
            continue
        value = ast.literal_eval(statement.value)
        for target in statement.targets:
            result[target.id] = value
    return result

class NonLiteralAssignmentError(ValueError):
    ### TODO: Come up with a better name
    pass
