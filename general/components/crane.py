from gpiozero import DistanceSensor

# trigPin = 16
# echoPin = 26
# sensor = DistanceSensor(echo=echoPin, trigger=trigPin ,max_distance=3)

# print('Distance: ', sensor.distance * 100,'cm')

class Crane:
    def __init__(self, pin_ultrasound_trig ,pin_ultrasound_echo ):
        self.sensor = DistanceSensor(echo=pin_ultrasound_echo, trigger=pin_ultrasound_trig ,max_distance=3)
        self.last_distance = 0.0
        
    def detect_distance(self):
        current_distance = self.sensor.distance * 100
        if current_distance != self.last_distance:
            self.last_distance = current_distance
            return current_distance
        return None
    
    def print_distance(self):
        current_distance = self.sensor.distance * 100
        # if current_distance != self.last_distance:
        #     self.last_distance = current_distance
        #     print(f"Distance: {current_distance} cm")
        if abs(current_distance - self.last_distance) >= 0.5:
            self.last_distance = current_distance
            print(f"Distance: {current_distance} cm")
        
        
    def destroy(self):
        self.sensor.close()