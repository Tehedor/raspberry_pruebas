from gpiozero import LED, MotionSensor, PWMLED
import time
from ADCDevice import *
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
            self.previous_state[0] = True
        elif not current_state and self.previous_state[0]:
            self.led.off()
            self.previous_state[0] = False
    
    # Server mode
    def detect_motion_server_pir(self,update_motion_state, previous_state):
        current_state = self.sensor.motion_detected
        if current_state and not previous_state:
            server_requests.pir_sensor_change(current_state)
            # self.previous_state[0] = True
            update_motion_state(True)
        elif not current_state and previous_state:
            server_requests.pir_sensor_change(current_state)
            update_motion_state(False)
            # self.previous_state[0] = False

    def detect_motion_server_led(self, state):
        if state:
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
    def __init__(self, led_pin, previous_state, threshold=128):
        self.led = PWMLED(led_pin)
        self.adc = ADCDevice()
        self.threshold = threshold
        self.previous_intensity = 0
        self.previous_state = previous_state
        self.previous_light_state = False
        self.enable_intensity = False
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
        if motion_detected and value < self.threshold:
            self.led.value = 1.0  # Turn on LED to maximum brightness
        else:
            self.led.value = 0.0  # Turn off LED

    # Server mode
    def detect_intensity_server_photo(self):
        value = self.adc.analogRead(0)  # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3
        intensity = value
        # print(f'ADC Value: {value}, Voltage: {intensity:.2f}V')
        # if abs(intensity - self.previous_intensity) > 0.1:
        #     server_requests.photoresistor_sensor_change(intensity)
        self.previous_intensity = intensity

    def detect_intensity_server_light(self, intensity, previous_state):
        print(f'ADC Value: {intensity}, Voltage: {intensity:.2f}V')
        print(f'Motion Detected: {previous_state}')
        print(f'Light State: {self.previous_light_state}')
        if intensity > self.threshold:
            self.enable_intensity = True
            if not self.previous_light_state and previous_state:
                self.led.value = 1.0  # Turn on LED to maximum brightness
                server_requests.light_change(True)
                print('## ## ## ## ## ## ##')
                print('ON light intensity')
                print('## ## ## ## ## ## ##')
                self.previous_light_state = True
                
        elif self.previous_light_state:
            self.enable_intensity = False
            if self.previous_light_state and not previous_state:
                self.led.value = 0.0
                server_requests.light_change(False)
                print('## ## ## ## ## ## ##')
                print('OFF light intensity')
                print('## ## ## ## ## ## ##')
                self.previous_light_state = False
            
        # if not self.previous_light_state and intensity < self.threshold:
        #     self.led.value = 1.0  # Turn on LED to maximum brightness
        #     server_requests.light_change(True)
        #     print('## ## ## ## ## ## ##')
        #     print('ON light intensity')
        #     print('## ## ## ## ## ## ##')
        #     self.previous_light_state = True
        # elif self.previous_light_state:
        #     self.led.value = 0.0  # Turn off LED
        #     server_requests.light_change(False)
        #     print('## ## ## ## ## ## ##')
        #     print('OFF light intensity')
        #     print('## ## ## ## ## ## ##')
        #     self.previous_light_state = False

    def detect_intensity_server_light_state(self, state):
        if not self.previous_light_state and state and self.enable_intensity:
            self.led.value = 1.0  # Turn on LED to maximum brightness
            server_requests.light_change(True)
            print('## ## ## ## ## ## ##')
            print('ON light state')
            print('## ## ## ## ## ## ##')
            self.previous_light_state = True
        elif self.previous_light_state and not state:
            self.led.value = 0.0  # Turn off LED
            server_requests.light_change(False)
            print('## ## ## ## ## ## ##')
            print('OFF light state')
            print('## ## ## ## ## ## ##')
            self.previous_light_state = False

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
        self.photo_resistor = PhotoResistor(photo_led_pin, self.previous_state, threshold)

    def control_lights(self):
        self.pir_sensor.detect_motion()  # cambiar estado a si se detecta
        motion_detected = self.previous_state[0]  # Verifica si el PIR detecta movimiento
        self.photo_resistor.adjust_led_brightness(motion_detected)  # ajustar el brillo en función de si se detecta o no


    def update_motion_state(self, state):
        self.previous_state[0] = state
        print(f"[StreetLight] Motion state updated to: {state}")


    # Server mode
    def control_lights_server(self):
        self.control_lights_server_pir()
        self.control_lights_server_photo()

    # PirSensor class
    def control_lights_server_pir(self):
        self.pir_sensor.detect_motion_server_pir(self.update_motion_state, self.previous_state[0])

    def control_lights_server_led(self, state):
        self.pir_sensor.detect_motion_server_led(state)

    # PhotoResistor class
    def control_lights_server_photo(self):
        self.photo_resistor.detect_intensity_server_photo()

    def control_lights_server_light(self, intensity):
        self.photo_resistor.detect_intensity_server_light(intensity, self.previous_state[0])

    def control_lights_server_light_state(self, state):
        self.photo_resistor.detect_intensity_server_light_state(state)

    # Destroy 
    def destroy(self):
        self.pir_sensor.destroy()
        self.photo_resistor.destroy()