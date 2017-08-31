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
psdfactory.py:
"""

from taurus.core.taurusbasetypes import TaurusElementType
from taurus.core.taurusfactory import TaurusFactory
from taurus.core.util.log import Logger
from taurus.core.util.singleton import Singleton
from taurus_pandas.pdsattribute import PandasAttribute
from taurus_pandas.pdsauthority import PandasAuthority
from taurus_pandas.pdsdevice import PandasDevice
from taurus_pandas.pdshandlers import schemesMap

__all__ = ["PandasFactory"]

__docformat__ = "restructuredtext"


class PandasFactory(Singleton, TaurusFactory, Logger):
    schemes = schemesMap.keys()
    elementTypesMap = {TaurusElementType.Authority: PandasAuthority,
                       TaurusElementType.Device: PandasDevice,
                       TaurusElementType.Attribute: PandasAttribute
                       }

    DEFAULT_AUTHORITY = '//localhost'

    def init(self, *args, **kwargs):
        """Singleton instance initialization.
           **For internal usage only**"""
        name = self.__class__.__name__
        self.call__init__(Logger, name)
        self.call__init__(TaurusFactory)

    def getAuthorityNameValidator(self):
        import pdsvalidator
        return pdsvalidator.PandasAuthorityNameValidator()

    def getDeviceNameValidator(self):
        import pdsvalidator
        return pdsvalidator.PandasDeviceNameValidator()

    def getAttributeNameValidator(self):
        import pdsvalidator
        return pdsvalidator.PandasAttributeNameValidator()
