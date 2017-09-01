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

__all__ = ["PandasFactory"]
__docformat__ = "restructuredtext"

from taurus.core.taurusbasetypes import TaurusElementType
from taurus.core.taurusfactory import TaurusFactory
from taurus.core.util.log import Logger
from taurus.core.util.singleton import Singleton
from taurus.core import TaurusException

from taurus_pandas.pdsattribute import PandasAttribute
from taurus_pandas.pdsauthority import PandasAuthority
from taurus_pandas.pdsdevice import PandasDevice
from taurus_pandas.pdshandlers import schemesMap


class PandasFactory(Singleton, TaurusFactory, Logger):
    """
        A Singleton class that provides Pandas related objects.
    """
    schemes = schemesMap.keys()
    elementTypesMap = {TaurusElementType.Authority: PandasAuthority,
                       TaurusElementType.Device: PandasDevice,
                       TaurusElementType.Attribute: PandasAttribute
                       }

    DEFAULT_AUTHORITY = '//localhost'

    def __init__(self):
        """ Initialization. Nothing to be done here for now."""
        pass

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

    def getAuthority(self, name=None):
        if name is None:
            name = 'pds://localhost'

        v = self.getAuthorityNameValidator()
        if not v.isValid(name):
            raise TaurusException(
                "Invalid Pandas authority name %s" % name)

        if not hasattr(self, "_auth"):
            self._auth = PandasAuthority(name)
        return self._auth

    def getAttribute(self, name):
        v = self.getAttributeNameValidator()
        if not v.isValid(name):
            msg = "Invalid attribute name '{name}'".format(name=name)
            raise TaurusException(msg)

        fullname, _, _ = v.getNames(name)
        attr = self._attrs.get(fullname)
        if attr is not None:
            return attr
        try:
            # this works only if the devname is present in the attr full name
            # (not all schemes are constructed in this way)
            groups = v.getUriGroups(fullname)
            scheme = groups['scheme']
            devname = groups['devname']
            dev = self.getDevice(scheme + ":" + devname)
        except:
            self.debug('Cannot get attribute parent from name "%s"', fullname)
            dev = None

        cls = self.elementTypesMap[TaurusElementType.Attribute]
        attr = cls(name=fullname, parent=dev)
        self._attrs[fullname] = attr
        return attr
