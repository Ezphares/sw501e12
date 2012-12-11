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