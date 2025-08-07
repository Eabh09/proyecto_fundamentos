from machine import UART, Pin
from time import sleep
import urandom

# Definir los pines para Serial2
RXD2 = 16
TXD2 = 17

# Configurar UART2 con los pines correspondientes
uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, rx=Pin(RXD2), tx=Pin(TXD2))

# Función para enviar comandos al módulo LoRa
def sendCmd(cmd):
    uart2.write(cmd + '\r\n')  # Enviar el comando seguido de un retorno de carro y nueva línea
    sleep(0.5)  # Esperar 500 ms para que el módulo reciba el comando
    while uart2.any():
        response = uart2.read().decode('utf-8')  # Leer la respuesta y decodificarla
        print(response, end='')  # Imprimir la respuesta en el monitor serial

# Configuración inicial
def setup():
    print("Configurando parámetros antena LoRa")
    sleep(1)
    sendCmd("AT+ADDRESS=1")  # Configurar el address a 1
    sleep(1)
    sendCmd("AT+NETWORKID=5")  # Configurar el Network ID a 5
    sleep(1)
    sendCmd("AT+BAND?")  # Leer la frecuencia configurada
    sleep(1)
    sendCmd("AT+PARAMETER?")  # Leer los parámetros configurados
    sleep(1)
    sendCmd("AT+MODE?")  # Leer el modo configurado
    sleep(1)

# Bucle principal
def loop():
    while True:
        # Generar los valores a transmitir
        value1 = urandom.randint(-100, 100)
        value2 = urandom.randint(0, 4000)
        value3 = urandom.randint(1, 9)

        # Construir el mensaje que se enviará en un solo string
        data = "{},{},{}".format(value1, value2, value3)
        datalen = str(len(data))  # Obtener el tamaño del mensaje

        print("Enviando: " + data)
        sendCmd("AT+SEND=2," + datalen + "," + data)  # Construir y enviar el comando AT al módulo LoRa

        sleep(5)  # Esperar 5 segundos antes de enviar el siguiente mensaje

# Llamar a las funciones de configuración y bucle principal
setup()
loop()
