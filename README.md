treelib
-------

Tree implementation in python: simple for you to use.

## Modifications

```sh
treelib/tree.py/Tree.show()
```

The original treelib only supports `data_property` argument as a `string`, and prints the corresponding attribute of the node data. This modification allows `data_property` argument to be a `list`, and prints the corresponding attributes in the list. For instance:

```python
sent_trees[5].show(data_property=["text", "dep_"])
```

------

[![Build Status](https://travis-ci.org/caesar0301/treelib.svg?branch=master)](https://travis-ci.org/caesar0301/treelib)
[![Documentation Status](https://readthedocs.org/projects/treelib/badge/?version=latest)](http://treelib.readthedocs.io/en/latest/?badge=latest)
[![Status](https://img.shields.io/pypi/status/treelib.svg)](https://pypi.python.org/pypi/treelib)
[![Latest](https://img.shields.io/pypi/v/treelib.svg)](https://pypi.python.org/pypi/treelib)
[![PyV](https://img.shields.io/pypi/pyversions/treelib.svg)](https://pypi.python.org/pypi/treelib)
[![PyPI download month](https://img.shields.io/pypi/dm/treelib.svg)](https://pypi.python.org/pypi/treelib/)
[![GitHub contributors](https://img.shields.io/github/contributors/caesar0301/treelib.svg)](https://GitHub.com/caesar0301/treelib/graphs/contributors/)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/caesar0301/treelib.svg)](https://GitHub.com/caesar0301/treelib/pull/)
[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/caesar0301/treelib.svg)](https://GitHub.com/caesar0301/treelib/pull/)




Quick Start
-----------

    sudo easy_install -U treelib

Documentation
-------------

For installation, APIs and examples, see http://treelib.readthedocs.io/en/latest/

Update
-------

* 2017-08-10: Abandon supporting Python 3.2 since v1.4.0.
* 2012-07-07: First published.


Contributors
------------

> Brett Alistair Kromkamp (brettkromkamp@gmail.com): Post basic idea online.
>
> Xiaming Chen (chenxm35@gmail.com): Finished primary parts and made the library freely public.
>
> Holger Bast (holgerbast@gmx.de): Replaced list with `dict` for fast node index and optimized the performance.
>
> Ilya Kuprik (ilya-spy@ynadex.ru): Added ZIGZAG tree-walk algorithm to tree traversal.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)

