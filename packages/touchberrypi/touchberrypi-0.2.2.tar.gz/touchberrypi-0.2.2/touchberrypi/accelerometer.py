from .i2c_peripheral import I2cPeripheral

class Accelerometer(I2cPeripheral):
    WHO_AM_I = 0x1A
    REG_WHO_AM_I = 0x0D

    def __init__(self, i2c_bus, slave_address):
        super().__init__(i2c_bus, slave_address)

    def who_am_i(self):
        return self.read_register(Accelerometer.REG_WHO_AM_I)

    def self_check(self):
        """Read value from peripheral register and checks against known value"""
        if self.who_am_i() != Accelerometer.WHO_AM_I:
            print("Failed to talk to MMA8451Q Accelerometer")
        else:
            print("MMA8451Q Accelerometer online ...")
