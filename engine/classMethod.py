#
# classMethod.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class ClassMethod:
    def __init__(self, method):
        self.__call__ = method
