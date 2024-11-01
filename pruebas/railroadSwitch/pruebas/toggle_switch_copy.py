from gpiozero import Button

button = Button(26)


def loop():
    if button.is_pressed:
        state = 1
    else:
        state = 0
    
    while True:
        if button.is_pressed:  # if button is pressed
            if state == 0 :
                state = 1
                print("State 1")
            # state = 1     
        else : # if button is relessed
            # print("Button is released") 
            if state == 1:
                state = 0
                print("State 0")
            
            
if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")
