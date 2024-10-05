from gpiozero import PWMLED
import time
from ADCDevice import *

ledPin = 27 # define ledPin
led = PWMLED(ledPin)
adc = ADCDevice() # Define an ADCDevice class object
threshold = 128  # Define un umbral de intensidad (puedes ajustarlo según necesites)

def setup():
	global adc
	if(adc.detectI2C(0x48)): # Detect the pcf8591.
		adc = PCF8591()
	elif(adc.detectI2C(0x4b)): # Detect the ads7830
		adc = ADS7830()
	else:
		print("No correct I2C address found, \n"
		"Please use command 'i2cdetect -y 1' to check the I2C address! \n"
		"Program Exit. \n")
		exit(-1)

def loop():
	while True:
		value = adc.analogRead(0)  # read the ADC value of channel 0
		voltage = value / 255.0 * 3.3
		print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))

		# Control de encendido/apagado basado en el umbral
		if value > threshold:
			led.value = 1.0  # Encender LED a máxima intensidad
		else:
			led.value = 0.0  # Apagar LED

		time.sleep(0.01)

def destroy():
	led.close()
	adc.close()

if __name__ == '__main__': # Program entrance
	print ('Program is starting ... ')
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
		print("Ending program")
