#
# continuousEvent.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

class ContinuousEvent:
    """
    Used to contain the data of continuous events
    """
    def __init__(self, values, relative = False):

        self.relative = relative
        #handle multiple "values" types
        if isinstance(values, list) or isinstance(values, tuple):
            self.values = list(values)
        else:
            self.values = [values]

        self.normalized = not isinstance(self.values[0], int)
