import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)

# import socket

# UDP_IP = "<my.ip.address>"
# UDP_PORT = 50007
# MESSAGE1 = "$ Channel 1 Thru 5 @ FULL #"
# MESSAGE1_B = bytes(MESSAGE1, 'utf-8')
# MESSAGE2 = "$ Channel 1 thru 5 @ 0 #"
# MESSAGE2_B = bytes(MESSAGE2, 'utf-8')

# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# print("message: %s" % MESSAGE1)
# print("message: %s" % MESSAGE2)


while True: # Run forever

        
    if GPIO.input(26) == GPIO.HIGH:
        # sock = socket.socket(socket.AF_INET, # Internet
        #             #  socket.SOCK_DGRAM) # UDP
        # sock.sendto(MESSAGE2_B, (UDP_IP, UDP_PORT)) #
        
        time.sleep(0.5)
        print("State 1")
    else:
        # sock = socket.socket(socket.AF_INET, # Internet
        #              socket.SOCK_DGRAM) # UDP
        # sock.sendto(MESSAGE1_B, (UDP_IP, UDP_PORT)) #
        time.sleep(0.5) 
        print("State 0")