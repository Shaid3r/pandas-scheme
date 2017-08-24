#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""Tests for taurus.core.pandas.test.test_pdsvalidator..."""

from taurus.external import unittest
from taurus.core.test import (valid, invalid, names,
                              AbstractNameValidatorTestCase)
from tpds.pdsvalidator import (PandasAuthorityNameValidator,
                               PandasDeviceNameValidator,
                               PandasAttributeNameValidator)


@valid(name='pds://localhost')
@invalid(name='pds:')
@names(name='pds://localhost',
       out=('pds://localhost', '//localhost', 'localhost'))
class PandasAuthValidatorTestCase(AbstractNameValidatorTestCase,
                                  unittest.TestCase):
    validator = PandasAuthorityNameValidator


@valid(name='pds://localhost/path/to/file.csv')
@valid(name='pds:/path/to/file.csv')
@valid(name='pds:/path/to/file?format=csv')  # TMP specifying format
@valid(name='pds:/path/to/file{csv}')  # TMP specifying format
@valid(name='pds:/pa\ th/to/file.csv')  # Escaped spaces
@invalid(name='pds:/pa th/to/file.csv')  # White spaces are not accepted
class PandasDevValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = PandasDeviceNameValidator


@valid(name='pds://localhost/path/to/file.csv::/"column0":')  # First column
@valid(name='pds://localhost/path/to/file.csv::/0:')  # First column with index
# First column without colon
@valid(name='pds://localhost/path/to/file.csv::/"column0"')
@valid(name='pds://localhost/path/to/file.csv::/:0')  # First row
@valid(name='pds://localhost/path/to/file.csv::/"column0":0')  # First cell
# Multiple columns
@valid(name='pds://localhost/path/to/file.csv::/"column0":;"column2:"')
# Multiple columns with indexes
@valid(name='pds://localhost/path/to/file.csv::/0:;2:')
# Multiple columns with indexes without colons
@valid(name='pds://localhost/path/to/file.csv::/0;2')
# Multiple columns without colons
@valid(name='pds://localhost/path/to/file.csv::/"column0";"column2"')
# Multiple columns mixed notation
@valid(name='pds://localhost/path/to/file.csv::/"column0":;"column2"')
# Cross section (top left cell|bottom right cell)
@valid(name='pds://localhost/path/to/file.csv::/"column0":3|"column2":7')
# Multiple cross sections
@valid(name='pds://localhost/path/to/file.csv::'
            '/"column0":3|"column2":7;column0":3|"column2":7')
@invalid(name='pds://localhost/path/to/file.csv::')  # Empty attribute
class PandasAttrValidatorTestCase(AbstractNameValidatorTestCase,
                                  unittest.TestCase):
    validator = PandasAttributeNameValidator

if __name__ == "__main__":
    unittest.main()
