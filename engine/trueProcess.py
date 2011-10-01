#
# trueProcess.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

try:
    import multiprocessing
except:
    raise Exception("Unable to load multiprocessing Python module.")

class TrueProcess(multiprocessing.Process):
    """
    A wrapper for multiple processes based on Allen Downey's threading wrapper.
    """
    def __init__(self, target, *args):
        multiprocessing.Process.__init__(self, target=target, args=args)
        self.start()
