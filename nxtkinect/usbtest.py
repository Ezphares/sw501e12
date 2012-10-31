'''
    usbtest.py
    A test program, to test usbcom class
    Usage:
    python usbtest.py
'''

from nxtkinect.usbcom import Usbcom

if __name__ == '__main__':
    usbcom = Usbcom()
    usbcom.send_data(-2046, 222, 333, 444, 555, 1000)
