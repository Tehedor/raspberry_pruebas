# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# import time

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# # GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
# GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)

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

# try:
#     while True: # Run forever

            
#         if GPIO.input(5) == GPIO.HIGH:
#             # sock = socket.socket(socket.AF_INET, # Internet
#             #             #  socket.SOCK_DGRAM) # UDP
#             # sock.sendto(MESSAGE2_B, (UDP_IP, UDP_PORT)) #
            
#             time.sleep(0.5)
#             print("State 1")
#         else:
#             # sock = socket.socket(socket.AF_INET, # Internet
#             #              socket.SOCK_DGRAM) # UDP
#             # sock.sendto(MESSAGE1_B, (UDP_IP, UDP_PORT)) #
#             time.sleep(0.5) 
#             print("State 0")
# except KeyboardInterrupt:
#     # Clean up GPIO on exit
#     GPIO.cleanup()

############################################################################################################
############################################################################################################


import RPi.GPIO as GPIO

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for your switch
SWITCH_PIN = 6

# Define debounce time in milliseconds
DEBOUNCE_TIME_MS = 200  # 200 milliseconds

# Set the initial state and pull-up resistor for the switch
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the switch state and previous state
switch_state = GPIO.input(SWITCH_PIN)
prev_switch_state = switch_state

# Define a function to handle switch presses
def switch_callback(channel):
    global switch_state
    switch_state = GPIO.input(SWITCH_PIN)

# Add an event listener for the switch press
# GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=DEBOUNCE_TIME_MS)
GPIO.add_event_detect(SWITCH_PIN, switch_state ,callback=switch_callback, bouncetime=DEBOUNCE_TIME_MS)

try:
    # Main loop
    while True:
        # Check if the switch state has changed
        if switch_state != prev_switch_state:
            if switch_state == GPIO.HIGH:
                print("The switch: ON -> OFF")
            else:
                print("The switch: OFF -> ON")
            
            prev_switch_state = switch_state


        if switch_state == GPIO.HIGH:
            print("The switch: OFF")
        else:
            print("The switch: ON")

except KeyboardInterrupt:
    # Clean up GPIO on exit
    GPIO.cleanup()



############################################################################################################
############################################################################################################
############################################################################################################

# import RPi.GPIO as GPIO
# import time

# # Set the GPIO mode to BCM
# GPIO.setmode(GPIO.BCM)

# # Define the GPIO pin for your switch
# SWITCH_PIN = 6

# # Define debounce time in milliseconds
# DEBOUNCE_TIME_MS = 200  # 200 milliseconds

# # Set the initial state and pull-up resistor for the switch
# GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Initialize the switch state and previous state
# switch_state = GPIO.input(SWITCH_PIN)
# prev_switch_state = switch_state

# # Define a function to handle switch presses
# def switch_callback(channel):
#     global switch_state, prev_switch_state
#     switch_state = GPIO.input(SWITCH_PIN)
#     if switch_state != prev_switch_state:
#         if switch_state == GPIO.HIGH:
#             print("The switch: ON -> OFF")
#         else:
#             print("The switch: OFF -> ON")
#         prev_switch_state = switch_state

# # Add an event listener for the switch press
# GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=DEBOUNCE_TIME_MS)

# try:
#     # Main loop
#     while True:
#         time.sleep(1)  # Sleep to reduce CPU usage

# except KeyboardInterrupt:
#     # Clean up GPIO on exit
#     GPIO.cleanup()
