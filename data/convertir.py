#Hola, lo que voy a tratar de hacer va a ser  transformar un fichero log 
#en un fichero json
#import json
# Abrir el archivo de registro en modo lectura
#with open("2023-04-18.log", "r") as file:

    # Leer las líneas del archivo
    #lines = file.readlines()

    # Recorrer todas las líneas y mostrarlas por pantalla
    #for line in lines:
        #print(json.dumps(line.strip()))

import json

# Ruta del archivo de log
log_file = "prueba.log"

# Abrir el archivo de log en modo lectura
with open(log_file, "r") as file:
    # Leer todas las líneas del archivo
    lines = file.readlines()

    # Crear una lista vacía para almacenar los registros en formato JSON
    json_logs = []

    # Recorrer todas las líneas del archivo de log
    for line in lines:
        # Dividir la línea en dos partes utilizando el primer ":" como separador
        parts = line.strip().split(":", 1)

        # Extraer el nombre del campo y el valor del campo de la primera parte
        field_name = parts[0].strip()
        field_value = parts[1].strip() if len(parts) > 1 else None

        # Si el nombre del campo es "Mac Address" o "Tiempo conectado", dividir el valor por ":" para obtener el valor correcto
        if field_name == "Mac Address":
            field_value = ":".join(field_value.split(":")[-6:]).upper() # Asegurarse de que la dirección MAC esté en mayúsculas
        elif field_name == "Tiempo conectado":
            field_value = ":".join(field_value.split(":")[-3:])

        # Crear un diccionario para almacenar los campos del registro
        log = {
            "timestamp": parts[0].strip(),
            "mac_address": None,
            "name_in_network": None,
            "given_name": None,
            "allowed_on_network": None,
            "connected_time": None
        }

        # Asignar el valor del campo al campo correspondiente en el diccionario
        if field_name == "Mac Address":
            log["mac_address"] = field_value
        elif field_name == "Name in network":
            log["name_in_network"] = field_value
        elif field_name == "Given name":
            log["given_name"] = field_value
        elif field_name == "Allowed on network":
            log["allowed_on_network"] = field_value
        elif field_name == "Tiempo conectado":
            log["connected_time"] = field_value
# Agregar el diccionario a la lista de registros en formato JSON
        json_logs.append(log)

# Guardar la lista de registros en formato JSON en un archivo llamado logs.json
with open("logs.json", "w") as file:
    json.dump(json_logs, file)
