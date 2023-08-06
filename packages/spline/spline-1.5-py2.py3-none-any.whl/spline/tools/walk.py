"""
   Iterating Python data more easily.

.. module:: walk
    :platform: all
    :synopis: iterating Python data more easily.
.. moduleauthor:: Thomas Lehmann <thomas.lehmann.private@gmail.com>

   =======
   License
   =======
   Copyright (c) 2017 Thomas Lehmann

   Permission is hereby granted, free of charge, to any person obtaining a copy of this
   software and associated documentation files (the "Software"), to deal in the Software
   without restriction, including without limitation the rights to use, copy, modify, merge,
   publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
   to whom the Software is furnished to do so, subject to the following conditions:
   The above copyright notice and this permission notice shall be included in all copies
   or substantial portions of the Software.
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


class Walker(object):
    """
    Walking of Pythonic data.

    >>> wdata = Walker({'person':{'name': 'Hercule', 'surname': 'Poirot'}})
    >>> wdata.person.name == 'Hercule'
    True
    >>> wdata.person.surname == 'Poirot'
    True
    """

    def __init__(self, data):
        """initializer walker with data."""
        self.data = data

    def __getattr__(self, key):
        """Organizing walking of dictionaries via direct field access."""
        value = self.data[key]
        if isinstance(value, dict):
            return Walker(value)
        return value
