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
from taurus import makeSchemeExplicit

__all__ = ["PandasAuthorityNameValidator", "PandasDeviceNameValidator",
           "PandasAttributeNameValidator"]

from os import path

from taurus.core.taurusvalidator import (TaurusAttributeNameValidator,
                                         TaurusDeviceNameValidator,
                                         TaurusAuthorityNameValidator)
from taurus_pandas.pdsfactory import PandasFactory
from taurus_pandas.pdshandlers import schemesMap


class PandasAuthorityNameValidator(TaurusAuthorityNameValidator):
    """A validator for Authority names in the pandas scheme.
        For now it is a dummy one, allowing only //localhost
        """
    scheme = "|".join(["(" + x + ")" for x in schemesMap.keys()])
    authority = '//localhost'
    path = '(?!)'
    query = '(?!)'
    fragment = '(?!)'

    def getUriGroups(self, name, strict=None):
        name = makeSchemeExplicit(name, default='pds')
        m = self.name_re.match(name)
        # if it is strictly valid, return the groups
        if m is not None:
            ret = m.groupdict()
            ret['__STRICT__'] = True
            return ret
        return None


class PandasDeviceNameValidator(TaurusDeviceNameValidator):
    """A validator for Device names in the pandas scheme."""
    scheme = PandasAuthorityNameValidator.scheme
    authority = PandasAuthorityNameValidator.authority
    # devname group is mandatory
    path = r'(?P<devname>(/(//+)?([A-Za-z]:/)?' \
           r'([\w.\-]+/)*[\w.\-]+))'
    query = '(?!)'
    fragment = '(?!)'

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

    def getUriGroups(self, name, strict=None):
        groups = TaurusDeviceNameValidator.getUriGroups(self, name, strict)

        try:
            scheme = groups.get('scheme')

            if scheme != 'pds':
                return groups
        except:
            return None

        import os
        _, ext = os.path.splitext(groups.get('devname'))

        for handler in schemesMap.keys():
            if schemesMap[handler].canHandle(ext):
                groups['scheme'] = handler
                return groups
        return None


class PandasAttributeNameValidator(TaurusAttributeNameValidator):
    """A validator for Attribute names in the pandas scheme."""
    scheme = PandasAuthorityNameValidator.scheme
    authority = PandasAuthorityNameValidator.authority
    path = r'%s::(?P<attrname>[\w.\-/\[\]"\',]*)' % PandasDeviceNameValidator.path
    query = '(?!)'
    fragment = '(?!)'

    def getNames(self, fullname, factory=None, fragment=False):
        """reimplemented from :class:`TaurusAttributeNameValidator`.
        """
        groups = self.getUriGroups(fullname)

        try:
            scheme = groups.get('scheme')

            if scheme == 'pds':
                import os
                _, ext = os.path.splitext(groups.get('devname'))

                for handler in schemesMap.keys():
                    if schemesMap[handler].canHandle(ext):
                        groups['scheme'] = handler
                        break
        except:
            return None

        authority = groups.get('authority')
        if authority is None:
            f_or_fklass = factory or PandasFactory
            groups['authority'] = f_or_fklass.DEFAULT_AUTHORITY

        complete = '%(scheme)s:%(authority)s%(devname)s::%(attrname)s' % groups
        normal = '%(devname)s::%(attrname)s' % groups
        short = '%(attrname)s' % groups

        return complete, normal, short

    def getUriGroups(self, name, strict=None):
        groups = TaurusAttributeNameValidator.getUriGroups(self, name, strict)

        if groups is None:
            return None

        attrname = groups.get('attrname')
        if attrname is None:
            return None

        if attrname != '':
            try:
                import ast
                ast.literal_eval(attrname)
            except:
                return None
        return groups
