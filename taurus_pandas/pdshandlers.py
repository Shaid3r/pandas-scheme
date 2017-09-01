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
psdhandlers.py:
"""

import pandas

class AbstractHandler(object):
    fmts = []
    kwargs = {}

    @classmethod
    def canHandle(cls, ext):
        return ext in cls.fmts

    def setFilename(self, filename):
        self.filename = filename

    def read(self):
        raise NotImplementedError("read cannot be called"
                                  " for AbstractHandler")

    def addArgs(self, args):
        raise NotImplementedError("addArgs cannot be called"
                                  " for AbstractHandler")


class CSVHandler(AbstractHandler):
    fmts = ['.csv']

    def read(self):
        print "kwargs: ", self.kwargs
        return pandas.read_csv(self.filename, **self.kwargs)

    def addArgs(self, args):
        try:
            self.kwargs['usecols'] = args[0]
            # self.kwargs['rows'] = args[1]
        except:
            pass


class XLSHandler(AbstractHandler):
    fmts = ['.xls', '.xlsx']

    def read(self):
        print "kwargs: ", self.kwargs
        return pandas.read_excel(self.filename, **self.kwargs)

    def addArgs(self, args):
        print args
        try:
            self.kwargs['sheetname'] = args[0]
            self.kwargs['parse_cols'] = args[1]
            # self.kwargs['rows'] = args[2]
        except:
            pass


schemesMap = {'pds': AbstractHandler,
              'pds-csv': CSVHandler,
              'pds-xls': XLSHandler
              }


if __name__ == "__main__":
    c = CSVHandler()
    print c.canHandle('csv')
