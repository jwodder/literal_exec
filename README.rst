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


Related Prior Art
=================
- https://github.com/takluyver/astsearch
- ``rwt``: Extracting ``__requires__``: https://git.io/vHaJA
- http://softwarerecs.stackexchange.com/q/38958/19264
