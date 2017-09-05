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

"""
Pandas scheme for taurus core model.

This is a Taurus scheme that that gives access to selected columns and
rows converting them to `TaurusAttrValue`. It uses :mod: `pandas`.

For example, to get column "column1" from the file
/path/to/myfile.csv, you should do something like::

    >>> import taurus
    >>> myattr = taurus.Attribute('pds:/path/to/myfile.csv::["column1"]')

Pandas attributes (should) work just as other Taurus attributes and can be
referred by their model name wherever a Taurus Attribute model is expected. For
example, you can launch a `TaurusForm` with a pandas attribute::
    $> taurusform 'pds:/path/to/myfile.csv::["column1","column2"]'


Pandas model consists from the following parts:

`<scheme>:[//<authority>]/<path>::[<attrname>]`

Where:

    - <scheme> decides about used handler. Use `pds` to recognize
    file from extension, or for example `pds-csv` to force using
    CSVHandler.

    - <authority> is optional, for now only //localhost is supported

    - <path> is path to file.

    - <attrname> is optional, if not given, it means to get every column
    and every row. <attrname> should consists from valid python types
    separated by colon, because they will be passed to `ast.literal_eval`
    Usually it contains list of columns and rows, but it can be specific for
    the given format (eg. excel format has also "sheet"). <attrname> can
    contain also dict of parameters, that will be sent to pandas function.
    It must be at the end.


Some examples of valid pandas models are:

    - Recognize file extension and get all columns from 1-st sheet
        `pds:/path/to/file.xls::`

    - Force xls handler and get all columns from "Sheet"
        `pds-xls:/path/to/file::"Sheet"`

    - Get 1 column ("column1" must be in brackets)
        `pds-xls:/path/to/file::"Sheet",["column1"]`

    - Get multiple columns
        `pds-xls:/path/to/file::"Sheet",["column1","column2"]`

    - Get row 0, all columns
        `pds-xls:/path/to/file::"Sheet",[],[0]`

    - Get all rows from 0 to 7 (excluding 7), all columns, 1-st sheet
        `pds-xls:/path/to/file::"",[],[0,7]`

    - Pass parameters to pandas function
        `pds-xls:/path/to/file::{"parse_cols":"A:B"}`

"""

from pdsfactory import PandasFactory
from pdsattribute import PandasAttribute
from pdsdevice import PandasDevice
from pdsauthority import PandasAuthority
from pdsvalidator import *
