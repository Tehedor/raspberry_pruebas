from flask import Flask, request, jsonify

class TestServer:
    def __init__(self, host='0.0.0.0', port=80):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()

    def setup_routes(self):
        # Street Light
        @self.app.route('/ledDetectionActuator', methods=['POST'])
        def led_detection_actuator():
            data = request.json
            print(f"Route: /ledDetectionActuator, Data: {data}")
            return jsonify({"status": "received", "route": "/ledDetectionActuator", "data": data}), 200

        @self.app.route('/lightActuator', methods=['POST'])
        def light_actuator():
            data = request.json
            print(f"Route: /lightActuator, Data: {data}")
            return jsonify({"status": "received", "route": "/lightActuator", "data": data}), 200

        # Camera
        @self.app.route('/cameraActuator', methods=['POST'])
        def camera_actuator():
            data = request.json
            print(f"Route: /cameraActuator, Data: {data}")
            return jsonify({"status": "received", "route": "/cameraActuator", "data": data}), 200

        # Servomotor
        @self.app.route('/servmotorActuator', methods=['POST'])
        def servmotor_actuator():
            data = request.json
            print(f"Route: /servmotorActuator, Data: {data}")
            return jsonify({"status": "received", "route": "/servmotorActuator", "data": data}), 200

        # Train
        @self.app.route('/engineDCActuator', methods=['POST'])
        def engine_dc_actuator():
            data = request.json
            print(f"Route: /engineDCActuator, Data: {data}")
            return jsonify({"status": "received", "route": "/engineDCActuator", "data": data}), 200

    def run(self):
        print(f"Starting test server on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':
    server = TestServer()
    server.run()
