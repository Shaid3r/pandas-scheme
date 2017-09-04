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
    _fmts = []

    def __init__(self):
        self._kwargs = {}
        self._cols = None
        self._rows = None

    def parseAttrName(self, attr_name):
        """:return (DataFrame)"""
        if attr_name != '':
            import ast
            print("attr: " + attr_name)
            args = ast.literal_eval(attr_name)

            if isinstance(args[-1], dict):
                print "Dict: ", args[-1]
                self.addKwargs(args[-1])
                self.addArgs(args[:-1])
            else:
                print "No dict", args
                self.addArgs(args)

        df = self.read()
        df = self.getColumns(df, self._cols)  # Cut columns
        df = self.getRows(df, self._rows)  # Cut rows

        return df

    @classmethod
    def canHandle(cls, ext):
        return ext in cls._fmts

    def setFilename(self, filename):
        self.filename = filename

    def read(self):
        raise NotImplementedError("read cannot be called"
                                  " for AbstractHandler")

    def addArgs(self, args):
        raise NotImplementedError("addArgs cannot be called"
                                  " for AbstractHandler")

    def addKwargs(self, args):
        for arg in args:
            self._kwargs[arg] = args[arg]

    @staticmethod
    def getColumns(df, columns):
        if columns:
            return df[columns]
        return df

    @staticmethod
    def getRows(df, rows):
        # print "ROWS", rows
        # print df[rows]
        return df


class CSVHandler(AbstractHandler):
    _fmts = ['.csv']

    def read(self):
        return pandas.read_csv(self.filename, **self._kwargs)

    def addArgs(self, args):
        if isinstance(args, list):
            self._cols = args
        elif isinstance(args, tuple):
            self._cols = args[0]
            self._rows = args[1]


class XLSHandler(AbstractHandler):
    _fmts = ['.xls', '.xlsx']

    def read(self):
        return pandas.read_excel(self.filename, **self._kwargs)

    def addArgs(self, args):
        if isinstance(args, basestring):
            self._kwargs['sheetname'] = args
        elif isinstance(args, tuple):
            if args[0] != '':
                self._kwargs['sheetname'] = args[0]
            try:
                self._cols = args[1]
                self._rows = args[2]
            except:
                pass


schemesMap = {'pds': AbstractHandler,
              'pds-csv': CSVHandler,
              'pds-xls': XLSHandler
              }

if __name__ == "__main__":
    c = CSVHandler()
    print c.canHandle('csv')
