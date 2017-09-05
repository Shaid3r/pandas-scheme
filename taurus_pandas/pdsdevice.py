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
taurus_pandas module. See __init__.py for more detailed documentation
"""

__all__ = ["PandasDevice"]

from taurus.core.taurusdevice import TaurusDevice


class PandasDevice(TaurusDevice):
    """PandasDevice object. It is a :class:`TaurusDevice` and is used as the
    parent of :class:`PandasAttribute` objects.

    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the
                 :meth:`PandasFactory.getDevice`
    """
    _scheme = 'pds'

    def __init__(self, name, **kwargs):
        self.call__init__(TaurusDevice, name, **kwargs)
        v = self.getNameValidator()
        urigroups = v.getUriGroups(name)
        self.filename = urigroups.get("devname")
