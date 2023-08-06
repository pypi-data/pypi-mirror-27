from .i2c_peripheral import I2cPeripheral

class TemperatureSensor(I2cPeripheral):
    DEF_HYSTERESIS = 75

    REG_TEMPERATURE = 0
    REG_CONFIG = 1
    REG_HYSTERESIS = 2
    REG_LIMIT = 3

    def __init__(self, i2c_bus, slave_address):
        super().__init__(i2c_bus, slave_address)

    def temperature(self):
        values = self.read_block(TemperatureSensor.REG_TEMPERATURE, 2)
        return self.convert_to_temperature(values)

    def hysteresis(self):
        values = self.read_block(TemperatureSensor.REG_HYSTERESIS, 2)
        return self.convert_to_temperature(values)

    def convert_to_temperature(self, byte_values):
        return (byte_values[0]*1.0) + byte_values[1]/256.0

    def self_check(self):
        """Read value from peripheral register and checks against known value"""
        # I know not the best idea but i need a way to self check
        if int(self.hysteresis()) != TemperatureSensor.DEF_HYSTERESIS:
            print("Failed to talk to MCP9800 Temperature Sensor")
        else:
            print("MCP9800 Temperature Sensor online ...")
