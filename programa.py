import subprocess
import time

intervalo = 300 
#Esto lo que hace es que lo voy a ajecutar cada 300 segundos

while True:
    subprocess.call("python dispositivos_to_log.py", shell=True)
    time.sleep(intervalo)
