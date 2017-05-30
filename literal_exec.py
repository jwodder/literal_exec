""" Parse literal variable assignments from source files """

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
    doc = ast.get_docstring(top_level, clean=False)
    if doc is not None:
        result["__doc__"] = doc
    for statement in top_level.body:
        if isinstance(statement, ast.Assign):
            try:
                value = ast.literal_eval(statement.value)
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
                    ast.literal_eval(statement.value)
                except (TypeError, ValueError):
                    raise NonLiteralAssignmentError()
        elif isinstance(statement, ast.ImportFrom):
            if statement.module == '__future__' and not statement.level:
                pass
            elif strict:
                raise NonLiteralAssignmentError()
        elif isinstance(statement, ast.Pass):
            pass
        elif strict:
            raise NonLiteralAssignmentError()
    return result

class NonLiteralAssignmentError(ValueError):
    ### TODO: Come up with a better name
    pass
