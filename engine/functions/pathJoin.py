#
# pathJoin.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

from os.path import join

def pathJoin(pathStrings):
    return join(*pathStrings)
