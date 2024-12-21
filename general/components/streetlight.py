from gpiozero import LED, MotionSensor, PWMLED
import time
from ADCDevice import *
# import ..server.server_requests as server_requests
from server import server_requests

# ** ##### ** ##### ** ##### ** ##### ** #
# ** PirSensor class
# ** ##### ** ##### ** ##### ** ##### ** #
class PirSensor:
    def __init__(self, led_pin, sensor_pin, previous_state):
        self.led = LED(led_pin)
        self.sensor = MotionSensor(sensor_pin)
        self.previous_state = previous_state

    # Serverless mode
    def detect_motion(self):
        current_state = self.sensor.motion_detected
        if current_state and not self.previous_state[0]:
            self.led.on()
            # print("Motion detected! PIR LED turned on >>>")
            self.previous_state[0] = True
        elif not current_state and self.previous_state[0]:
            self.led.off()
            # print("No Motion! PIR LED turned off <<")
            self.previous_state[0] = False
    
    # Server mode
    def detect_motion_server_pir(self):
        current_state = self.sensor.motion_detected
        
        if current_state and not self.previous_state[0]:
            # 'ON'
            server_requests.pir_sensor_change(current_state)
            self.previous_state[0] = True
        elif not current_state and self.previous_state[0]:
            # 'OFF'
            server_requests.pir_sensor_change(current_state)
            self.previous_state[0] = False

    def detect_motion_server_led(self, state):
        if state == True:
            self.led.on()
            print('## ## ## ## ## ## ##')
            print('ON led')
            print('## ## ## ## ## ## ##')
            server_requests.led_detection_change('ON')
        else:
            print('## ## ## ## ## ## ##')
            print('OFF led')
            print('## ## ## ## ## ## ##')
            self.led.off()
            server_requests.led_detection_change('OFF')
        # if state == 'ON':
        #     self.led.on()
        #     server_requests.led_detection_change('ON')
        # else:
        #     self.led.off()
        #     server_requests.led_detection_change('OFF')

    # Destroy 
    def destroy(self):
        self.led.close()
        self.sensor.close()

# ** ##### ** ##### ** ##### ** ##### ** #
# ** PhotoResistor class
# ** ##### ** ##### ** ##### ** ##### ** #
class PhotoResistor:
    def __init__(self, led_pin, previous_state, threshold=128):
        self.led = PWMLED(led_pin)
        self.adc = ADCDevice()
        self.threshold = threshold
        self.previous_intensity = 0
        self.previous_state = previous_state
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
        # print('@@@@@@@@@@@@@@@@@@@@@@')
        # print(intensity)
        # print(self.previous_intensity)
        if abs(intensity - self.previous_intensity) > 0.1:
            server_requests.photoresistor_sensor_change(intensity)
        self.previous_intensity = intensity

    def detect_intensity_server_light(self, intensity):
        print(f'ADC Value: {intensity}, Voltage: {intensity:.2f}V')
        print(f'Motion Detected: {self.previous_state[0]}')
        print('@@@@@@@@')
        print(intensity)
        print('@@@@@@@@')
        if self.previous_state[0] and (intensity > self.threshold):
        # if self.previous_state[0] and intensity > self.threshold:
            self.led.value = 1.0  # Turn on LED to maximum brightness
            server_requests.light_change(True)
            print('## ## ## ## ## ## ##')
            print('ON light intensity')
            print('## ## ## ## ## ## ##')
            # print("Low light detected! Photoresistor LED turned on >>>")
            # server_requests.light_change('ON')
        else:
            self.led.value = 0.0  # Turn off LED
            print('## ## ## ## ## ## ##')
            print('OFF light intensity')
            print('## ## ## ## ## ## ##')
            server_requests.light_change(False)
            # print("Sufficient light or no motion! Photoresistor LED remains off <<")
            # server_requests.light_change('OFF')
    
    def detect_intensity_server_light_state(self, state):
        # print(f'ADC Value: {intensity}, Voltage: {intensity:.2f}V')
        print(f'Motion Detected: {self.previous_state[0]}')
        if self.previous_state[0]:
            self.led.value = 1.0  # Turn on LED to maximum brightness
            print('## ## ## ## ## ## ##')
            print('ON light state')
            print('## ## ## ## ## ## ##')
            server_requests.light_change(True)
            # print("Low light detected! Photoresistor LED turned on >>>")
            # server_requests.light_change('ON')
        else:
            self.led.value = 0.0  # Turn off LED
            print('## ## ## ## ## ## ##')
            print('OFF light state')
            print('## ## ## ## ## ## ##')
            server_requests.light_change(False)
            # print("Sufficient light or no motion! Photoresistor LED remains off <<")
            # server_requests.light_change('OFF')

    def destroy(self):
        self.led.close()
        self.adc.close()

# ** ##### ** ##### ** ##### ** ##### ** #
# ** StreetLight class
# ** ##### ** ##### ** ##### ** ##### ** #
class StreetLight:
    def __init__(self, pir_led_pin, pir_sensor_pin, photo_led_pin, threshold=128):
        self.previous_state = [False]
        self.pir_sensor = PirSensor(pir_led_pin, pir_sensor_pin, self.previous_state)
        self.photo_resistor = PhotoResistor(photo_led_pin, threshold, self.previous_state)
        

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

    def control_lights_server_light_state(self, state):
        # motion_detected = self.pir_sensor.previous_state  # Verifica si el PIR detecta movimiento
        self.photo_resistor.detect_intensity_server_light_state(state)
    
    def control_lights_server_light(self, intensity):
        # motion_detected = self.pir_sensor.previous_state  # Verifica si el PIR detecta movimiento
        self.photo_resistor.detect_intensity_server_light(intensity)
    

# Destroy 
    def destroy(self):
        self.pir_sensor.destroy()
        self.photo_resistor.destroy()
