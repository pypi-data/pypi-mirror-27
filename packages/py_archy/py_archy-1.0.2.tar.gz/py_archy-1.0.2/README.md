
# PyArchy

Implementation of the popular node-archy tool in python.
Draws good looking trees and lists on the command line.

[![PyPI](https://img.shields.io/pypi/v/py_archy.svg)](https://pypi.python.org/pypi?name=py_archy&:action=display)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

[The original Archy on NPM](https://www.npmjs.com/package/archy)

### Installation

```
pip install py_archy
```

### Usage

```
>>> from pyarchy import archy
>>>
>>> tree = { 'nodes' : [{ 'nodes' : ['a','b','c'], 'label' : 'bar'}, 'bizz'], 'label' : 'foo'}
>>>
>>> print( archy(tree)) 
foo                                                                   
├─┬ bar
│ ├── a
│ ├── b
│ └── c
└── bizz 

>>> print( archy(tree, unicode=False))
+-- bar
| +-- a 
| +-- b                                                                                                   
| `-- c 
`-- bizz
```

### Credits
This package was created with Cookiecutter.

