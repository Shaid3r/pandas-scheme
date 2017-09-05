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
This module contains all handlers that depending on the file extension
parses given attribute name and returns pandas.DataFrame.

It also defines `schemesMap` that every supported scheme assigns proper
handler.
"""

import ast
import pandas


class AbstractHandler(object):
    """
    Base class for every Handler.

    _exts: (list) list of the supported extensions
    _kwargs: (dict) dict of arguments that will be passed to pandas function
    _cols: (list) list of columns cut by parseAttrName
    _rows: (list) list of rows cut by parseAttrName

    Every new handler should provide:
    - _exts
    - read
    - _addArg

    Additionally handler should be assigned to scheme in `schemeMap`.
    """
    _exts = []

    def __init__(self):
        self._kwargs = {}
        self._cols = None
        self._rows = None

    def parseAttrName(self, attr_name):
        """
        Parses part of the URI after "::" using `ast.literal_eval` then
        opens given file using pandas functions, cut appropriate columns
        and rows and returns them.
        :param attr_name: (str) attribute name from the URI
        :return: (pandas.DataFrame)
        """
        if attr_name != '':
            args = ast.literal_eval(attr_name)

            if isinstance(args, dict):
                self._addKwargs(args)
            elif not isinstance(args, tuple):
                self._addArg(0, args)
            else:
                if isinstance(args[-1], dict):
                    self._addKwargs(args[-1])
                    self._addArgs(args[:-1])
                else:
                    self._addArgs(args)

        df = self.read()
        df = self.getColumns(df, self._cols)  # Cut columns
        df = self.getRows(df, self._rows)  # Cut rows

        return df

    @classmethod
    def canHandle(cls, ext):
        """
        Checks if given handler can handle file with this extension.
        :param ext: (str)
        :return: (bool)
        """
        return ext in cls._exts

    def read(self):
        """
        Opens given file using appropriate pandas function and
        returns it content.
        :return: (pandas.DataFrame)
        """
        raise NotImplementedError("read cannot be called"
                                  " for AbstractHandler")

    def _addArg(self, pos, arg):
        """
        Sets appropriate attributes for given argument.
        This method should be implemented in derived classes.
        :param pos: (int) position of the argument in attr_name
        :param arg: (undefined) argument
        """
        raise NotImplementedError("addArg cannot be called"
                                  " for AbstractHandler")

    def _addArgs(self, args):
        for pos, arg in enumerate(args):
            self._addArg(pos, arg)

    def _addKwargs(self, args):
        for arg in args:
            self._kwargs[arg] = args[arg]

    @staticmethod
    def getColumns(df, columns):
        if columns:
            return df[columns]
        return df

    @staticmethod
    def getRows(df, rows):
        if rows:
            if len(rows) == 2:
                return df[rows[0]:rows[1]]
            return df[rows[0]:rows[0] + 1]
        return df

    def setFilename(self, filename):
        self.filename = filename


class CSVHandler(AbstractHandler):
    _exts = ['.csv']

    def read(self):
        return pandas.read_csv(self.filename, **self._kwargs)

    def _addArg(self, pos, arg):
        if pos == 0:
            self._cols = arg
        else:
            self._rows = arg


class XLSHandler(AbstractHandler):
    _exts = ['.xls', '.xlsx']

    def read(self):
        return pandas.read_excel(self.filename, **self._kwargs)

    def _addArg(self, pos, arg):
        if pos == 0 and arg != '':
            self._kwargs['sheetname'] = arg
        elif pos == 1:
            self._cols = arg
        else:
            self._rows = arg


schemesMap = {'pds': AbstractHandler,
              'pds-csv': CSVHandler,
              'pds-xls': XLSHandler
              }
