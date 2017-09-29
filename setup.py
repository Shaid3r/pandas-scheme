#!/usr/bin/env python

##############################################################################
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
##############################################################################

from setuptools import setup, find_packages

version = '0.1.0'
description = 'pandas Taurus scheme'
long_description = '''taurus-pandas-scheme is the Taurus scheme that provides
access to the contents of files as Taurus Attributes. It uses the pandas module.
'''
license = 'LGPL'
platforms = ['Linux', 'Windows']


authors = 'Shaid3r'
email = 'michal@szczepanczyk.com'
url = 'http://www.taurus-scada.org/en/stable/devel/core_tutorial.html'

install_requires = ['taurus>=4.0.1',
                    'pandas']

setup(name='taurus-pandas-scheme',
      version=version,
      description=description,
      long_description=long_description,
      author=authors,
      maintainer=authors,
      maintainer_email=email,
      url=url,
      platforms=platforms,
      license=license,
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      test_suite='pandas.test.testsuite.get_suite',
      )
