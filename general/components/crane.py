from gpiozero import DistanceSensor
# from ..server import server_requests
from server import server_requests

class Crane:
    def __init__(self, pin_ultrasound_trig ,pin_ultrasound_echo ):
        self.sensor = DistanceSensor(echo=pin_ultrasound_echo, trigger=pin_ultrasound_trig ,max_distance=3)
        self.last_distance = 0.0
        
        
# Serverless mode
    def detect_distance(self):
        current_distance = self.sensor.distance * 100
        # if current_distance != self.last_distance:
        if abs(current_distance - self.last_distance) >= 0.5:
            self.last_distance = current_distance
            return current_distance
        return None
    
    def print_distance(self):
        current_distance = self.sensor.distance * 100
        # if current_distance != self.last_distance:
        if abs(current_distance - self.last_distance) >= 0.5:
            self.last_distance = current_distance
            print(f"Distance: {current_distance} cm")

# Server mode
    def detect_distance_server(self):
        current_distance = self.sensor.distance * 100  
        if abs(current_distance - self.last_distance) >= 0.5:
            self.last_distance = current_distance
            print(f"Distance: {current_distance} cm")
            server_requests.ultrasound_sensor_change(current_distance)        

# Destroy  
    def destroy(self):
        self.sensor.close()