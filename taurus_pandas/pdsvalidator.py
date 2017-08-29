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
from os import path

__all__ = ["PandasAuthorityNameValidator", "PandasDeviceNameValidator",
           "PandasAttributeNameValidator"]

from taurus.core.taurusvalidator import (TaurusAttributeNameValidator,
                                         TaurusDeviceNameValidator,
                                         TaurusAuthorityNameValidator)
from taurus_pandas.pdsfactory import PandasFactory


class PandasAuthorityNameValidator(TaurusAuthorityNameValidator):
    """A validator for Authority names in the pandas scheme.
        For now it is a dummy one, allowing only //localhost
        """
    scheme = '(pds)|(pds-csv)|(pds-xls)'
    authority = '//localhost'
    path = '(?!)'
    query = '(?!)'
    fragment = '(?!)'


class PandasDeviceNameValidator(TaurusDeviceNameValidator):
    """A validator for Device names in the pandas scheme."""
    scheme = PandasAuthorityNameValidator.scheme
    authority = PandasAuthorityNameValidator.authority
    # devname group is mandatory
    path = r'(?P<devname>(/(//+)?([A-Za-z]:/)?' \
           r'([\w.\-]+/)*[\w.\-]+))'
    query = '(?!)'
    fragment = '(?!)'

    def __init__(self):
        TaurusDeviceNameValidator.__init__(self)
        # print(self.namePattern)

    def getNames(self, fullname, factory=None):
        """reimplemented from :class:`TaurusDeviceNameValidator`."""
        groups = self.getUriGroups(fullname)
        if groups is None:
            return None

        authority = groups.get('authority')
        if authority is None:
            f_or_fklass = factory or PandasFactory
            groups['authority'] = f_or_fklass.DEFAULT_AUTHORITY

        filename = groups.get('devname').rsplit('/', 1)[1]
        groups['devname'] = path.realpath(groups.get('devname'))
        complete = '%(scheme)s:%(authority)s%(devname)s' % groups
        normal = '%(devname)s' % groups
        short = filename

        return complete, normal, short


class PandasAttributeNameValidator(TaurusAttributeNameValidator):
    pass

