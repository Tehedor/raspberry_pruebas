from gpiozero import Button
import time


button = Button(19) # define Button pin according to BCM Numbering

def loop():
    state = 0
    control = 1
    
    while True:
        if button.is_pressed:  # if button is pressed
            print("Button is pressed") # print information on terminal 
            if control == 1:
                control = 0
                print("1")
                state = 1 
        else : # if button is relessed
            control = 1
            if state == 1:
                print("0")
                state = 0

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")
