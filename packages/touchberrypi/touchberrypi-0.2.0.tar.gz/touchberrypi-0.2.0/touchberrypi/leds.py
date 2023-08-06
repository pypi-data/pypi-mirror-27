from .color import Color
from time import sleep
from .i2c_peripheral import I2cPeripheral
from enum import Enum

class Led(Enum):
    LED1 = 0
    LED2 = 1
    LED3 = 2
    LED4 = 3
    LED5 = 4

class Leds(I2cPeripheral):
    DEF_ALL_CALL_ADDR = 0xD0

    REG_MODE_1 = 0x00
    REG_LED_0 = 0x02
    REG_LEDOUT0 = 0x14
    REG_ALLCALL = 0x1B

    NUMBER_OF_RGB_LEDS = 5

    def __init__(self, i2c_bus, slave_address):
        super().__init__(i2c_bus, slave_address)
        self.configure_for_pwn()
        self.enable()
        self.all_off()

    def all_off(self):
        self.set_all(Color(0, 0, 0))

    def set_all(self, color):
        register = Leds.REG_LED_0
        register = self.get_auto_increment_reg_address(register)
        values = color.values() * Leds.NUMBER_OF_RGB_LEDS
        self.write_block(register, values)

    def set_led(self, led, color):
        register = Leds.REG_LED_0 + (led.value * 3)
        register = self.get_auto_increment_reg_address(register)
        self.write_block(register, color.values())

    def configure_for_pwn(self):
        register = self.get_auto_increment_reg_address(Leds.REG_LEDOUT0)
        values = [0xAA] * 4
        self.write_block(register, values)

    def enable(self):
        mode = self.read_register(Leds.REG_MODE_1)
        mode &= (~0x01 << 4);
        self.write_register(Leds.REG_MODE_1, mode)

    def all_call_address(self):
        return self.read_register(Leds.REG_ALLCALL)

    def get_auto_increment_reg_address(self, register):
        return register | (0x01 << 7)

    def self_check(self):
        """Read value from peripheral register and checks against known value"""
        # I know not the best idea but i need a way to self check
        if self.all_call_address() != Leds.DEF_ALL_CALL_ADDR:
            print("Failed to talk to TLC59116 Led Driver")
        else:
            print("TLC59116 Led Driver online ...")
