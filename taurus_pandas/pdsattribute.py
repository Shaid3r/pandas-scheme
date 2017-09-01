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

__all__ = ["PandasAttribute"]

import pandas

from taurus.core import TaurusException, TaurusAttrValue, TaurusTimeVal
from taurus.core.taurusattribute import TaurusAttribute
from taurus.external.pint import Quantity
from taurus_pandas.pdshandlers import schemesMap


class PandasAttribute(TaurusAttribute):
    """Store DataFrame object"""
    _scheme = 'pds'
    handler = None

    def __init__(self, name, parent, **kwargs):
        TaurusAttribute.__init__(self, name, parent, **kwargs)

        v = self.getNameValidator()
        v.getUriGroups(name)
        groups = v.getUriGroups(name)

        self.handler = schemesMap[groups['scheme']]()
        self._attr_name = groups.get("attrname")
        self._last_value = None

    def read(self, cache=True):
        """Read file, gets df, set rvalue"""
        if cache and self._last_value is not None:
            return self._last_value

        dev = self.getParentObj()
        self.handler.setFilename(dev.filename)

        if self._attr_name != '':
            import ast
            print("attr: " + self._attr_name)
            args = ast.literal_eval(self._attr_name)
            if isinstance(args, basestring):
                args = (args,)

            if args[-1] is dict:
                print "Dict: ", args[-1]
                # self.handler.addKwargs()
                # self.handler.addArgs(args[:-1])
            else:
                print "No dict", tuple(args)
                self.handler.addArgs(args)

        data_frame = self.handler.read()

        print data_frame
        # if data_frame is None:
        #     msg = ""

        value = TaurusAttrValue()
        value.rvalue = self.decode(data_frame)
        value.time = TaurusTimeVal.now()
        self._last_value = value
        return value

    # def nextChunk(self):
    #     pass
    #
    # def setChunkSize(self, size):
    #     handler.setChunkSize(size)

    def decode(self, data_frame):

        value = 0

        # value = Quantity(attr_value_np, units=units)
        return value

    def encode(self, value):
        # TODO: implement it if you want to support writable attributes
        return value

    def poll(self):
        # v = self.read(cache=False)
        # self.fireEvent(TaurusEventType.Periodic, v)
        pass

    def isWritable(self, cache=True):
        # TODO: implement it if you want to support writable attributes
        return False

    def write(self, value, with_read=True):
        # TODO: implement it if you want to support writable attributes
        raise TaurusException('Attributes are read-only')

    def isUsingEvents(self):
        # TODO: implement it if you want to support writable attributes
        return False

    def _subscribeEvents(self):
        # TODO: implement it if you want to support writable attributes
        pass

    def _unsubscribeEvents(self):
        # TODO: implement it if you want to support writable attributes
        pass


if __name__ == "__main__":
    import os
    from taurus_pandas.pdsfactory import PandasFactory

    path2file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'test/res/file.xls')
    attrname = '"Sheet1"'
    # attrname = '"Sheet1",["column"]'
    a = PandasFactory().getAttribute("pds:{}::{}".format(path2file, attrname))
    print a.read()
