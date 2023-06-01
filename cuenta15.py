from getmac import get_mac_address
from prettytable import PrettyTable
from datetime import date
from device import Device
from network import Network
import json
import time

def obtener_dispositivos_conectados(network):
    try:
        devices = network.get_devices()
    except Exception as e:
        print(f"An error occurred: {e}")

    for device in devices:
        device['mac'] = get_mac_address(ip=device['addresses']['ipv4'])
    print(devices)
    return devices

def actualizar_contador_dispositivos(dispositivos, contador_dispositivos):
    for dispositivo in dispositivos:
        mac = dispositivo['mac']
        contador_actual = contador_dispositivos.get(mac, 0)
        contador_dispositivos[mac] = contador_actual + 1

    with open('contador_dispositivos.json', 'w') as f:
        json.dump(contador_dispositivos, f, indent=4)

if __name__ == "__main__":
    contador_dispositivos = {}
    network = Network()

    intervalo = 30 # Intervalo de 60 segundos para que haya ejecuciones cada minuto
    num_ejecuciones = 15 #aqui se van a realizar 15 iteracciones, por eso 15

    for i in range(1, num_ejecuciones + 1):
        #print("Ejecucion numero",i)
        dispositivos = obtener_dispositivos_conectados(network)
        actualizar_contador_dispositivos(dispositivos, contador_dispositivos)
        time.sleep(intervalo)
