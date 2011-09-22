import ctypes
import time

class PICReader:
    def __init__(self):
        self.__usb__ = ctypes.cdll.LoadLibrary('usb.dll')
        self.__usb__.initialize()
        self.__dev__ = self.__usb__.open_device(0x6666, 0x0003, 0)

    def setRA0(self, param):
        SET_DUTY = 0x04
        return self.__performCommand__(GET_RA0, parameter=param, io='w', requestType='vendor', recipient='device')

    def readRA2(self, param=0):
        GET_RA2 = 0x03
        return self.__performCommand__(GET_RA2, parameter=param, io='r', requestType='vendor', recipient='device')

    def readRA3(self, param=0):
        GET_RA3 = 0x05
        return self.__performCommand__(GET_RA3, parameter=param, io='r', requestType='vendor', recipient='device')

    def setRA1on(self):
        SET_RA1 = 0x01
        return self.__performCommand__(SET_RA1, parameter=0, io='w', requestType='vendor', recipient='device')

    def setRA1off(self):
        CLR_RA1 = 0x02
        return self.__performCommand__(CLR_RA1, parameter=0, io='w', requestType='vendor', recipient='device')

    def setConfig(self):
        SET_CONFIG = 0x09
        return self.__performCommand__(SET_CONFIG, parameter=1, io='w', requestType='standard', recipient='device')

    def __performCommand__(self, requestID, parameter=0, io='r', requestType='standard', recipient='device'):

        if io == 'r':
            transferDirection = '1'
            wLength = 1
        elif io == 'w':
            transferDirection = '0'
            wLength = 0
        else:
            raise ValueError, "Invalid io value specified. Can only be 'r' or 'w'"

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

        buffer = ctypes.c_buffer(8)

        ret = self.__usb__.control_transfer(self.__dev__, int(transferDirection + requestType + recipient, 2), requestID, parameter, 0, wLength, buffer)
        
        if ret < 0:
            raise IOError, "Unable to perform vendor request."
        else:
            return buffer.raw

    def close(self):
        usb.close_device(dev)



if __name__ == "__main__":
    reader = PICReader()
    while True:
        print repr(reader.readRA3())
        time.sleep(0.1)