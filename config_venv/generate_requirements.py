import subprocess

def create_requirements():
    # Crear el archivo requirements.txt usando pip freeze
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    requirements = result.stdout

    # Escribir el contenido en el archivo requirements.txt
    with open('requirements.txt', 'w') as file:
        file.write(requirements)

    # Leer el contenido del archivo requirements.txt
    with open('requirements.txt', 'r') as file:
        lines = file.readlines()

    # Modificar la línea que contiene ADCDevice
    with open('requirements.txt', 'w') as file:
        for line in lines:
            if 'ADCDevice' in line:
                file.write('./packages/ADCDevice-1.0.3.tar.gz\n')
            else:
                file.write(line)

if __name__ == "__main__":
    create_requirements()