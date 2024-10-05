from gpiozero import LED, MotionSensor, PWMLED
import time
from ADCDevice import *

class PirSensor:
    def __init__(self, led_pin, sensor_pin):
        self.led = LED(led_pin)
        self.sensor = MotionSensor(sensor_pin)
        self.previous_state = False

    def detect_motion(self):
        current_state = self.sensor.motion_detected
        if current_state and not self.previous_state:
            self.led.on()
            # print("Motion detected! PIR LED turned on >>>")
            self.previous_state = True
        elif not current_state and self.previous_state:
            self.led.off()
            # print("No Motion! PIR LED turned off <<")
            self.previous_state = False

    def destroy(self):
        self.led.close()
        self.sensor.close()

class PhotoResistor:
    def __init__(self, led_pin, threshold=128):
        self.led = PWMLED(led_pin)
        self.adc = ADCDevice()
        self.threshold = threshold
        self.setup()

    def setup(self):
        if self.adc.detectI2C(0x48):  # Detect the pcf8591.
            self.adc = PCF8591()
        elif self.adc.detectI2C(0x4b):  # Detect the ads7830
            self.adc = ADS7830()
        else:
            print("No correct I2C address found. Program Exit.")
            exit(-1)

    def adjust_led_brightness(self, motion_detected):
        value = self.adc.analogRead(0)  # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3
        # print(f'ADC Value: {value}, Voltage: {voltage:.2f}V')

        if motion_detected and value > self.threshold:
            self.led.value = 1.0  # Turn on LED to maximum brightness
            # print("Low light detected! Photoresistor LED turned on >>>")
        else:
            self.led.value = 0.0  # Turn off LED
            # print("Sufficient light or no motion! Photoresistor LED remains off <<")

    def destroy(self):
        self.led.close()
        self.adc.close()


class StreetLight:
    def __init__(self, pir_led_pin, pir_sensor_pin, photo_led_pin, threshold=128):
        self.pir_sensor = PirSensor(pir_led_pin, pir_sensor_pin)
        self.photo_resistor = PhotoResistor(photo_led_pin, threshold)

    def control_lights(self):
        self.pir_sensor.detect_motion()
        motion_detected = self.pir_sensor.previous_state  # Verifica si el PIR detecta movimiento
        self.photo_resistor.adjust_led_brightness(motion_detected)

    def destroy(self):
        self.pir_sensor.destroy()
        self.photo_resistor.destroy()
