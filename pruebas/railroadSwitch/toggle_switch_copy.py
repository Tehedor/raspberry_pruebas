from gpiozero import Button

button = Button(26)
# button = Button(37)
# button.wait_for_press()
# print("The button was pressed!")




def loop():
    state = 0
    pressed = 0
    
    while True:
        if button.is_pressed:  # if button is pressed
            state = 1     
            print("State 1")
        else : # if button is relessed
            # print("Button is released") 
            pressed = 0   
            print("State 0")