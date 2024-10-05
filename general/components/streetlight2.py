from gpiozero import LED, MotionSensor, PWMLED
import time
from ADCDevice import *

# Clase para el sensor PIR
class PirSensor:
    def __init__(self, led_pin, sensor_pin):
        self.led = LED(led_pin)
        self.sensor = MotionSensor(sensor_pin)
        self.previous_state = False

    def detect_motion(self):
        current_state = self.sensor.motion_detected
        if current_state and not self.previous_state:
            self.led.on()
            print("Motion detected! LED turned on >>>")
            self.previous_state = True
        elif not current_state and self.previous_state:
            self.led.off()
            print("No Motion! LED turned off <<")
            self.previous_state = False

    def destroy(self):
        self.led.close()
        self.sensor.close()

# Clase para el fotorresistor
class PhotoResistor:
    def __init__(self, led_pin, threshold=128):
        self.led = PWMLED(led_pin)
        self.adc = ADCDevice()
        self.threshold = threshold
        self.setup()

    def setup(self):
        if self.adc.detectI2C(0x48): # Detect the pcf8591.
            self.adc = PCF8591()
        elif self.adc.detectI2C(0x4b): # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found. Program Exit.")
            exit(-1)

    def adjust_led_brightness(self):
        value = self.adc.analogRead(0)  # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3
        print(f'ADC Value: {value}, Voltage: {voltage:.2f}V')

        if value > self.threshold:
            self.led.value = 1.0  # Turn on LED to maximum brightness
        else:
            self.led.value = 0.0  # Turn off LED

    def destroy(self):
        self.led.close()
        self.adc.close()
