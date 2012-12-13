""" Converts each of the position coordinates x, y and z as well as the speed vector x, y and z coordinates to an array of chars. """
def convert(self, number):
#If the number is negative, the sign bit will be set to 1, otherwise it will be set to 0.
    if number < 0:
        sign = 1
        number = -number
    else:
        sign = 0
#If the number is larger than an int, the data is not valid, and the array will be zeroed.
    if(number >= 65536):
        return [0, 0, 0]
#The int number is converted into an array of chars so that it can be sent over USB.
    else:
        return [sign, int(number / 256), int(number % 256)]
        

def send_data(self, pos_x, pos_y, pos_z, speed_x, speed_y, speed_z):
#Every input is an array converted from an int, they are all added to one array that can be sent over USB.
    data = []
    data.extend(self.convert(pos_x))
    data.extend(self.convert(pos_y))
    data.extend(self.convert(pos_z))
    data.extend(self.convert(speed_x))
    data.extend(self.convert(speed_y))
    data.extend(self.convert(speed_z))
    data = array.array('i', data)