'''
    PYTHON-NETWORK-SCANNER
    Copyright (C) 2021  devmarcstorm

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
import subprocess
from getmac import get_mac_address
from prettytable import PrettyTable

from datetime import date

from device import Device
from network import Network
from vendedor import Vendedor
#from json_to_log4 import procesar_logs

import json
import os
import sys
import codecs
import subprocess

from datetime import datetime

from fastapi import FastAPI, Form, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from typing import List

#from flask import Flask, jsonify

#app = Flask(__name__)

@app.get('/')
def index():
  return "Hola esta es mi API <3"

@app.get('/meses/{mes}')
def leer_logs_mes(mes):
   # print("HOLAAAA")
    ubicacion_actual = os.getcwd()
   # print(ubicacion_actual)
    carpeta_logs = os.path.join(ubicacion_actual, 'data')
    print(carpeta_logs)
    archivos_logs = os.listdir(carpeta_logs)
   # print("Hola esto son los logs")
   # print(archivos_logs)
    logs_to_array = []
    for archivo in archivos_logs:
        #print(archivo)
        if not archivo.endswith('.log'):
            continue
        try:
            fecha_archivo = datetime.strptime(archivo[:10], '%Y-%m-%d')
            #print("Hola aqui tienes las fechas del archivo que son logs")
            #print(fecha_archivo)
            #print(fecha_archivo.month)
            #print(mes)
            #logaritmos.push(fecha_archivo
            #print(f"El archivo {archivo} corresponde al mes {fecha_archivo.month}.")

        except ValueError:
            continue
        try:
            if fecha_archivo.month == int(mes):
                with open(os.path.join(carpeta_logs, archivo), 'r') as f:
                    contenido_archivo = f.read()
                    #print("HOLAAAA")
                    #print(contenido_archivo)
                    contenido_modificado = "[{}]".format(",".join(contenido_archivo.splitlines()))
                    #logaritmos = json.loads(contenido_archivo.strip())
                    #print(json.loads(contenido_modificado))
                    #logaritmos.append(log_json)
                    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    #print(json.loads(logaritmos.replace('\n', ''))
                    logs_to_array.extend(json.loads(contenido_modificado))
                    #print(logs_to_array)
                    #logs_objects = procesar_logs(logaritmos)
        except Exception as e:
            print(f"Error al procesar el archivo{archivo}:{e}")
    #print("HOLA AQUI ES EL FINAL Y EL RESULTADO")
    #print(logs_to_array)
    #logs_objects = procesar_logs(logaritmos)
    #print(logs_objects)
    return logs_to_array


#-----------------El error de CORS-----------------------------------------
@app.middleware("http") 
async def add_cors_headers(request, call_next): 
    response = await call_next(request) 
    response.headers["Access-Control-Allow-Origin"] = "*" 
    return response
#----------------------------------------------------------------
@app.get('/devices')
def create_device_list(devices, data):
    ''' Return a dictonary like {'known': [], 'unknown': []}

    Creates 2 lists from devices (class Device) and makes them available in a dictionary
       - 'known': list of known devices (mac address included in the data/device.json)
       - 'unknown': list of unknown devices (not included)
    '''
    known_devices = []
    unknown_devices = []
   # print(devices)
    for host, info in devices:
     
       # print("------------Info MAC:",info['mac'])
       #print("------------Info host:",host)
       # print("------------Info Hostname:",info['hostnames'][0]['name'])
        #print("------------Info Data:",data)

        device = Device(info['mac'], host, info['hostnames'][0]['name'], data) 
       # print("-----------ESTO ES DEVICE:",device)
        
        if device.name:
           # print("EL JSON NENU")
           # print(jsonify(device))
            known_devices.append(device)
        else:
            unknown_devices.append(device)
    #print("CONOCIDOSSSSSS",known_devices)
    #print("Desconocidosssssssss",unknown_devices)
    #print("HOLAAAAAAA ESTAS SON LAS LISTAS")
    #print('known: ', known_devices, 'unknown: ', unknown_devices)
    #print(known_devices[1].to_string()) print( jsonify('known: ', 
    #known_devices, 'unknown: ', unknown_devices)) conocidos = jsonify 
    #(known_devices) desconocidos = jsonify(unknown_devices) response = 
    #jsonify({'known': known_devices, 'unknown': unknown_devices}) 
    #print(conocidos)
    #print(devices)
    #----------------------- NOTA, LO RELACIONADO CON JSONIFY NO FUNCIONA--------------------
    return {'known': known_devices, 'unknown': unknown_devices}
    #return response
#@app.get("/devices")    

#@app.get("/ari")
#def create_ari() -> List[str]:
#    network = Network()
#    devices = []
#    try:
#        devices = network.get_devices()
#    except KeyboardInterrupt:
#        print("You stopped scanning. Scanning may take a while. If it takes too long, you may need to increase the timeout value.")
#        sys.exit()
#    for host, info in devices:
#        info['mac'] = get_mac_address(ip=host)
#    print("ARRRIIIIIIIIIIII")
#    print(devices)
#    return devices

import re
@app.get("/ari")
def create_ari() -> List[dict]:
    network = Network()
    devices = []
    try:
        devices = network.get_devices()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Aquí puede registrar el error o devolver una respuesta de error apropiada
        return {"error": "Ocurrió un error al obtener los dispositivos."}
    puertos = []
    for device in devices:
        device['mac'] = get_mac_address(ip=device['addresses']['ipv4'])
        print(device['mac'])
        #Esto lo hago ya que me está cogiendo la dirección mac de la raspi como none
	#Entonces lo que hago es ponerle a piñon la dir mac por ethernet
        if device['addresses']['ipv4'] == "192.168.1.27":
            device['mac'] = "b8:27:eb:98:a0:60"
         
        #print("--------------VENDEDOR------")
        #print("oui",device['mac'])
        output= subprocess.check_output(["oui", device['mac']]).decode('utf-8').strip()
        #-----------------
        output = output.replace('，', ',')  # Reemplazar el carácter problemático
        #Esa linea la he tenido que poner por este vendedor, que me estaba pillando una coma que no es la normal
        #SHENZHEN BILIAN ELECTRONIC CO.，LTD
	#NO.268? Fuqian Rd, Jutang community, Guanlan Town, Longhua New district
	#shenzhen guangdong 518000
	#China
        #--------------------
        vendedor = output.splitlines()[0]
        #print(vendedor)
        #subprocess.call(["oui",device['mac']], shell=True)
        #print(v.get_vendedor(device['mac']))
        #print("----------------------------")
        device['vendor'] = vendedor

#    print("ARRRIIIIIIIIIIII")
#        print(devices)
#    devices_json = jsonpickle.encode(devices)
#    return devices_json
#    return jsonpickle.encode(devices)
#    device = [{'hostnames': [{'name': 'liveboxfibra', 'type': 'PTR'}], 'addresses': {'ipv4': '192.168.1.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'syn-ack'}}]
#    device = [{"py/object": "nmap.nmap.PortScannerHostDict", "hostnames": [{"name": "liveboxfibra", "type": "PTR"}], "state": "up", "reason": "syn-ack", "__dict__": {}}]
# Ejecutar el comando nmap para obtener la información de los puertos abiertos
#        ip_address = device['addresses']['ipv4']
#        output = subprocess.check_output(["sudo", "nmap", "-O", "-v", ip_address])
#        pattern = re.compile(r"([0-9]+)/tcp\s+(open|closed|filtered)\s+(\w+)")
#        matches = pattern.findall(str(output))

#        all_ports = []
#        for match in matches:
#            port_info = {
#                "PORT": match[0],
#                "STATE": match[1],
#                "SERVICE": match[2]
#            }
#            all_ports.append(port_info)
#        device["ports"] = all_ports
    print(devices)
    return devices

@app.get("/puertos/{dir_ip}")
def get_puertos (dir_ip):
    output = subprocess.check_output(["sudo", "nmap", "-O", "-v", dir_ip])
    pattern = re.compile(r"([0-9]+)/tcp\s+(open|closed|filtered)\s+(\w+)")
    matches = pattern.findall(str(output))

    puertos = []
    for match in matches:
        port_info = {
            "PORT": match[0],
            "STATE": match[1],
            "SERVICE": match[2]
        }
        puertos.append(port_info)
    print(puertos)
    return  puertos

@app.post("/dispositivos")
def create_data(devices,json_devices):
    return create_device_list(devices, json_devices)

@app.get("/conocidos")
def lista_conocidos () -> List[dict]:
#    print(/devices.json)
#    return "/devices.json"
    with open("data/devices.json") as disposit:
      conocidos =  json.load(disposit)
    print("HOLAAAAA CONOCIDOS")
    print (conocidos)
    return [conocidos]


@app.post("/anade_conocidos")
async def anade_conocidos(mac_address: str = Form(...),
                           device_type: str = Form(...),
                           owner: str = Form(...),
                           location: str = Form(...),
                           allowed: str = Form(...))-> dict :

    filename = "/home/pi/tfg/opcion3/python-network-scanner/data/devices.json"
    data = {}

    data[mac_address] = {"type": device_type,
                         "owner": owner,
                         "location": location,
                         "allowed": allowed}
    print("HOOOOLAAAAA EL DATA",data[mac_address])

    with open(filename, "r+") as f:
        try:
            existing_data = json.load(f)
        except json.decoder.JSONDecodeError: 
            existing_data = {}

        existing_data.update(data)

        f.seek(0)
        json.dump(existing_data, f, indent=4,ensure_ascii=False)

    print(f"Los datos han sido agregados exitosamente al archivo {filename}.")

    print("HOLAAAAA DATAA")
    print (data)
    return data

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#----------------NO ME HACE LA PETICION PUT EL HTML NO SE PQ-------------
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#@app.put("/update_conocidos")
#@app.route('/update_conocidos', methods=['PUT'])
#async def anade_conocidos(mac_address: str = Form(...),
#                           device_type: str = Form(...),
#                           owner: str = Form(...),
#                           location: str = Form(...),
#                           allowed: str = Form(...))  -> dict :

#    print("Holaaaa")

#    filename = "/home/pi/tfg/opcion3/python-network-scanner/data/devices.json"

#    with open(filename, "r+") as f:
#        try:
#            existing_data = json.load(f)
#        except json.decoder.JSONDecodeError:
#            existing_data = {}

#        if mac_address in existing_data:
#            devices[mac_address]["type"] = device_type
#            devices[mac_address]["owner"] = owner
#            devices[mac_address]["location"] = location
#            devices[mac_address]["allowed"] = allowed
            
#            with open(filename, "w") as f:
#                json.dump(existing_data, f, indent=4,ensure_ascii=False)

#            return existing_data[mac_address]
#        else:
#            return  {"error": "El dispositivo no se encuentra en la lista."}
#    return "hoooolaaaa"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.put("/update_conocidos")
async def update_conocidos(
    mac_address: str = Form(...),
    device_type: str = Form(...),
    owner: str = Form(...),
    location: str = Form(...),
    allowed: str = Form(...)
) -> dict:
    print(f"Actualizando dispositivo con MAC {mac_address}")
    print(f"Actualizando dispositivo con MAC {mac_address}")

    filename = "data/devices.json"
   #Voy a seguir la misma logica que el metodo para añadir dispositivos,
   #escribo los datos en el formulario que quiero actualizar, los cambio y los guardo con json.dump
 
   # Lee el contenido del archivo JSON y conviértelo en un diccionario
    with open(filename, "r") as f:
        data = json.load(f)

    # Actualiza los valores del objeto deseado
    if mac_address in data:
        data[mac_address]["type"] = device_type
        data[mac_address]["owner"] = owner
        data[mac_address]["location"] = location
        data[mac_address]["allowed"] = allowed

        # Escribe los cambios de vuelta al archivo
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return {"message": "Datos actualizados con éxito."}
    else:
        return {"message": "El dispositivo no se encuentra en la lista."}


@app.post("/eliminar-dispositivo/{mac_address_bytes}")
#OJO ME ESTA DANDO ERROR LA DIRECCION MAC PQ INTERPRETA LOS : COMO UN SEPARADOR PARA LA DIRECCION
#Asi que una opcion para resolver este problema es pasar la informacion en la url en bytes en vez de strings
#asi que voy a tener que descodificar la direccion mac de bytes a string para poder borrarla
async def eliminar_dispositivo(mac_address_bytes: str):
    filename = "data/devices.json"
    print("Hola esta es la mac address")
    print(mac_address_bytes)
#    return "hola"
    with open(filename, "r+") as f: #No se si es con un r+ o sin el +
        try:
            existing_data = json.load(f)
        except json.decoder.JSONDecodeError:
            existing_data = {}
        print(existing_data)
#    return mac_address_bytes

    # Decodificar la dirección MAC de la URL de hexadecimal a su formato origin >con dos puntos
    #mac_address = ":".join([codecs.decode(mac_address_bytes[i:i+2].upper(), "hex").decode() for i in range(0, len(mac_address_bytes), 2)])
        print("HOOOLAAAAA, LA NUEVA MAC")
        mac_address = ':'.join(mac_address_bytes[i:i+2] for i in range(0, len(mac_address_bytes), 2))
        print(mac_address)
    
    #mac_address = ":".join([bytes.fromhex(mac_address_bytes[i:i+2].decode()).hex() for i in range(0, len(mac_address_bytes), 2)])
    #mac_address = ":".join([mac_address_bytes[i:i+2].hex() for i in range(0, len(mac_address_bytes), 2)])
    
        if mac_address in existing_data:
#             print("Hola está aquí")
                del existing_data[mac_address]
                print(existing_data)

                f.seek(0)
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
                f.truncate()
                print(existing_data)
                return {"mensaje": f"El dispositivo con direccion MAC {mac_address} ha sido eliminado."}
        else:
                return {"mensaje": f"No se ha encontrado un dispositivo con direccion MAc {mac_address}."}


if __name__ == '__main__':
    
    dataPath = 'data'
    try:
        with open("{}/devices.json".format(dataPath), "r") as readFile:
                json_devices = json.load(readFile)
    except FileNotFoundError:
                json_devices = {}
                print('''No valid "data/devices.json" found. Please create one with the following format:
{
    "00:00:00:00:00:00":
    {
      "type": "Device",
      "owner": "John Appleseed",
      "location": null,
      "allowed": true
    }
}
            ''')
    network = Network()
    devices = []
    try:
        devices = network.get_devices()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Aquí puede registrar el error o devolver una respuesta de error apropi>
        #return {"error": "Ocurrió un error al obtener los dispositivos."}
    puertos = []
    for device in devices:
        device['mac'] = get_mac_address(ip=device['addresses']['ipv4'])
        print(device['mac'])

        #YA HE CONSEGUIDO QUE ME GENERE UN LOG DE ESTO
        #jamones = Device.to_json(device['mac'])
        #print(jamones)
    print(devices)

    devices=create_ari()
    print(devices)
#    network = Network()
#    try:
#        devices = network.get_devices()
#    except KeyboardInterrupt:
#        print('You stopped scanning. Scanning may take a while. If it takes too long, there may be a problem with the connection. Did you specify the correct network?')
#        sys.exit()

    #for host, info in devices:
    #    info['mac'] = get_mac_address(ip=host)
    
   
    #data = create_data(devices,json_devices)
    #data = create_device_list(devices, json_devices)
    #log_text = ''

    #table = PrettyTable()
    #table.field_names = ["MAC ADDRESS", "IP", "NAME IN NETWORK","TIEMPO","NAME", 'LOCATION', 'ALLOWED']
    #for device in data['known']:
    #    table.add_row(device.to_list())
    #    log_text += '{}\n'.format(device.to_string())
    
    #print('Known Devices\n{}'.format(table))

    #table = PrettyTable()
    #table.field_names = ["MAC ADDRESS", "IP", "NAME IN NETWORK","TIEMPO"]
    #for device in data['unknown']:
       # print(device) No me saca el tipo de disposito
       #Me saca algo parecido <device.Device object at 0x7685af10>
       # print(device.to_list())
    #    table.add_row(device.to_list()[:4])
    #    log_text += '{}\n'.format(device.to_string())
    
    #print('Unknown Devices\n{}'.format(table))
    #app.run()

#       NO SE PQ PERO ESTAS LINEAS ME DAN UN ERROR CUANDO EJECUTO EL SERVIDOR API
#dataPath = "/data"
#if not os.path.isdir(dataPath):
#    os.mkdir(dataPath)

#with open("{}/{}.log".format(dataPath, date.today()), "a") as appendFile:
#    appendFile.write(log_text)
#    print('You can find a log file with all devices in "data/{}.log"'.format(date.today()))
