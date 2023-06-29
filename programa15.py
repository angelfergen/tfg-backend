import subprocess
import time
import json
from datetime import datetime, date

while True:
    dia = {}
    for hora in range(0, 24): #Aqui se van a ejecutar desde las 00 hasta las 24 sin incluir
        print("HORA", hora)
        objects = []  # Lista para almacenar los objetos JSON de cada 15 minutos
        for num in range(1, 5): #se realizan las 4 iteracciones que necesito
            print("Ejecucion numero", num)
            subprocess.call("sudo python cuenta15.py", shell=True)
            # Ahora lo que voy a hacer será crear 1 fichero para cada intervalor de15 minutos
            with open('contador_dispositivos.json', 'r') as f:
                contenido = json.load(f)
            with open(f'parte{num}.json', 'w') as f:
                json.dump(contenido, f, indent=4)
        
            # Aqui lo que voy a hacer va a ser guardar las 4 partes de cada 15 minutos en uno entero y lo guardo en la lista cada uno
            with open(f'parte{num}.json', 'r') as f:
                objeto = json.load(f)
                objects.append(objeto)

        # Agregar la lista de objetos JSON al diccionario "dia" con la clave "hora"
        dia[str(hora)] = objects

        # Guardar los objetos JSON en el archivo "horaX.json"
        with open(f'hora{hora}.json', 'w') as f:
            json.dump(objects, f, indent=4)

        # Y ahora lo que hago es juntar todos los ficheros de las horas en uno diario
    with open("data/{}.log".format( date.today()), 'w') as f:
        json.dump(dia, f, indent=4)
