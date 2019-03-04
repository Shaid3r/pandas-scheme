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

__all__ = ["PandasAttribute"]

from taurus.core import TaurusException
from taurus.core.taurusattribute import TaurusAttribute
from taurus.core.taurusbasetypes import (DataType,
                                         DataFormat,
                                         TaurusAttrValue,
                                         TaurusTimeVal, TaurusEventType)
from taurus.external.pint import Quantity
from taurus_pandas.pdshandlers import schemesMap


class PandasAttribute(TaurusAttribute):
    """A :class:`TaurusAttribute` that gives access to selected columns and
     rows converting them to `TaurusAttrValue`.

    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the
                 :meth:`PandasFactory.getAttribute`
    """
    _scheme = 'pds'
    handler = None

    npdtype2taurusdtype = {'b': DataType.Boolean,
                           'i': DataType.Integer,
                           'f': DataType.Float,
                           'O': DataType.String,
                           'S': DataType.String
                           }

    def __init__(self, name, parent, **kwargs):
        TaurusAttribute.__init__(self, name, parent, **kwargs)

        v = self.getNameValidator()
        v.getUriGroups(name)
        groups = v.getUriGroups(name)

        self.handler = schemesMap[groups['scheme']]()
        self._attr_name = groups.get("attrname")
        self._last_value = None

        wantpolling = not self.isUsingEvents()
        haspolling = self.isPollingEnabled()
        if wantpolling:
            self._activatePolling()
        elif haspolling and not wantpolling:
            self.disablePolling()

    def read(self, cache=True):
        """Returns the value of the attribute.

        :param cache: (bool) If True (default), the last calculated value will
                      be returned. If False, the referenced values will be re-
                      read.
        :return: TaurusAttrValue
        """
        if cache and self._last_value is not None:
            return self._last_value

        dev = self.getParentObj()
        self.handler.setFilename(dev.filename)

        data_frame = self.handler.parseAttrName(self._attr_name)

        value = TaurusAttrValue()
        value.rvalue = self.decode(data_frame)
        value.time = TaurusTimeVal.now()
        self._last_value = value

        return value

    def decode(self, data_frame):
        """
        Decode the DataFrame to the corresponding python attribute
        :param data_frame: (pandas.DataFrame)
        :return: taurus valid type
        """
        columns_count = len(data_frame.columns)
        attr_value_np = data_frame.as_matrix()

        if columns_count < 2:
            attr_value_np = attr_value_np.reshape(-1)

            if len(attr_value_np) == 1:
                self.data_format = DataFormat._0D
                attr_value_np = attr_value_np[0]
            else:
                self.data_format = DataFormat._1D
        else:
            if len(attr_value_np) == 1:
                self.data_format = DataFormat._1D
                attr_value_np = attr_value_np[0]
            else:
                self.data_format = DataFormat._2D

        try:
            npdtype = attr_value_np.dtype.kind
            self.type = self.npdtype2taurusdtype.get(npdtype)
        except AttributeError:
            self.type = self.npdtype2taurusdtype.get("O")

        if self.isNumeric():
            value = Quantity(attr_value_np, units="dimensionless")
        elif self.data_format == DataFormat._0D:
            value = attr_value_np
        elif self.type is DataType.String or self.type is DataType.Boolean:
            value = attr_value_np.tolist()

        if self.type == self.npdtype2taurusdtype["O"] and columns_count >= 2:
            for row_idx in range(len(value)):
                for item_idx in range(len(value[row_idx])):
                    value[row_idx][item_idx] = str(value[row_idx][item_idx])

        return value

    def poll(self):
        v = self.read(cache=False)
        self.fireEvent(TaurusEventType.Periodic, v)

    def isUsingEvents(self):
        return False

# -----------------------------------------------------------------------------
    def encode(self, value):
        # TODO: implement it if you want to support writable attributes
        return value

    def isWritable(self, cache=True):
        # TODO: implement it if you want to support writable attributes
        return False

    def write(self, value, with_read=True):
        # TODO: implement it if you want to support writable attributes
        raise TaurusException('Attributes are read-only')


if __name__ == "__main__":
    import os
    from taurus_pandas.pdsfactory import PandasFactory

    path2file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'test/res/file.xls')
    attrname = ''
    # attrname = '["int1"]'
    # attrname = '["int1","int2"]'
    # attrname = '"Sheet1"'
    # attrname = '"Sheet1",["column"]'
    a = PandasFactory().getAttribute("pds:{}::{}".format(path2file, attrname))
    print a.read()
