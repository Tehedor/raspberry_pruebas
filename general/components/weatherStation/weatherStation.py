#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2020/10/16
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 11      #define the pin of DHT11

def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15):            
            chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                print("DHT11,OK!")
                break
            time.sleep(0.1)
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)       
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()  



class WheaterStation:
    def __init__(self, pin_weatherSensor, sleeptime):
        self.sensor = DistanceSensor(echo=pin_ultrasound_echo, trigger=pin_ultrasound_trig ,max_distance=3)
        self.last_temperature = 0.0
        self.times_control_timer = 0
        self.times_limit = 3/sleeptime # 30 seconds
        
    def detect_weather(self):
        current_distance = self.sensor.distance * 100
        if current_distance != self.last_distance:
            self.last_distance = current_distance
            return current_distance
        return None
    
    def print_distance(self):
        current_distance = self.sensor.distance * 100
        # if current_distance != self.last_distance:
        #     self.last_distance = current_distance
        #     print(f"Distance: {current_distance} cm")
        if abs(current_distance - self.last_distance) >= 0.5:
            self.last_distance = current_distance
            print(f"Distance: {current_distance} cm")
        
        
    def destroy(self):
        GPIO.cleanup()
        self.sensor.close()