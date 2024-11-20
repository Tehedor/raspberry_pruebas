sudo apt update
sudo apt install python3 python3-pip
git clone https://github.com/Tehedor/raspberry_pruebas.git
cd raspberry_pruebas
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt



Para general requirements.txt con la libreria ADCDevices:
python3 generate_requirements.py