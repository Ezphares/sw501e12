'''
    usbcom.py
    This file contains the usb communication class used to communicate with the NXT over usb.
'''

import usb.core
import usb.util
import array
import sys
import os

class Usbcom:
    ID_VENDOR_LEGO = 0x0694
    ID_PRODUCT_NXT = 0x0002
    SYSTEM_COMMAND_REPLY = 0x01
    REPLY_COMMAND = 0x02
    USB_ECROBOT_MODE = 0xFF
    USB_ECROBOT_SIGNATURE = 'ECROBOT'
    DISCONNECT_REQ = 0xFF
    ACK_STRING = 0x02
    NXTdevice = None
    handle = None
    NXTout = None
    NXTin = None

    def convert(self, number):
        if number < 0:
            sign = 1
            number = -number
        else:
            sign = 0
        if(number >= 65536):
            return [0, 0, 0]
        else:
            return [sign, int(number / 256), int(number % 256)]
            

    def send_data(self, pos_x, pos_y, pos_z, speed_x, speed_y, speed_z):
        data = []
        data.extend(self.convert(pos_x))
        data.extend(self.convert(pos_y))
        data.extend(self.convert(pos_z))
        data.extend(self.convert(speed_x))
        data.extend(self.convert(speed_y))
        data.extend(self.convert(speed_z))
        data = array.array('i', data)
        print data

        self.handle.bulkWrite(self.NXTout.address, data)

        data = self.handle.bulkRead(self.NXTin.address, 4)

        if data[0] == self.ACK_STRING and data[1:3].tostring() == "ok":
            data = array.array('c', list(chr(self.DISCONNECT_REQ)))
            self.handle.bulkWrite(self.NXTout.address, data)
        else:
            print 'Error: could not send data'
        
        

    def __init__(self):

        for bus in usb.busses():

           for device in bus.devices:
               if device.idVendor == self.ID_VENDOR_LEGO and device.idProduct == self.ID_PRODUCT_NXT:
                   self.NXTdevice = device
                   break

           if self.NXTdevice is None:
               print 'Error: No NXT device found.'
               sys.exit( -1 )

           config = self.NXTdevice.configurations[0]

           iface = config.interfaces[0][0]

           self.NXTout, self.NXTin = iface.endpoints

           self.handle = self.NXTdevice.open();
           self.handle.claimInterface(0)

           if os.name != 'nt':
               self.handle.reset()

           data = array.array('B', [self.SYSTEM_COMMAND_REPLY, self.USB_ECROBOT_MODE])

           self.handle.bulkWrite(self.NXTout.address, data)

           data = self.handle.bulkRead(self.NXTin.address, len(self.USB_ECROBOT_SIGNATURE) + 1)

           if data[0] != self.REPLY_COMMAND or data[1:].tostring() != self.USB_ECROBOT_SIGNATURE:
               print 'Error: Invalid NXT signature.'
               sys.exit(-1)   
