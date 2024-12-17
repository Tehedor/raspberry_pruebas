import time
import os
from picamera2 import Picamera2, Preview
from gpiozero import Button
from ftplib import FTP

# from ..server import server_requests
from server import server_requests


class Radar:
    def __init__(self, pin_button):
        self.button = Button(pin_button) 
        self.file_path = os.path.expanduser("~/Desktop/pictures/")     
        self.presence_state = False
        os.makedirs(self.file_path, exist_ok=True)  # Crear la carpeta si no existe
        self.ftp_host = os.getenv('FTP_HOST')
        self.ftp_user = os.getenv('FTP_USER')
        self.ftp_password = os.getenv('FTP_PASSWORD')
        self.remote_folder = os.getenv('REMOTE_FOLDER')


    def make_photo(self):
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
        picam2.configure(preview_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(0.5)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        local_file = os.path.join(self.file_path, f"image_{timestamp}.jpg")
        metadata = picam2.capture_file(local_file)
        # print ('Hello.a photo has been to taken successfully')   # print information on terminal
        picam2.close()
        # print ('Please preess the button take a photo')
        return local_file
        
# Serverless mode
    def control_button(self):
        if self.button.is_pressed:  # if button is pressed
            self.make_photo()

    # def broker_control_button(self):
    #     if self.button.is_pressed:  # if button is pressed
    #         self.send_request()
# Server mode
    
    def control_button_server(self):
        if self.button.is_pressed:
            server_requests.infrared_sensor_change(True)
            self.presence_state = True
        else:
            if self.presence_state == True:
                server_requests.infrared_sensor_change(False)
                self.presence_state = False

    def control_camera_server(self, state):
        if state == 'ON':
            local_file = self.make_photo() 
            self.upload_to_ftp(local_file)
            server_requests.camera_change(local_file)
        else:
            pass

    def upload_to_ftp(self, local_file):
        try:
            with FTP(self.ftp_host) as ftp:
                ftp.login(user=self.ftp_user, passwd=self.ftp_password)
                ftp.cwd(self.remote_folder)  # Cambiar al directorio remoto
                with open(local_file, "rb") as file:
                    ftp.storbinary(f"STOR {os.path.basename(local_file)}", file)
                print(f"Foto subida exitosamente a FTP: {os.path.basename(local_file)}")
        except Exception as e:
            print(f"Error al subir la foto: {e}")

    
    
# Destroy
    def destroy(self):
        self.button.close()