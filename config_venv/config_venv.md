# Confiugración de venv

## Configuar entorno virutal de python

```bash
sudo apt update
sudo apt install python3 python3-pip
git clone https://github.com/Tehedor/raspberry_pruebas.git
```

```bash
cd raspberry_pruebas
python3 -m venv .venv
source .venv/bin/activate
```

```bash
cd config_venv
pip install -r requirements.txt
```

## Crear requirementes con nuevas liberias

- Para general requirements.txt con la libreria ADCDevices:

``` bash
python3 generate_requirements.py
```
