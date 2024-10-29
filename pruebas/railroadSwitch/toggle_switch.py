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
import RPi.GPIO as GPIO
import time

# Configurar GPIO
GPIO.setmode(GPIO.BCM)  # Usar numeración BCM
pin_interruptor = 26  # Ajusta según tu configuración
GPIO.setup(pin_interruptor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down

def interruptor_cambiado(canal):
    # Función llamada cuando ocurre un evento en el interruptor
    if GPIO.input(pin_interruptor) == GPIO.HIGH:
        print("Interruptor encendido")
    else:
        print("Interruptor apagado")

# Agregar detector de eventos
GPIO.add_event_detect(pin_interruptor, GPIO.BOTH, callback=interruptor_cambiado, bouncetime=300)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()