from literal_exec import literal_exec

def test_simple():
    assert literal_exec('''
a_string = 'str'
an_int = 42
a_list = ["foo", "bar", "baz", 23]
a_dict = {"foo": "bar", "baz": 23}
a_tuple = ("foo", "bar", "baz", 23)
a_set = {"foo", "bar", "baz", 23}
''') == {
    "a_string": "str",
    "an_int": 42,
    "a_list": ["foo", "bar", "baz", 23],
    "a_dict": {"foo": "bar", "baz": 23},
    "a_tuple": ("foo", "bar", "baz", 23),
    "a_set": {"foo", "bar", "baz", 23},
}

def test_reassignment():
    assert literal_exec('''
foo = 'value #1'
foo = 'value #2'
''') == {"foo": "value #2"}

def test_semicolons():
    assert literal_exec('foo = "bar"; bar = "baz"') \
        == {"foo": "bar", "bar": "baz"}

def test_multi_assign():
    assert literal_exec('foo = bar = "baz"') == {"foo": "baz", "bar": "baz"}

def test_list_assign():
    assert literal_exec('foo, bar = "baz", "quux"') \
        == {"foo": "baz", "bar": "quux"}

def test_skip_nonliteral():
    assert literal_exec('''
foo = 'bar'
bar = range(42)
baz = 42
''') == {"foo": "bar", "baz": 42}
