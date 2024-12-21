#!/usr/bin/env python3
#############################################################################
# Filename    : Freenove_DHT.py
# Description :	DHT Temperature & Humidity Sensor library for Raspberry
# Author      : freenove
# modification: 2020/10/16
########################################################################
import RPi.GPIO as GPIO
import time
# from ..server import server_requests
from server import server_requests


gpio_to_physical = {2: 3, 3: 5, 4: 7, 14: 8, 15: 10, 17: 11, 
                    18: 12, 27: 13, 22: 15, 23: 16, 24: 18, 
                    10: 19, 9: 21, 25: 22, 11: 23, 8: 24, 7: 26, 
                    0: 27, 1: 28, 5: 29, 6: 31, 12: 32, 13: 33, 
                    19: 35, 16: 36, 26: 37, 20: 38, 21: 40}

class WeatherStation(object):
	DHTLIB_OK = 0
	DHTLIB_ERROR_CHECKSUM = -1
	DHTLIB_ERROR_TIMEOUT = -2
	DHTLIB_INVALID_VALUE = -999
	
	DHTLIB_DHT11_WAKEUP = 0.020#0.018		#18ms
	DHTLIB_TIMEOUT = 0.0001			#100us
	
	humidity = 0
	temperature = 0
	
	def __init__(self,pin_weatherSensor,sleeptime):
		self.pin = gpio_to_physical[pin_weatherSensor]
		self.bits = [0,0,0,0,0]
		GPIO.setmode(GPIO.BOARD)
		self.times_control_timer = 0
		# self.times_limit = 3/sleeptime # 30 seconds/ sleeptime
		self.times_limit = 30 # 30 seconds
        
	#Read DHT sensor, store the original data in bits[]	
	def readSensor(self,pin,wakeupDelay):
		mask = 0x80
		idx = 0
		self.bits = [0,0,0,0,0]
		# Clear sda
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,GPIO.HIGH)
		time.sleep(0.5)
		# start signal
		GPIO.output(pin,GPIO.LOW)
		time.sleep(wakeupDelay)
		GPIO.output(pin,GPIO.HIGH)
		# time.sleep(0.000001)
		GPIO.setup(pin,GPIO.IN)
		
		loopCnt = self.DHTLIB_TIMEOUT
		# Waiting echo
		t = time.time()
		while True:
			if (GPIO.input(pin) == GPIO.LOW):
				break
			if((time.time() - t) > loopCnt):
				return self.DHTLIB_ERROR_TIMEOUT
		# Waiting echo low level end
		t = time.time()
		while(GPIO.input(pin) == GPIO.LOW):
			if((time.time() - t) > loopCnt):
				#print ("Echo LOW")
				return self.DHTLIB_ERROR_TIMEOUT
		# Waiting echo high level end
		t = time.time()
		while(GPIO.input(pin) == GPIO.HIGH):
			if((time.time() - t) > loopCnt):
				#print ("Echo HIGH")
				return self.DHTLIB_ERROR_TIMEOUT
		for i in range(0,40,1):
			t = time.time()
			while(GPIO.input(pin) == GPIO.LOW):
				if((time.time() - t) > loopCnt):
					#print ("Data Low %d"%(i))
					return self.DHTLIB_ERROR_TIMEOUT
			t = time.time()
			while(GPIO.input(pin) == GPIO.HIGH):
				if((time.time() - t) > loopCnt):
					#print ("Data HIGH %d"%(i))
					return self.DHTLIB_ERROR_TIMEOUT		
			if((time.time() - t) > 0.00005):	
				self.bits[idx] |= mask
			#print("t : %f"%(time.time()-t))
			mask >>= 1
			if(mask == 0):
				mask = 0x80
				idx += 1	
		#print (self.bits)
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,GPIO.HIGH)
		return self.DHTLIB_OK
	#Read DHT sensor, analyze the data of temperature and humidity
	def readDHT11Once(self):
		rv = self.readSensor(self.pin,self.DHTLIB_DHT11_WAKEUP)
		if (rv is not self.DHTLIB_OK):
			self.humidity = self.DHTLIB_INVALID_VALUE
			self.temperature = self.DHTLIB_INVALID_VALUE
			return rv
		self.humidity = self.bits[0]
		self.temperature = self.bits[2] + self.bits[3]*0.1
		sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
		if(self.bits[4] is not sumChk):
			return self.DHTLIB_ERROR_CHECKSUM
		return self.DHTLIB_OK
	def readDHT11(self):
		result = self.DHTLIB_INVALID_VALUE
		for i in range(0,15):
			result = self.readDHT11Once()
			if result == self.DHTLIB_OK:
				return self.DHTLIB_OK
			time.sleep(0.1)
		return result

	# def printResult(self):
	# 	self.readDHT11Once()
	# 	print("Humidity : %.2f, \t Temperature : %.2f "%(self.humidity,self.temperature))
	
# Serverless mode
	def printResult(self):
		result = self.readDHT11()
		# print("times_control_timer: %d"%(self.times_control_timer))
		if self.times_control_timer <= 0:
			if result == self.DHTLIB_OK:
				print("Humidity : %.2f, \t Temperature : %.2f " % (self.humidity, self.temperature))
			else:
				print("Failed to read from DHT sensor")
			self.times_control_timer = self.times_limit
		else:
			self.times_control_timer -= 1

# Server mode
	def detect_temperature_server(self):
		result = self.readDHT11()
		if self.times_control_timer <= 0:
			if result == self.DHTLIB_OK:
				print("Humidity : %.2f, \t Temperature : %.2f " % (self.humidity, self.temperature))
				server_requests.temperature_sensor_change(self.temperature)
				server_requests.humidity_sensor_change(self.humidity)
			else:
				print("Failed to read from DHT sensor")
			self.times_control_timer = self.times_limit
		else:
			self.times_control_timer -= 1
        

# Destroy
	def destroy(self):
		GPIO.cleanup()
		# exit()


# def loop():
# 	dht = DHT(19)
# 	sumCnt = 0
# 	okCnt = 0
# 	while(True):
# 		sumCnt += 1
# 		# chk = dht.readDHT11()	
# 		chk = dht.readDHT11Once()
# 		# if (chk is 0):
# 		if (chk == 0):
# 			okCnt += 1		
# 		okRate = 100.0*okCnt/sumCnt;
# 		print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt,okRate))
# 		print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk,dht.humidity,dht.temperature))
# 		time.sleep(3)		
		
# if __name__ == '__main__':
# 	print ('Program is starting ... ')
# 	try:
# 		loop()
# 	except KeyboardInterrupt:
# 		pass
# 		exit()		
		
		
