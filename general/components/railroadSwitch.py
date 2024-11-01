from gpiozero import Button, AngularServo

myCorrection = 0.0
maxPW = (2.5 + myCorrection) / 1000
minPW = (0.5 - myCorrection) / 1000

class RailroadSwitch:
    def __init__(self, pin_switch, pin_servo):
        self.switch = Button(pin_switch)  # define Button pin according to BCM Numbering
        self.servo = AngularServo(pin_servo, initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=minPW, max_pulse_width=maxPW)
        self.state = 0
        
    def control_switch(self):
        if self.switch.is_pressed:  # if switch is pressed
            if self.state == 0:
                self.state = 1
                print("State 1")
                self.control_servo(self.state)
        else:  # if switch is released
            if self.state == 1:
                self.state = 0
                print("State 0")
                self.control_servo(self.state)
        
    def control_servo(self, state):
        if state == 0:
            for angle in range(0, 91, 1):
                self.servo.angle = angle
        else:
            for angle in range(90, -1, -1):
                self.servo.angle = angle    
    ########################################################                
    ############## Broker                 
    ########################################################                
                
    def broker_control_switch(self):
        if self.switch.is_pressed:  # if switch is pressed
            if self.state == 0:
                self.state = 1
                print("State 1")
                self.send_request(self.state)
        else:  # if switch is released
            if self.state == 1:
                self.state = 0
                print("State 0")
                self.send_request(self.state)                
                
    def broker_control_servo(self, state):
        if state == 0:
            for angle in range(0, 91, 1):
                self.servo.angle = angle
        else:
            for angle in range(90, -1, -1):
                self.servo.angle = angle    
                
    ########################################################                
    ############## Request
    ########################################################   
    def send_request(self, state):
        url = f"http://{self.ip_address}/update_state"
        data = {'state': state}
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Request successful")
            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        
        
    def destroy(self):
        self.switch.close()
