from .i2c_peripheral import I2cPeripheral

class TouchSensor(I2cPeripheral):
    CHIP_ID_CHECK = 0x2E
    REG_CHIP_ID = 0
    REG_KEY_STATE = 3
    REG_CALIBRATE = 56
    REG_RESET = 57
    NUMBER_OF_KEYS = 7

    def __init__(self, i2c_bus, slave_address):
        super().__init__(i2c_bus, slave_address)

    def chip_id(self):
        return self.read_register(TouchSensor.REG_CHIP_ID)

    def key_state(self):
        return self.read_register(TouchSensor.REG_KEY_STATE)

    def calibrate(self):
        self.write_register(TouchSensor.REG_CALIBRATE, 0xFF)

    def reset(self):
        self.write_register(TouchSensor.REG_RESET, 0xFF)

    def self_check(self):
        """Read value from peripheral register and checks against known value"""
        if self.chip_id() != TouchSensor.CHIP_ID_CHECK:
            print("Failed to talk to QT1070 Touch Sensor")
        else:
            print("QT1070 Touch Sensor online ...")
