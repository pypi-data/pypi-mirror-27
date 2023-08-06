Bplustree
=========

.. image:: https://travis-ci.org/NicolasLM/bplustree.svg?branch=master
    :target: https://travis-ci.org/NicolasLM/bplustree
.. image:: https://coveralls.io/repos/github/NicolasLM/bplustree/badge.svg?branch=master
    :target: https://coveralls.io/github/NicolasLM/bplustree?branch=master

An on-disk B+tree for Python 3.

Quickstart
----------

Install Bplustree with pip::

   pip install bplustree

Create a B+tree index stored on a file and use it with:

.. code:: python

    >>> from bplustree import BPlusTree
    >>> tree = BPlusTree(filename='/tmp/bplustree.db', order=50)
    >>> tree.insert(1, b'foo')
    >>> tree.insert(2, b'bar')
    >>> tree.get(1)
    b'foo'
    >>> for i in tree:
    ...     print(i)
    ...
    1
    2
    >>> tree.close()

License
-------

MIT
Copyright (c) 2017 Nicolas Le Manchet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

