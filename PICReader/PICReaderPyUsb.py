import usb.core
import usb.util

import time

class Reader:

    READ_POT    = 0x01
    READ_BUTTON = 0x02
    SET_LED     = 0x03
    CLEAR_LED   = 0x04
    SET_CONFIG  = 0x09

    def __init__(self):
        self._dev = usb.core.find(idVendor=0x6666, idProduct=0x0003)

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

    def close(self):
        usb.close_device(dev)

if __name__ == "__main__":
    reader = Reader()
    while True:
        print "POT0: ", reader.readPotentiometer(0)
        print "POT1: ", reader.readPotentiometer(1)
        print "BTTN0: ", reader.readButton(0)
        print "BTTN1: ", reader.readButton(1)
        reader.setLED(1)
        reader.clearLED(0)
        time.sleep(0.1)
        reader.clearLED(1)
        reader.setLED(0)
