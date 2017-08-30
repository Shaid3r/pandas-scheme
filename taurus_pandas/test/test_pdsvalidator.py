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
# CSV tests
@valid(name='pds-csv:/path/to/file::')  # Get all columns
@valid(name='pds-csv:/path/to/file::["column1"]')  # Get 1 column
# Get multiple columns
@valid(name='pds-csv:/path/to/file::["column1","column2"]')
@valid(name='pds-csv:/path/to/file::[],[0]')  # Get row 0, all columns
# Get 7 rows starting with 0, all columns
@valid(name='pds-csv:/path/to/file::[],[0,7]')
# =========================================================================
# XLS tests
@valid(name='pds-xls:/path/to/file::')  # Get all columns from 1-st sheet
@valid(name='pds-xls:/path/to/file::"Sheet"')  # Get all columns from "Sheet"
@valid(name='pds-xls:/path/to/file::"Sheet",["column1"]')  # Get 1 column
# Get multiple columns
@valid(name='pds-xls:/path/to/file::"Sheet",["column1","column2"]')
@valid(name='pds-xls:/path/to/file::"Sheet",[],[0]')  # Get row 0, all columns
# Get 7 rows starting with 0, all columns, 1-st sheet
@valid(name='pds-xls:/path/to/file::"",[],[0,7]')
@invalid(name='pds-xls:/path/to/file::",[],[0,7]')
class PandasAttrValidatorTestCase(AbstractNameValidatorTestCase,
                                  unittest.TestCase):
    validator = PandasAttributeNameValidator

if __name__ == "__main__":
    unittest.main()
