from flask import Flask, request, jsonify
import requests
import os

class IoTServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/ledDetectionActuator', methods=['POST'])
        def led_detection_actuator():
            data = request.json.get("data")[0]
            print(f"Received data for LED Detection Actuator: {data}")
            # result = self.led_detection_change(data.get("stateLed"))
            # return jsonify(result), 201
            return jsonify({"status": "success", "data": data}), 201

        @self.app.route('/lightActuator', methods=['POST'])
        def light_actuator():
            data = request.json.get("data")[0]
            print(f"Received data for Light Actuator: {data}")
            # result = self.light_change(data.get("stateLight"))
            # return jsonify(result), 201
            return jsonify({"status": "success", "data": data}), 201

        @self.app.route('/engineDCActuator', methods=['POST'])
        def engine_dc_actuator():
            data = request.json.get("data")[0]
            print(f"Received data for Engine DC Actuator: {data}")
            # result = self.engine_dc_change(data.get("velocityEngine"))
            # return jsonify(result), 201
            return jsonify({"status": "success", "data": data}), 201    

        @self.app.route('/servmotorActuator', methods=['POST'])
        def servmotor_actuator():
            data = request.json.get("data")[0]
            print(f"Received data for Servomotor Actuator: {data}")
            # result = self.servmotor_change(data.get("stateMotor"))
            # return jsonify(result), 201
            return jsonify({"status": "success", "data": data}), 201

        @self.app.route('/cameraActuator', methods=['POST'])
        def camera_actuator():
            data = request.json.get("data")[0]
            print(f"Received data for Camera Actuator: {data}")
            # result = self.camera_change(data.get("stateCamera"))
            # return jsonify(result), 201
            return jsonify({"status": "success", "data": data}), 201

    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':
    server = IoTServer()
    print('Server is starting...')
    server.run()