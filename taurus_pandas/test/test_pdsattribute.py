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
import numpy
import taurus
from taurus.core import TaurusAttrValue
from taurus.external.pint import Quantity
from taurus.external import unittest
from taurus.test import insertTest
from taurus_pandas.pdsattribute import PandasAttribute


@insertTest(helper_name="read_attr",
            attr_fullname='pds:/./res/file.xls::',
            expected=dict(
                rvalue="sth"
            )
)
class PandasAttributeTestCase(unittest.TestCase):

    def read_attr(self, attr_fullname, expected={}):
        a = taurus.Attribute(attr_fullname)
        read_value = a.read()

        msg = ('read() for "{}" did not return an TaurusAttrValue ' +
               '(got a {})'.format(attr_fullname,
                                   read_value.__class__.name__))
        self.assertTrue(isinstance(read_value, TaurusAttrValue), msg)

        # Test attribute
        for k, exp in expected.iteritems():
            try:
                got = getattr(a, k)
            except AttributeError:
                msg = ('The attribute "{}" does not provide infor on {}'
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

