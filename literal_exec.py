__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'literal-exec@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/literal_exec'

import ast

def literal_execfile(path, strict=False):
    with open(path) as fp:
        src = fp.read()
    return literal_exec(src, strict=strict)

def literal_exec(src, strict=False):
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
