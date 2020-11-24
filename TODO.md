- "Arithmetic" ("constant"?) expressions should always be supported.  They're
  just literals written out the long way, after all!
    - On second thought, no.

- Handle `del`

- Tests
    - Constants <https://docs.python.org/3/library/constants.html>:
        - Parsing
        - Error when (only certain constants?) are assigned to
        - Handling references to reassignable constants after they've been
          reassigned
    - https://stackoverflow.com/q/30147165/744178
    - reading from a file with an encoding declaration
    - assigning to a subscript
    - list/tuple expressions with PEP 448 unpacking
- Features & correctness
    - To fix: `ast.literal_eval` can't parse sets in Python 2
- Docstrings
    - module docstring
- Release
    - README badges & links

- Add an option for erroring when a literal variable is reassigned a nonliteral?

- Store variable annotations in `__annotations__`?
- Rethink the name "`delete_nonliteral`"
- Add an option for setting `__future__` directives to use when `exec`'ing?
- Include `__name__`?
- Include `__file__`?
- Include `__dict__`?

- Possible evaluation modes/"levels":
    - strict: error on anything that isn't a literal assignment
    - ignore anything that isn't a literal assignment
    - non-literal assignments cause variable deletion

    - Treat literal `__setitem__` assignments as normal literal assignments
        - support literal `__setitem__` assignments
            - TODO: Raise an informative error when the user tries a literal
              __setitem__ assignment that fails for type reasons
    - Treat literal `__setitem__` assignments as non-literal assignments
        - error on literal `__setitem__` assignments
        - ignore literal `__setitem__` assignments
        - literal `__setitem__` assignments cause deletion of the parent
          variable


- Nonliteral assignments to detect and delete:
    - inside blocks (including all branches thereof)
    - `global`?
    - mutable method calls? (e.g., `list.append`)

- Possible contructs to support evaluation of:
    - arithmetic expressions
        - Define a new public function for this
    - assignment from other literal variables
        - assignment from subscripted literal variables
        - Give `literal_exec` a `namespace={}` argument for setting the initial
          (read-only?) namespace
        - Note: Be careful with how this feature interacts with
          `delete_nonliteral=False`
    - assignments inside blocks with conditions that can be evaluated
      statically
        - literal conditions
        - arithmetic conditions
        - conditions referencing prior literal variables
    - format strings?

- Things to flat-out ignore:
    - `globals()`
    - infinite loops?
    - `raise`?
        - `assert`
    - `from foo import *`
