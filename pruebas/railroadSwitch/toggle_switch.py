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
# import RPi.GPIO as GPIO
# import time

# # Configurar GPIO
# GPIO.setmode(GPIO.BCM)  # Usar numeración BCM
# pin_interruptor = 26  # Ajusta según tu configuración
# GPIO.setup(pin_interruptor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down

# def interruptor_cambiado(canal):
#     # Función llamada cuando ocurre un evento en el interruptor
#     if GPIO.input(pin_interruptor) == GPIO.HIGH:
#         print("Interruptor encendido")
#     else:
#         print("Interruptor apagado")

# # Agregar detector de eventos
# GPIO.add_event_detect(pin_interruptor, GPIO.BOTH, callback=interruptor_cambiado, bouncetime=300)

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     GPIO.cleanup()


#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIimport 
import time
import threading
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
PIN = 26
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.IN)

def handle(channel):
    movement = GPIO.input(PIN)
    if movement:
        print("Movement")
    else:
        print("No movement")

print("Setting up event detect")
worked = False
while not worked:
    # keep trying to set up event detect based on suggestion in 
    # https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=129015&p=874227#p874227
    worked = True
    try:
        GPIO.add_event_detect(PIN, GPIO.BOTH, handle)
    except RuntimeError:
        worked = False

print("We are running!")  # This never prints, never gets out of above while loop

try:
    while True:
        time.sleep(1e6)
except KeyboardInterrupt:
    print("Exiting program")
    GPIO.cleanup()