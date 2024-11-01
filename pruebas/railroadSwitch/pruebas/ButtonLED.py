# from gpiozero import Button,AngularServo
from gpiozero import Button
import time


button = Button(20) # define Button pin according to BCM Numbering
myGPIO=21

# SERVO_DELAY_SEC = 0.001 
myCorrection=0.0
maxPW=(2.5+myCorrection)/1000
minPW=(0.5-myCorrection)/1000
# servo =  AngularServo(myGPIO,initial_angle=0,min_angle=0, max_angle=180,min_pulse_width=minPW,max_pulse_width=maxPW)



def loop():
    state = 0
    pressed = 0
    
    while True:
        if button.is_pressed:  # if button is pressed
            print("Button is pressed") # print information on terminal 
            if pressed == 0:
                state = 1 - state
                pressed = 1
            if state == 1:
                # for angle in range(0, 181, 1):   # make servo rotate from 0 to 180 deg
                #     servo.angle = angle
                # time.sleep(SERVO_DELAY_SEC)
                print("1")
            else:
                # for angle in range(180, -1, -1): # make servo rotate from 180 to 0 deg
                #     servo.angle = angle
                # time.sleep(SERVO_DELAY_SEC)
                print("0")
            
        else : # if button is relessed
            # print("Button is released") 
            pressed = 0   

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")
