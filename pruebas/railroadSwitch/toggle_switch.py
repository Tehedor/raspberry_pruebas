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
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SWITCH_PIN = 6

DEBOUNCE_TIME_MS = 200  # 200 milliseconds

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

switch_state = GPIO.input(SWITCH_PIN)
prev_switch_state = switch_state

def switch_callback(channel):
    global switch_state, prev_switch_state
    switch_state = GPIO.input(SWITCH_PIN)
    if switch_state != prev_switch_state:
        if switch_state == GPIO.HIGH:
            print("The switch: ON -> OFF")
        else:
            print("The switch: OFF -> ON")
        prev_switch_state = switch_state

GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=DEBOUNCE_TIME_MS)

try:
    # Main loop
    while True:
        pass  # Do other tasks here

except KeyboardInterrupt:
    GPIO.cleanup()