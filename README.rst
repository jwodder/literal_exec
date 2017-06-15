.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://travis-ci.org/jwodder/literal_exec.svg?branch=master
    :target: https://travis-ci.org/jwodder/literal_exec

.. image:: https://coveralls.io/repos/github/jwodder/literal_exec/badge.svg?branch=master
    :target: https://coveralls.io/github/jwodder/literal_exec?branch=master

.. image:: https://img.shields.io/github/license/jwodder/literal_exec.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/literal_exec>`_
| `Issues <https://github.com/jwodder/literal_exec/issues>`_

*This is very much a work in progress.  Until the "build" badge above turns
green, assume none of this works.*

``literal_exec`` provides a Python function of the same name that takes the
source for a Python module and — without running any of the code in that module
— extracts all assignments of the form ``variable = "literal expression"``,
returning a ``dict`` of the results.  It can be used for parsing configuration
files written in Python without creating security holes or used as part of yet
another solution to the problem of `single-sourcing Python project versions
<https://packaging.python.org/single_source_version/>`_ (though the latter use
won't really become fully viable until ``pyproject.toml`` support is more
widespread).


Intended Behavior
=================

- The ``literal_exec`` function takes a string of Python code (assumed to be a
  module) to parse.  ``literal_execfile`` takes a path to a file.  They both
  return a dictionary mapping variable names to variable values.

  - Both functions also take optional ``strict`` (default ``False``) and
    ``delete_nonliteral`` (default ``True``) boolean arguments, described
    below.

- Input is parsed as code for the same Python version as ``literal_exec`` is
  running under (so trying to parse strictly Python 2 code in Python 3 or *vice
  versa* won't work).

- The only ``__future__`` imports that are honored are ``print_function`` (for
  its effect on parsing) and ``unicode_literals`` (for its effect on string
  literal types); all others are ignored.

- If a variable ``x`` is assigned a literal value (i.e., something that can be
  parsed with ``ast.literal_eval``) at module scope and nothing else in the
  code modifies ``x`` afterwards, then ``literal_exec`` will return ``"x"``
  with said value.  If something *does* modify ``x`` afterwards, either setting
  it to a non-literal expression or else modifying it conditionally, and if
  ``delete_nonliteral`` is true, then ``literal_exec`` will try its hardest to
  detect that modification and unset ``x`` accordingly; if
  ``delete_nonliteral`` is false, such nonliteral assignments will simply be
  ignored.

- If the input has a module docstring, it is assigned to the ``"__doc__"`` key.

- The following are completely ignored:

  - blank lines
  - comments (except possibly for an encoding declaration)
  - non-docstring statements consisting entirely of literal values and
    (optionally) operations upon them (e.g., ``2 + 2``, ``'foo' * 5``)
  - ``pass`` statements

- If ``strict`` is ``True``, a statement that is not a literal assignment, a
  ``__future__`` import, a docstring, or otherwise ignored will cause a
  ``NonLiteralAssignmentError`` to be raised.

- The only effect of ``from foo import *`` is to cause a
  ``NonLiteralAssignmentError`` to be raised if ``strict`` is ``True``.


Related Prior Art
=================
- https://github.com/takluyver/astsearch
- ``rwt``: Extracting ``__requires__``: https://git.io/vHaJA
- http://softwarerecs.stackexchange.com/q/38958/19264
