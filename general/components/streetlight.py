from gpiozero import LED, MotionSensor, PWMLED
import time
from ADCDevice import *
# import ..server.server_requests as server_requests
from server import server_requests

# ** ##### ** ##### ** ##### ** ##### ** #
# ** PirSensor class
# ** ##### ** ##### ** ##### ** ##### ** #
class PirSensor:
    def __init__(self, led_pin, sensor_pin):
        self.led = LED(led_pin)
        self.sensor = MotionSensor(sensor_pin)
        self.previous_state = False

    # Serverless mode
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
    
    # Server mode
    def detect_motion_server_pir(self):
        current_state = self.sensor.motion_detected
        
        if current_state and not self.previous_state:
            # 'ON'
            server_requests.pir_sensor_change(current_state)
            self.previous_state = True
        elif not current_state and self.previous_state:
            # 'OFF'
            server_requests.pir_sensor_change(current_state)
            self.previous_state = False

    def detect_motion_server_led(self, state):
        if state == 'ON':
            self.led.on()
            server_requests.led_detection_change('ON')
        else:
            self.led.off()
            server_requests.led_detection_change('OFF')

    # Destroy 
    def destroy(self):
        self.led.close()
        self.sensor.close()

# ** ##### ** ##### ** ##### ** ##### ** #
# ** PhotoResistor class
# ** ##### ** ##### ** ##### ** ##### ** #
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

    # Serverless mode
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

    # Server mode
    def detect_intensity_server_photo(self):
        value = self.adc.analogRead(0)  # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3
        intensity = voltage
        server_requests.photoresistor_sensor_change(intensity)

    def detect_intensity_server_light(self, intensity,motion_detected):
        if motion_detected and intensity > self.threshold:
            self.led.value = 1.0  # Turn on LED to maximum brightness
            # print("Low light detected! Photoresistor LED turned on >>>")
            server_requests.light_change('ON')
        else:
            self.led.value = 0.0  # Turn off LED
            # print("Sufficient light or no motion! Photoresistor LED remains off <<")
            server_requests.light_change('OFF')

    def destroy(self):
        self.led.close()
        self.adc.close()

# ** ##### ** ##### ** ##### ** ##### ** #
# ** StreetLight class
# ** ##### ** ##### ** ##### ** ##### ** #
class StreetLight:
    def __init__(self, pir_led_pin, pir_sensor_pin, photo_led_pin, threshold=128):
        self.pir_sensor = PirSensor(pir_led_pin, pir_sensor_pin)
        self.photo_resistor = PhotoResistor(photo_led_pin, threshold)

    def control_lights(self):
        self.pir_sensor.detect_motion() # cambiar estado a si se tetecta
        motion_detected = self.pir_sensor.previous_state  # Verifica si el PIR detecta movimiento
        self.photo_resistor.adjust_led_brightness(motion_detected) # ajustar el brillo en funcion de si se detecta o no


# Server mode
    def control_lights_server(self):
        self.control_lights_server_pir()
        self.control_lights_server_photo()

# PirSenor class
    def control_lights_server_pir(self):
        self.pir_sensor.detect_motion_server_pir()

    def control_lights_server_led(self, state):
        self.pir_sensor.detect_motion_server_led(state)

# PhotoResistor class
    def control_lights_server_photo(self):
        self.photo_resistor.detect_intensity_server_photo()

    def control_lights_server_light(self, state):
        motion_detected = self.pir_sensor.previous_state  # Verifica si el PIR detecta movimiento
        self.photo_resistor.detect_intensity_server_light(state, motion_detected)

# Destroy 
    def destroy(self):
        self.pir_sensor.destroy()
        self.photo_resistor.destroy()
