#!/usr/bin python

# Copyright 2015 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import doctest
import pkgutil
import sys

import papersize

def load_module(module_finder, name):
    """Load and return module `name`."""
    if sys.version_info >= (3, 4, 0):
        return module_finder.find_spec(name).loader.load_module()
    return module_finder.find_module(name).load_module(name)

def load_tests(__loader, tests, __pattern):
    """Load tests (doctests).
    """
    # Loading doctests
    tests.addTests(doctest.DocTestSuite(papersize))
    for module_finder, name, __is_pkg in pkgutil.walk_packages(
            papersize.__path__,
            prefix="{}.".format(papersize.__name__),
        ):
        if name in sys.modules:
            module = sys.modules[name]
        else:
            try:
                module = load_module(module_finder, name)
            except ImportError:
                continue
        try:
            tests.addTests(doctest.DocTestSuite(module))
        except ValueError:
            # No docstring, or no doctests in the docstrings
            pass

    return tests
