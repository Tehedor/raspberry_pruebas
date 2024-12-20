import time
import os
from picamera2 import Picamera2, Preview
from gpiozero import Button
from ftplib import FTP

# from ..server import server_requests
from server import server_requests

# from radar import subir_foto
from minio import Minio
from minio.error import S3Error  # Importar S3Error para manejar los errores


minio_client = Minio(
    "138.4.22.12:80",  # Dirección de tu servidor MinIO
    access_key="admin",  # Tu access key
    secret_key="admin123",  # Tu secret key
    secure=False  # Establece en True si estás usando HTTPS
)


class Radar:
    def __init__(self, pin_button):
        self.button = Button(pin_button) 
        self.file_path = os.path.expanduser("/home/admin/Desktop//pictures/")     
        self.presence_state = False


    def make_photo(self):
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
        picam2.configure(preview_config)
        # picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(0.5)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        print("a")
        local_file = os.path.join(self.file_path, f"image_{timestamp}.jpg")
        print("b")
        metadata = picam2.capture_file(local_file)
        print("c")
        # print ('Hello.a photo has been to taken successfully')   # print information on terminal
        picam2.close()
        # print ('Please preess the button take a photo')
        print(f"Photo taken: {local_file}")
        return local_file,timestamp
        
        
        
        
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
        if state == True:
            local_file,timestamp = self.make_photo() 
            
            
            # Subir la imagen a MinIO
            bucket_name = "bucketfotos"
            folder_name = "photostrain"
            # object_name = f"{folder_name}/" + local_file.split("/")[-1]
            object_name = f"{folder_name}/" + os.path.basename(local_file)

            try:
                # Verifica si el bucket existe, si no, crea uno
                if not minio_client.bucket_exists(bucket_name):
                    print(f"Bucket {bucket_name} no existe, creándolo...")
                    minio_client.make_bucket(bucket_name)

                # Subir el archivo
                minio_client.fput_object(bucket_name, object_name, local_file)
                print(f"Imagen subida exitosamente: {object_name}")
                media_url = f"http://"
                state_camera = True
                server_requests.camera_change(state_camera,media_url,timestamp)
            except S3Error as err:
                print(f"Error al subir la imagen: {err}")            
            
        else:
            pass

    
# Destroy
    def destroy(self):
        self.button.close()