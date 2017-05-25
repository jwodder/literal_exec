__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'literal-exec@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/literal_exec'

import ast

def literal_execfile(path):
    with open(path) as fp:
        src = fp.read()
    return literal_exec(src)

def literal_exec(src):
    top_level = ast.parse(src)
    result = {}
    for statement in top_level.body:
        if not isinstance(statement, ast.Assign):
            continue
        value = ast.literal_eval(statement.value)
        for target in statement.targets:
            result[target.id] = value
    return result
