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
                # print(f"Received data for LED Detection Actuator: {data}")
                led_state = data.get("presence", {}).get("value")
                # print(led_state)
                self.street_light.control_lights_server_led(led_state)
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling LED Detection Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

        @self.app.route('/lightActuator', methods=['POST'])
        def light_actuator():
            try:
                data = request.json.get("data")[0] 
                sensor = data.get("id")
                print(sensor)
                if sensor == 'urn:ngsi-ld:PirSensor:001':
                    print(f"Received data for Light Actuator: {data}")
                    led_state = data.get("presence", {}).get("value")
                    print(led_state)
                    self.street_light.control_lights_server_light_state(led_state)
                elif sensor == 'urn:ngsi-ld:PhotoresistorSensor:001':
                    # Received data for Photoresistor Sensor: {'id': 'urn:ngsi-ld:PhotoresistorSensor:001', 'type': 'PhotoresistorSensor', 'light': {'type': 'Property', 'value': 0.905882}}
                    print(f"Received data for ###Photoresistor### Sensor: {data}")
                    intesity= data.get("light", {}).get("value")
                    print(intesity)
                    print("dasdasdfasdfasdf")
                    # print(intesity)
                    # print("dasdasdfasdfasdf")
                    # self.street_light.control_lights_server_light(intesity);
                else:
                    print('Nothing')
                    
                # print(f"Received data for Light Actuator: {sensor}")
                            # print(f"Received data for Light Actuator: {data}")
                            # result = self.light_change(data.get("stateLight"))
                # led_state = data.get("presence", {}).get("value")
                # print(led_state)
                # # return jsonify(result), 201
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling Light Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500


        #  if (data.id === `urn:ngsi-ld:PhotoresistorSensor:${process.env.DEVICE_NUMBER || '002'}`) {
        #         console.log(data.light.value);
        #         if (data.light.value > intensityThreshold) {
        #             ctrl_lightActuator = 'ON';
        #             // console.log('Lus');
        #             if (state_lightAtuator === 'OFF') {
        #                 state_lightAtuator = 'ON';
        #                 // console.log('Encendido');
        #                 ActuatorsService.lightChange(state_lightAtuator);
        #                 SOCKET_IO.emit('update_lightActuator', state_lightAtuator);
        #             }
        #         } else if (data.light.value <= intensityThreshold){
        #             ctrl_lightActuator = 'OFF';
        #             // console.log('No hay gente');
        #             if (state_lightAtuator === 'ON') {
        #                 state_lightAtuator = 'OFF';
        #                 // console.log('Apagado'); 
        #                 ActuatorsService.lightChange(state_lightAtuator);
        #                 SOCKET_IO.emit('update_lightActuator', state_lightAtuator);
        #                 // console.log('Apagado');
        #             }
        #         }
        #     }
    
        #    // state_lightAtuator
        # if (data.id === `urn:ngsi-ld:PirSensor:${process.env.DEVICE_NUMBER || '002'}`) {
        #     if (data.presence.value === 'HIGH' && ctrl_lightActuator === 'ON' && state_lightAtuator === 'OFF') {
        #         state_lightAtuator = 'ON';
        #         ActuatorsService.lightChange(state_lightAtuator);
        #         SOCKET_IO.emit('update_lightActuator', state_lightAtuator);
        #         // console.log('Encendido');
        #     } else if (data.presence.value === 'LOW' && state_lightAtuator === 'ON') {
        #         state_lightAtuator = 'OFF';
        #         ActuatorsService.lightChange(state_lightAtuator);
        #         SOCKET_IO.emit('update_lightActuator', state_lightAtuator);
        #         // console.log('Apagado');
        #     } else if (ctrl_lightActuator === 'OFF'){
        #         state_lightAtuator = 'OFF';
        #         ActuatorsService.lightChange(state_lightAtuator);
        #         SOCKET_IO.emit('update_lightActuator', state_lightAtuator);
        #         // console.log('Apagado');
        #     }
        # }

# Camera
        @self.app.route('/cameraActuator', methods=['POST'])
        def camera_actuator():
            try:
                data = request.json.get("data")[0]
                print(f"Received data for Camera Actuator: {data}")
                presence = data.get("presence", {}).get("value")
#                 led_state = data.get("presence", {}).get("value")
                self.radar.control_camera_server(presence)
                return jsonify({"status": "success", "data": data}), 201
            except Exception as e:
                print(f"Error handling Camera Actuator: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
            
# Received data for Camera Actuator: {'id': 'urn:ngsi-ld:InfraredSensor:001', 'type': 'InfraredSensor', 'presence': {'type': 'Property', 'value': True}}


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