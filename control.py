from machine import Pin
import time
from transmisor import setup, data_letras

# Configuración con pull-up
n1 = Pin(14, Pin.IN, Pin.PULL_UP)
n2 = Pin(12, Pin.IN, Pin.PULL_UP)
n3 = Pin(19, Pin.IN, Pin.PULL_UP)
n4 = Pin(21, Pin.IN, Pin.PULL_UP)
n5 = Pin(22, Pin.IN, Pin.PULL_UP)
n6 = Pin(23, Pin.IN, Pin.PULL_UP)

setup()

# Guardar estado anterior de cada botón
last_n1 = 1
last_n3 = 1
last_n4 = 1
last_n5 = 1
last_n6 = 1

while True:
    # Leer estados actuales
    current_n1 = n1.value()
    current_n3 = n3.value()
    current_n4 = n4.value()
    current_n5 = n5.value()
    current_n6 = n6.value()
    
    # Detectar flanco descendente - CÓDIGOS CON LETRAS
    if last_n1 == 1 and current_n1 == 0:
        print("derecha")
        data_letras("D")  # D = derecha
    
    if last_n3 == 1 and current_n3 == 0:
        print("abajo")
        data_letras("A")  # A = abajo
    
    if last_n4 == 1 and current_n4 == 0:
        print("izquierda")
        data_letras("I")  # I = izquierda
    
    if last_n5 == 1 and current_n5 == 0:
        print("arriba")
        data_letras("U")  # U = arriba (Up)
    
    if last_n6 == 1 and current_n6 == 0:
        print("apagar/encender")
        data_letras("E")  # E = encender/apagar
    
    # Actualizar estados anteriores
    last_n1 = current_n1
    last_n3 = current_n3
    last_n4 = current_n4
    last_n5 = current_n5
    last_n6 = current_n6
    
    time.sleep(0.05)  # Debounce de 50ms