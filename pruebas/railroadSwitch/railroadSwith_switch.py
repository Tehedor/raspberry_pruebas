from gpiozero import Button, AngularServo
import time

switch = Button(26)  # define Button pin according to BCM Numbering
myGPIO = 21

myCorrection = 0.0
maxPW = (2.5 + myCorrection) / 1000
minPW = (0.5 - myCorrection) / 1000
servo = AngularServo(myGPIO, initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=minPW, max_pulse_width=maxPW)

def loop():
    state = 0
    
    while True:
        if switch.is_pressed:  # if switch is pressed
            if state == 0:
                state = 1
                print("State 1")
                for angle in range(0, 181, 1):  # make servo rotate from 0 to 180 deg
                    servo.angle = angle
            # state = 1     
        else:  # if switch is released
            if state == 1:
                state = 0
                print("State 0")
                for angle in range(180, -1, -1):  # make servo rotate from 180 to 0 deg
                    servo.angle = angle

if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")