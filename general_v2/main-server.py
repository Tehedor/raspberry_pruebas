import time
import signal
from flask import Flask, jsonify
from dotenv import load_dotenv
import subprocess

mode = "python3"            # sudo python3 script.py 
# mode =  "gunicorn"          # sudo gunicorn -b 0.0.0.0:5000 main_server:app 

# Inicialización de Flask y carga de variables de entorno
app = Flask(__name__)
load_dotenv()

state = "stopped"
process = None

def cleanup(signum, frame):
    global process
    if process:
        process.terminate()
        process.wait()
    print("Cleanup complete. Exiting...")
    exit(0)

# Registrar la función de limpieza para la señal SIGINT
signal.signal(signal.SIGINT, cleanup)

@app.route('/start', methods=['POST'])
def start_components():
    global state, process, mode

    if state != 'starting':
        state = "starting"

        process = subprocess.Popen(["sudo", "python3", "script.py", mode], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            response = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:3001/health"], capture_output=True, text=True)
            if response.stdout.strip() == "200":
                break
            state = "waiting to IOT server"
            time.sleep(1)

    state = "running"
    print("Components started.")
    return jsonify({"status": "success", "message": "Components started"}), 200


@app.route('/stop', methods=['POST'])
def stop_components():
    global state, process

    if process:
        process.terminate()  # Intenta detener el proceso
        process.wait()  # Espera a que el proceso termine
        process = None  # Limpia la variable

    state = "stopped"
    print("Components stopped.")
    return jsonify({"status": "success", "message": "Components stopped"}), 200


@app.route('/status', methods=['GET'])
def get_status():
    global state
    return jsonify({"status": "success", "state": state}), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)