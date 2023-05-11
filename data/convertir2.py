import json
# Abrir el archivo de registro en modo lectura
#with open("prueba.log", "r") as file:

    # Leer las líneas del archivo
#    lines = file.readlines()

    #Recorrer todas las líneas y mostrarlas por pantalla
#    for line in lines:
#        print(json.dumps(line.strip().split(":",1)))
#import json

# Abrir el archivo de registro en modo lectura
with open("2023-04-18.log", "r") as file:
    # Leer las líneas del archivo
    lines = file.readlines()
    json_logs = []

    # Crear un diccionario vacío que contendrá los datos
    data = {}

    # Recorrer todas las líneas y guardar los valores en el diccionario
    for line in lines:
        if line.startswith("Log:"):
          if data:
            json_logs.append(json.dumps(data))
            data = {}
        key, value = line.strip().split(":", 1)
        data[key] = value.strip()
#        json_log = { key: value.strip() }
#        json_logs.append(json_log)
    # Convertir el diccionario en formato JSON
    json_data = json.dumps(data)
    json_logs.append(json_data)
    # Imprimir el resultado
    print(json_logs)
#    print(json.dumps(json_logs))
