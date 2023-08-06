import smbus
from .leds import Leds
from .temperature_sensor import TemperatureSensor
from .touch_sensor import TouchSensor
from .accelerometer import Accelerometer
import threading
import time
from enum import Enum

class TouchKey(Enum):
    UP = 4
    DOWN = 8
    LEFT = 1
    RIGHT = 2
    A = 32
    B = 16
    X = 64

class KeyState(Enum):
    RELEASED = 0
    PRESSED = 1

class TouchberryPi(object):
    I2C_ADDRESS_ACCELEROMETER = 0x1C
    I2C_ADDRESS_TOUCH_SENSOR = 0x1B
    I2C_ADDRESS_TEMPERATURE_SENSOR = 0x48
    I2C_ADDRESS_LEDS = 0x60

    def __init__(self):
        self.i2c_bus = smbus.SMBus(1)

        self.key_down_callback = None
        self.key_up_callback = None
        self.key_change_callback = None

        self.touch = TouchSensor(self.i2c_bus, TouchberryPi.I2C_ADDRESS_TOUCH_SENSOR)
        self.temperature_sensor = TemperatureSensor(self.i2c_bus, TouchberryPi.I2C_ADDRESS_TEMPERATURE_SENSOR)
        self.leds = Leds(self.i2c_bus, TouchberryPi.I2C_ADDRESS_LEDS)
        self.accelerometer = Accelerometer(self.i2c_bus, TouchberryPi.I2C_ADDRESS_ACCELEROMETER)

    def temperature(self):
        return self.temperature_sensor.temperature()

    def set_all_leds(self, color):
        self.leds.set_all(color)

    def set_led(self, led, color):
        self.leds.set_led(led, color)

    # callback(TouchKey)
    def on_key_up(self, callback):
        self.key_up_callback = callback

    # callback(TouchKey)
    def on_key_down(self, callback):
        self.key_down_callback = callback

    # callback(TouchKey, KeyState)
    def on_key_change(self, callback):
        self.key_change_callback = callback

    def start_touch_listener(self, interval=0.5):
        self.interval = interval
        self.touchThread = threading.Thread(target=self.touch_run)
        self.touchThread.daemon = True        # Daemon threads are abruptly stopped at shutdown.
        self.touchThread.start()

    def touch_run(self):
        """ Method checks for touch changes """
        currentKeyState = 0
        previousKeyState = 0
        while True:
            currentKeyState = self.touch.key_state()
            if (currentKeyState != previousKeyState):
                stateInfo = self.determine_key_state_info(previousKeyState, currentKeyState)
                self.trigger_change_callbacks(stateInfo)

            previousKeyState = currentKeyState
            time.sleep(self.interval)

    def trigger_change_callbacks(self, keyStates):
        for state in keyStates:
            if state['changed']:
                if self.key_change_callback != None:
                    self.key_change_callback(state['key'], state['state'])
                if state['state'] == KeyState.PRESSED and self.key_down_callback != None:
                    self.key_down_callback(state['key'])
                elif state['state'] == KeyState.RELEASED and self.key_up_callback != None:
                    self.key_up_callback(state['key'])

    def determine_key_state_info(self, previousKeyState, currentKeyState):
        results = []
        changedKeys = previousKeyState ^ currentKeyState
        for i in range(0,TouchSensor.NUMBER_OF_KEYS):
            mask = 0x01 << i
            key = TouchKey(mask)
            changed = (changedKeys & mask) != 0
            state = KeyState((currentKeyState & mask) >> i)
            results.append({    \
                'key': key, \
                'changed': changed,  \
                'state': state  \
            })
        return results
