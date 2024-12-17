from flask import Flask, request, jsonify
import os
# from . import server_requests


class IoTServer:
    # def __init__(self, host='0.0.0.0', port=5000):
    def __init__(self, host='0.0.0.0', port=80, street_light=None, toll=None, crane=None, weather_station=None, railroad_switch=None, radar=None, train=None):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()
        self.street_light = street_light
        self.toll = toll
        self.crane = crane
        self.weather_station = weather_station
        self.railroad_switch = railroad_switch
        self.radar = radar
        self.train = train


    def setup_routes(self):
# Street Light
        @self.app.route('/ledDetectionActuator', methods=['POST'])
        def led_detection_actuator():
            try:
                data = request.json.get("data")[0]
                print(f"Received data for LED Detection Actuator: {data}")
                self.street_light.control_lights_server_led(data.get("stateLed"))
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling LED Detection Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

        @self.app.route('/lightActuator', methods=['POST'])
        def light_actuator():
            try:
                data = request.json.get("data")[0]
                # print(f"Received data for Light Actuator: {data}")
                # result = self.light_change(data.get("stateLight"))
                self.street_light.control_lights_server_light(data.get("stateLight"))
                # return jsonify(result), 201
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling Light Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

# Camera
        @self.app.route('/cameraActuator', methods=['POST'])
        def camera_actuator():
            try:
                data = request.json.get("data")[0]
                # print(f"Received data for Camera Actuator: {data}")
                self.radar.control_camera_server(data.get("stateCamera"))
                # return jsonify(result), 201
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling Camera Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

# Servmotor
        @self.app.route('/servmotorActuator', methods=['POST'])
        def servmotor_actuator():
            try:
                data = request.json.get("data")[0]
                print(f"Received data for Servomotor Actuator: {data}")
                # result = self.servmotor_change(data.get("stateMotor"))
                # return jsonify(result), 201
                state_value = data.get("state", {}).get("value")
                print(state_value)
                self.railroad_switch.control_servo_server(state_value)
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling Servomotor Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

# Train 
        @self.app.route('/engineDCActuator', methods=['POST'])
        def engine_dc_actuator():
            print('Engine DC Actuator, no configurado')
            # try:
            #     data = request.json.get("data")[0]
            #     print(f"Received data for Engine DC Actuator: {data}")
            #     # result = self.engine_dc_change(data.get("velocityEngine"))
            #     # return jsonify(result), 201
            #     return jsonify({"status": "success", "data": data}), 201    
            # except Exception as e:
            #     print(f"Error handling Engine DC Actuator: {e}")
            #     return jsonify({"status": "error", "message": str(e)}), 500


    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':
    server = IoTServer()
    print('Server is starting...')
    server.run()