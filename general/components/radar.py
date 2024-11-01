import time
import os
from picamera2 import Picamera2, Preview
from gpiozero import Button

class Radar:
    def __init__(self, pin_button):
        self.button = Button(pin_button) 
        self.file_path = os.path.expanduser("~/Desktop/pictures/")     
        
    def make_photo(self):
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
        picam2.configure(preview_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(0.5)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file = os.path.join(self.file_path, f"image_{timestamp}.jpg")
        metadata = picam2.capture_file(file)
        # print ('Hello.a photo has been to taken successfully')   # print information on terminal
        picam2.close()
        # print ('Please preess the button take a photo')
        
    def control_button(self):
        if self.button.is_pressed:  # if button is pressed
            self.make_photo()

    def broker_control_button(self):
        if self.button.is_pressed:  # if button is pressed
            self.send_request()
        
    def destroy():
        button.close()