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

"""Tests for taurus.core.taurus_pandas.test.test_pdsattribute..."""

import os

import numpy
import taurus
from taurus.core import TaurusAttrValue, DataType
from taurus.external import unittest
from taurus.external.pint import Quantity
from taurus.test import insertTest

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# =========================================================================
# Tests of return types
# =========================================================================
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["int1"]'.format(BASE_DIR),
            expected=dict(
                rvalue=Quantity([1, 2, 3], 'dimensionless'),
                type=DataType.Integer
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["int1","int2"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=Quantity([[1, 4], [2, 5], [3, 6]], 'dimensionless'),
                type=DataType.Integer
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["float1"]'.format(BASE_DIR),
            expected=dict(
                rvalue=Quantity([1.2, 3.4, 5.6], 'dimensionless'),
                type=DataType.Float
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["float1","float2"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=Quantity([[1.2, 1.2], [3.4, 2.3], [5.6, 3.4]],
                                'dimensionless'),
                type=DataType.Float
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["string1"]'.format(BASE_DIR),
            expected=dict(
                rvalue=['a', 'b', 'c'],
                type=DataType.String
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["string1","string2"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=[['a', 'd'], ['b', 'e'], ['c', 'f']],
                type=DataType.String
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["bool1"]'.format(BASE_DIR),
            expected=dict(
                rvalue=[True, True, False],
                type=DataType.Boolean
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["bool1","bool2"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=[[True, False], [True, False], [False, True]],
                type=DataType.Boolean
            ))
# Mixed types
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["int1","float1"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=Quantity([[1., 1.2], [2., 3.4], [3., 5.6]],
                                'dimensionless'),
                type=DataType.Float
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::["int1","string1"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=[['1', 'a'], ['2', 'b'], ['3', 'c']],
                type=DataType.String
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.csv::'.format(
                BASE_DIR),
            expected=dict(
                rvalue=[['1', '4', '1.2', '1.2', 'a', 'd', 'True', 'False'],
                        ['2', '5', '3.4', '2.3', 'b', 'e', 'True', 'False'],
                        ['3', '6', '5.6', '3.4', 'c', 'f', 'False', 'True']],
                type=DataType.String
            ))
# =========================================================================
# Tests of XMLHandler
# =========================================================================
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.xls::"Sheet2"'.format(BASE_DIR),
            expected=dict(
                rvalue=Quantity([1, 2, 3], 'dimensionless'),
                type=DataType.Integer
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.xls::"Sheet",["int1"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=Quantity([1, 2, 3], 'dimensionless'),
                type=DataType.Integer
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.xls::"",["int1"]'.format(
                BASE_DIR),
            expected=dict(
                rvalue=Quantity([1, 2, 3], 'dimensionless'),
                type=DataType.Integer
            ))
@insertTest(helper_name="read_attr",
            attr_fullname='pds:{}/res/file.xls::'
                          '"Sheet",["int1","int2"]'.format(BASE_DIR),
            expected=dict(
                rvalue=Quantity([[1, 4], [2, 5], [3, 6]], 'dimensionless'),
                type=DataType.Integer
            ))
class PandasAttributeTestCase(unittest.TestCase):
    def read_attr(self, attr_fullname, expected={}):
        a = taurus.Attribute(attr_fullname)
        read_value = a.read()

        msg = ('read() for "{}" did not return an TaurusAttrValue ' +
               '(got a {})'.format(attr_fullname,
                                   read_value.__class__.__name__))
        self.assertTrue(isinstance(read_value, TaurusAttrValue), msg)

        # Test attribute
        for k, exp in expected.iteritems():
            try:
                got = getattr(a, k)
            except AttributeError:
                msg = ('The attribute "{}" does not provide info on {}'
                       .format(attr_fullname, k))
                self.fail(msg)
            msg = ('{} for "{}" should be {} (got {})'.format(
                attr_fullname, k, exp, got))

            self.__assertValidValue(exp, got, msg)

    def __assertValidValue(self, exp, got, msg):
        # if we are dealing with quantities, use the magnitude for comparing
        if isinstance(got, Quantity):
            got = got.to(Quantity(exp).units).magnitude
        if isinstance(exp, Quantity):
            exp = exp.magnitude
        try:
            # for those values that can be handled by numpy.allclose()
            chk = numpy.allclose(got, exp)
        except:
            # for the rest
            if isinstance(got, numpy.ndarray):
                got = got.tolist()
            chk = bool(got == exp)

        self.assertTrue(chk, msg)
