#pin34
#pin35
#pin36
#pin39
import asyncio
from machine import Pin
from control_de_motores import abrir_puertas, cerrar_puertas, apagar_motor, encender_motor
from sensor import load_data
from biometrico import auto_detect_fingerprint
from avdc import Adc

in1 = Pin(36, Pin.IN)
in2 = Pin(35, Pin.IN)
finger = auto_detect_fingerprint()

async def tarea_sensores():
    """Tarea para leer sensores"""
    while True:
        load_data()
        await asyncio.sleep(1) 

async def tarea_puertas():
    """Tarea para controlar puertas"""
    while True:
        if in1.on():
            abrir_puertas()
        else:
            cerrar_puertas()
        await asyncio.sleep(0.1) 

async def tarea_motor():
    """Tarea para controlar motor"""
    while True:
        if in2.on():
            encender_motor()
        else:
            apagar_motor()
        await asyncio.sleep(0.1)
async def tarea_motor():
    """Tarea para cambio de tension del panel"""
    while True:
        Adc()    

async def tarea_biometrico():
    """Tarea para detector biométrico"""
    while True:
        finger_id = finger.get_fingerprint()
        if finger_id== True:
            print(f"Bienvenido usuario {finger_id}")
            encender_motor()
        else:
            contador=+1
            if contador>=4:
                print("alarma") 

        await asyncio.sleep(0.2)  # Cada 200ms

async def main():
    
    await asyncio.gather(
        tarea_sensores(),
        tarea_puertas(),
        tarea_motor(),
        tarea_biometrico()
    )

asyncio.run(main())



