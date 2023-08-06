class I2cPeripheral(object):
    MAX_SMB_BLOCK_SIZE = 32

    def __init__(self, i2c_bus, slave_address):
        self.i2c_bus = i2c_bus
        self.slave_address = slave_address
        self.self_check()

    def i2c_bus(self):
        return i2c_bus

    def slave_address(self):
        return slave_address

    def read_register(self, register):
        return self.i2c_bus.read_byte_data(self.slave_address, register)

    def write_register(self, register, value):
        self.i2c_bus.write_byte_data(self.slave_address, register, value)

    def read_block(self, start_register, length):
        if length > I2cPeripheral.MAX_SMB_BLOCK_SIZE:
            raise AttributeError("Length is too large, max " + I2cPeripheral.MAX_SMB_BLOCK_SIZE)

        # This just reads 32 bytes - go figure
        values = self.i2c_bus.read_i2c_block_data(self.slave_address, start_register)
        return values[0:length]

    def write_block(self, start_register, values):
        if len(values) > I2cPeripheral.MAX_SMB_BLOCK_SIZE:
            raise AttributeError("Length is too large, max " + I2cPeripheral.MAX_SMB_BLOCK_SIZE)

        self.i2c_bus.write_i2c_block_data(self.slave_address, start_register, values)

    def self_check(self):
        """Read value from peripheral register and checks against known value"""
        raise NotImplementedError("Please Implement this method")
