from gpiozero import Button
import time


button = Button(19) # define Button pin according to BCM Numbering

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
                print("1")
            else:
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
