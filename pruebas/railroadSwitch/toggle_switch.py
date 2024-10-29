# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# SWITCH_PIN = 6

# DEBOUNCE_TIME_MS = 200  # 200 milliseconds

# GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# switch_state = GPIO.input(SWITCH_PIN)

# prev_switch_state = switch_state

# try:
#     # Main loop
#     while True:
#         switch_state = GPIO.input(SWITCH_PIN)
#         if switch_state != prev_switch_state:
#             if switch_state == GPIO.HIGH:
#                 print("The switch: ON -> OFF")
#             else:
#                 print("The switch: OFF -> ON")
            
#             prev_switch_state = switch_state


# except KeyboardInterrupt:
#     GPIO.cleanup()



############################################################################################################
############################################################################################################
############################################################################################################
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# SWITCH_PIN = 6

# DEBOUNCE_TIME_MS = 200  # 200 milliseconds

# GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# switch_state = GPIO.input(SWITCH_PIN)
# prev_switch_state = switch_state

# def switch_callback(channel):
#     global switch_state, prev_switch_state
#     switch_state = GPIO.input(SWITCH_PIN)
#     if switch_state != prev_switch_state:
#         if switch_state == GPIO.HIGH:
#             print("The switch: ON -> OFF")
#         else:
#             print("The switch: OFF -> ON")
#         prev_switch_state = switch_state

# GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=DEBOUNCE_TIME_MS)

# try:
#     # Main loop
#     while True:
#         pass  # Do other tasks here

# except KeyboardInterrupt:
#     GPIO.cleanup()

############################################################################################################
############################################################################################################
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

btn_input = 6
# LED_output = 17;

# GPIO btn_input set up as input.
GPIO.setup(btn_input, GPIO.IN)
# GPIO.setup(LED_output, GPIO.OUT)

# handle the button event
def buttonEventHandler (pin):
    # turn LED on/off
    # GPIO.output(LED_output,True)
    # time.sleep(5)
    # GPIO.output(LED_output,False)
    print("Button pressed")

GPIO.add_event_detect(btn_input, GPIO.RISING, callback=buttonEventHandler)  
try:  
    GPIO.wait_for_edge(btn_input, GPIO.FALLING)  
except:
    GPIO.cleanup()   