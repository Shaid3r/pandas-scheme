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

"""Tests for taurus.core.taurus_pandas.test.test_pdsvalidator..."""

from taurus.external import unittest
from taurus.core.test import (valid, invalid, names,
                              AbstractNameValidatorTestCase)
from taurus_pandas.pdsvalidator import (PandasAuthorityNameValidator,
                                        PandasDeviceNameValidator,
                                        PandasAttributeNameValidator)


# =========================================================================
#  Tests for Pandas Authority name validation
# =========================================================================
@valid(name='pds://localhost')
@valid(name='pds-csv://localhost')
@valid(name='pds-xls://localhost')
# @valid(name='pds-hdf://localhost')  # TODO later
@invalid(name='pds:')
@names(name='pds://localhost',
       out=('pds://localhost', '//localhost', 'localhost'))
@names(name='pds-csv://localhost',
       out=('pds-csv://localhost', '//localhost', 'localhost'))
class PandasAuthValidatorTestCase(AbstractNameValidatorTestCase,
                                  unittest.TestCase):
    validator = PandasAuthorityNameValidator


# =========================================================================
#  Tests for Pandas Device name validation
# =========================================================================
@valid(name='pds://localhost/path/to/file.csv')
@valid(name='pds:/path/to/file.csv')
@valid(name='pds:/path-to/file.csv')
@valid(name='pds:/path_to/file.csv')
@valid(name='pds:/file.csv')
@valid(name='pds:/path/to/fi-le.csv')
@valid(name='pds:/path/to/fi_le.csv')
@valid(name='pds:/path/to/f.i.l.e..csv')
@valid(name='pds:/path/to/f-i_l.e.csv')
@valid(name='pds:/path/../to/file.csv')
@valid(name='pds:///path/to/file.csv')
@valid(name='pds://////path/to/file.csv')
@valid(name='pds-csv:/path/to/file')  # Specifying format
@valid(name='pds-xls:/path/to/file')  # Specifying format
# Escaped spaces (spaces not accepted for now)
# @valid(name='pds:/pa\ th/to/file.csv')
@valid(name='pds:/C:/Path/To/File.csv')
@valid(name='pds:/../file.csv')
@invalid(name='pds:path/to/file.csv')  # Missing first "/"
@invalid(name='pds:../file.csv')  # Missing first "/"
@invalid(name='pds:/pa th/to/file.csv')  # White spaces are not accepted
@invalid(name='pds:/path/to/file.csv/')  # Has extra final "/"
@invalid(name='pds:/path/to/file.csv::')  # Has extra final "::"
@invalid(name='pds:/path/to/file.csv::/"column0":')  # It is an attr URI
@invalid(name='pds://path/to/file.csv')  # Path cannot start with "//"
@invalid(name='pds:/1:/to/file.csv')  # Windows unit must be a letter
@names(name='pds:/path/to/file.csv',
       out=('pds://localhost/path/to/file.csv', '/path/to/file.csv',
            'file.csv'))
@names(name='pds:/a/../c/file.csv',
       out=('pds://localhost/c/file.csv', '/c/file.csv',
            'file.csv'))
@names(name='pds:/../file.csv',
       out=('pds://localhost/file.csv', '/file.csv',
            'file.csv'))
@names(name='pds:/foo/./file.csv',
       out=('pds://localhost/foo/file.csv', '/foo/file.csv',
            'file.csv'))
@names(name='pds:/foo/.../file.csv',
       out=('pds://localhost/foo/.../file.csv', '/foo/.../file.csv',
            'file.csv'))
class PandasDevValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = PandasDeviceNameValidator


# =========================================================================
#  Tests for Pandas Attribute name validation
# =========================================================================
@valid(name='pds-csv:/path/to/file::["column0"]')  # Get column
@valid(name='pds-csv:/path/to/file::["column0","column1",2]')  # Get 3 columns
# Recognize format and get all data
@valid(name='pds://localhost/path/to/file.csv::')
# Column label should be inside brackets
@invalid(name='pds-csv://localhost/path/to/file::"column0"')
@valid(name='pds-xls:/path/to/file::')  # Get all data from 1-st sheet
@valid(name='pds-xls:/path/to/file::"Sheet1"')  # Get all data from "Sheet1"
# Get column "Col1" from "Sheet1"
@valid(name='pds-xls:/path/to/file::"Sheet1";"Col1"')

# @valid(name='pds-csv://localhost/path/to/file::"column0"|[x for x in range(3)]')
# @valid(name='pds-csv://localhost/path/to/file::"column0"')
# @valid(name='pds://localhost/path/to/file.csv::/"column0":')  # First column
# @valid(name='pds:/path/to/file.csv::/0:')  # First column with index
# @valid(name='pds:/path/to/file.csv::/:0')  # First row
# @valid(name='pds:/path/to/file.csv::/"column0":0')  # First cell
# # Multiple columns
# @valid(name='pds:/path/to/file.csv::/"column0":;"column2:"')
# # Multiple columns with indexes
# @valid(name='pds:/path/to/file.csv::/0:;2:')
# # Multiple columns mixed notation
# @valid(name='pds:/path/to/file.csv::/"column0":;"column2"')
# # Cross section (top left cell|bottom right cell)
# @valid(name='pds:/path/to/file.csv::/"column0":3|"column2":7')
# # Multiple cross sections
# @valid(name='pds:/path/to/file.csv::'
#             '/"column0":3|"column2":7;column0":3|"column2":7')
# # First column from excel
# @valid(name='pds:/path/to/file.xls::/Worksheet/0:')  # First column with index
# First column without colon
# @invalid(name='pds:/path/to/file.csv::/"column0"')
# # Multiple columns with indexes without colons
# @invalid(name='pds:/path/to/file.csv::/0;2')
# # Multiple columns without colons
# @invalid(name='pds:/path/to/file.csv::/"column0";"column2"')
# # Has extra final ";"
# @invalid(name='pds:/path/to/file.csv::/"column0":;"')
# @invalid(name='pds:/path/to/file.csv::')  # Empty attribute
# @names(name='pds:/path/to/file.csv::/"column0":',
#        out=('pds:/path/to/file.csv::/"column0":',
#             '/path/to/file.csv::/"column0":', '/"column0:"'))
class PandasAttrValidatorTestCase(AbstractNameValidatorTestCase,
                                  unittest.TestCase):
    validator = PandasAttributeNameValidator

if __name__ == "__main__":
    unittest.main()
