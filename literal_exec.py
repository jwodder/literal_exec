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
        assert len(statement.targets) == 1
        name = statement.targets[0].id
        result[name] = ast.literal_eval(statement.value)
    return result
