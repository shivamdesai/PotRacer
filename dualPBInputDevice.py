
#
# biofeedback.py
#
# Copyright (C)2011 Julian Ceipek and Patrick Varin
#
# Redistribution is permitted under the BSD license.  See LICENSE for details.
#

try:
    import multiprocessing
except:
    raise Exception("Unable to load multiprocessing Python module.")

try:
    import usb.core
    import usb.util
except Exception as e:
    print "Unable to load pyusb properly."
    raise e

import time

from engine.trueProcess import TrueProcess
from engine.altInput import AltInput

class Reader:

    READ_POT    = 0x01
    READ_BUTTON = 0x02
    SET_LED     = 0x03
    CLEAR_LED   = 0x04
    SET_CONFIG  = 0x09

    def __init__(self, vendorID, productID):
        self.active = multiprocessing.Value('i',1)
        self._dev = usb.core.find(idVendor=vendorID, idProduct=productID)
        self.proc = None
        
    def listen(self):
        self.eventQueue = multiprocessing.Queue(8)
        self.proc = TrueProcess(self.continuousReader)

    def continuousReader(self):
        self._pot0 = None
        self._pot1 = None
        self._button0 = None
        self._button1 = None
        while self.active.value == 1:
            try:
                newVal = self.readPotentiometer(0)
                if not newVal == self._pot0:
                    self._pot0 = newVal
                    self.putPICMessage(('PIC_Potentiometer0', self._pot0))
                    self.setLED(0)
                else:
                    self.clearLED(0)
                    
                newVal = self.readPotentiometer(1)
                if not newVal == self._pot1:
                    self._pot1 = newVal
                    self.putPICMessage(('PIC_Potentiometer1', self._pot1))
                    self.setLED(1)
                else:
                    self.clearLED(1)
                    
                newVal = self.readButton(0)
                if not newVal == self._button0:
                    self._button0 = newVal
                    self.putPICMessage(('PIC_Button0', self._button0))
                    self.setLED(0)
                else:
                    self.clearLED(0)
                
                newVal = self.readButton(1)
                if not newVal == self._button1:
                    self._button1 = newVal
                    self.putPICMessage(('PIC_Button1', self._button1))
                    self.setLED(1)
                else:
                    self.clearLED(1)
                    
            except Exception as e:
                print "Reading from PIC Failed: ",e

    def putPICMessage(self, message):
        while self.eventQueue.full():
            self.eventQueue.get()
        self.eventQueue.put(message)

    def readPotentiometer(self, player):
        """
        player = 0 or 1
        """
        return self._performCommand(self.READ_POT, parameter=player, io='r', requestType='vendor', recipient='device')

    def readButton(self, player):
        """
        player = 0 or 1
        """
        return self._performCommand(self.READ_BUTTON, parameter=player, io='r', requestType='vendor', recipient='device')

    def setLED(self, player):
        """
        player = 0 or 1
        """
        return self._performCommand(self.SET_LED, parameter=player, io='w', requestType='vendor', recipient='device')

    def clearLED(self, player):
        """
        player = 0 or 1
        """
        return self._performCommand(self.CLEAR_LED, parameter=player, io='w', requestType='vendor', recipient='device')

    def setConfig(self):
        return self._performCommand(self.SET_CONFIG, parameter=1, io='w', requestType='standard', recipient='device')

    def _performCommand(self, requestID, parameter=0, io='r', requestType='standard', recipient='device'):

        if requestType == 'standard':
            requestType = '00'
        elif requestType == 'class':
            requestType = '01'
        elif requestType == 'vendor':
            requestType = '10'
        else:
            raise ValueError, "Invalid requestType value specified. Can only be 'standard', 'class', or 'vendor'"

        if recipient=='device':
            recipient = '00000'
        elif recipient=='interface':
            recipient = '00001'
        elif recipient=='endpoint':
            recipient = '00010'
        elif recipient=='other':
            recipient = '00011'
        else:
            raise ValueError, "Invalid recipient value specified. Can only be 'device', 'interface', 'endpoint', or 'other'"

        #buffer = ctypes.c_buffer(1)

        #ret = self._usb.control_transfer(self._dev, int(transferDirection + requestType + recipient, 2), requestID, parameter, 0, wLength, buffer)
        
        try:
            if io == 'r':
                transferDirection = '1'
                ret = self._dev.ctrl_transfer(int(transferDirection + requestType + recipient, 2),
                                          requestID, parameter, 0, 1)
                return ret[0]
            elif io == 'w':
                transferDirection = '0'
                self._dev.ctrl_transfer(int(transferDirection + requestType + recipient, 2),
                                          requestID, parameter, 0, None)
            else:
                raise ValueError, "Invalid io value specified. Can only be 'r' or 'w'"
        except:
            raise IOError, "Unable to perform vendor request."

    def deactivate(self):
        self.active.value = 0
        print("Closed PIC Process")

class DualPBDevice(AltInput):
    def __init__(self, vendorID, productID):
        self.reader = Reader(vendorID, productID)
        self.reader.listen()

    def poll(self):
        return (not self.reader.eventQueue.empty())

    def getEvents(self):
        events = []

        if not self.reader.eventQueue.empty():
            reading = self.reader.eventQueue.get()
            identifier = reading[0]
            value = reading[1]
            discrete = ('PIC_Button' in identifier) #POT is continuous; Button is discrete
            PICReading = self.makeEvent(identifier, value, discrete)
            events.append(PICReading)

        return events

    def stop(self):
        self.reader.deactivate()
