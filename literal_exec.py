""" Parse literal variable assignments from source files """

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'literal-exec@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/literal_exec'

import ast
import sys

def literal_execfile(path, strict=False, delete_nonliteral=True):
    with open(path, 'rb') as fp:
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
    doc = ast.get_docstring(top_level, clean=False)
    if doc is not None:
        result["__doc__"] = doc
    for statement in top_level.body:
        if isinstance(statement, ast.Assign):
            try:
                value = literal_eval(statement.value)
            except (TypeError, ValueError):
                if strict:
                    raise NonLiteralAssignmentError()
                elif delete_nonliteral:
                    for target in statement.targets:
                        result.pop(target.id, None)
            else:
                for target in statement.targets:
                    result[target.id] = value
        elif isinstance(statement, ast.Expr):
            if strict:
                try:
                    literal_eval(statement.value)
                except (TypeError, ValueError):
                    raise NonLiteralAssignmentError()
        elif isinstance(statement, ast.ImportFrom) and \
                statement.module == '__future__' and not statement.level:
            pass
        elif isinstance(statement, (ast.Import, ast.ImportFrom)):
            if strict:
                raise NonLiteralAssignmentError()
            elif delete_nonliteral:
                for alias in statement.names:
                    result.pop(alias.asname or alias.name, None)
        elif isinstance(statement, ast.Pass):
            pass
        elif strict:
            raise NonLiteralAssignmentError()
    return result

def literal_eval(expr):
    """
    Like `ast.literal_eval`, except it also supports:

    - set literals (not supported by Python 2's `ast.literal_eval`)
    - ``...`` (Python 3)
    """
    try:
        return ast.literal_eval(expr)
    except (TypeError, ValueError):
        if isinstance(expr, str):
            expr = ast.parse(expr, mode='eval')
            assert isinstance(expr, ast.Expression)
            expr = expr.body
        elif isinstance(expr, ast.Expression):
            expr = expr.body
        elif not isinstance(expr, ast.expr):
            raise TypeError
        if isinstance(expr, ast.Ellipsis):
            return Ellipsis
        elif isinstance(expr, ast.Set) and sys.version_info[0] == 2:
            return set(literal_eval(e) for e in expr.elts)
        else:
            raise ValueError

class NonLiteralAssignmentError(ValueError):
    ### TODO: Come up with a better name
    pass
