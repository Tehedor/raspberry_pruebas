from gpiozero import Button
import time

button = Button(12)  # define Button pin according to BCM Numbering

def loop():
    while True:
        if button.is_pressed:  # if button is pressed
            print("Button is pressed")  # print information on terminal
        else:
            print("Button is released")
        time.sleep(0.1)  # add a small delay to avoid flooding the terminal

if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("Ending program")