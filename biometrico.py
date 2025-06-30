"""
ZMFO40 con librería Adafruit Fingerprint para MicroPython
Adaptación para usar con sensor ZMFO40 v1.8
"""

import machine
import time

class AdafruitFingerprint:
    """Librería Adafruit adaptada para ZMFO40 en MicroPython"""
    
    # Constantes del protocolo
    FINGERPRINT_OK = 0x00
    FINGERPRINT_PACKETRECIEVEERR = 0x01
    FINGERPRINT_NOFINGER = 0x02
    FINGERPRINT_IMAGEFAIL = 0x03
    FINGERPRINT_IMAGEMESS = 0x06
    FINGERPRINT_FEATUREFAIL = 0x07
    FINGERPRINT_NOMATCH = 0x08
    FINGERPRINT_NOTFOUND = 0x09
    FINGERPRINT_ENROLLMISMATCH = 0x0A
    FINGERPRINT_BADLOCATION = 0x0B
    FINGERPRINT_DBRANGEFAIL = 0x0C
    FINGERPRINT_UPLOADFEATUREFAIL = 0x0D
    FINGERPRINT_PACKETRESPONSEFAIL = 0x0E
    FINGERPRINT_UPLOADFAIL = 0x0F
    FINGERPRINT_DELETEFAIL = 0x10
    FINGERPRINT_DBCLEARFAIL = 0x11
    FINGERPRINT_PASSFAIL = 0x13
    FINGERPRINT_INVALIDIMAGE = 0x15
    FINGERPRINT_FLASHERR = 0x18

    FINGERPRINT_STARTCODE = 0xEF01
    FINGERPRINT_COMMANDPACKET = 0x1
    FINGERPRINT_DATAPACKET = 0x2
    FINGERPRINT_ACKPACKET = 0x7
    FINGERPRINT_ENDDATAPACKET = 0x8

    FINGERPRINT_VERIFYPASSWORD = 0x13
    FINGERPRINT_GETIMAGE = 0x01
    FINGERPRINT_IMAGE2TZ = 0x02
    FINGERPRINT_REGMODEL = 0x05
    FINGERPRINT_STORE = 0x06
    FINGERPRINT_SEARCH = 0x04
    FINGERPRINT_DELETE = 0x0C
    FINGERPRINT_EMPTY = 0x0D
    FINGERPRINT_TEMPLATECOUNT = 0x1D

    def __init__(self, uart_num=2, baudrate=57600, tx_pin=17, rx_pin=16, password=0x0, address=0xFFFFFFFF):
        """
        Inicializar sensor ZMFO40 con protocolo Adafruit
        
        Args:
            uart_num: Número UART
            baudrate: Velocidad (57600 típico para ZMFO40)
            tx_pin: Pin TX del ESP32
            rx_pin: Pin RX del ESP32
            password: Contraseña del sensor
            address: Dirección del sensor
        """
        self.address = address
        self.password = password
        
        # Configurar UART
        self.uart = machine.UART(uart_num, baudrate=baudrate, tx=tx_pin, rx=rx_pin, timeout=1000)
        print(f"📡 UART configurado: TX={tx_pin}, RX={rx_pin}, Baudrate={baudrate}")
        
        # Verificar conexión
        if self.verifyPassword():
            print("✅ ZMFO40 conectado con protocolo Adafruit")
        else:
            raise Exception("❌ No se pudo conectar al ZMFO40")

    def _write_packet(self, packet_type, data):
        """Escribir paquete al sensor"""
        # Limpiar buffer
        while self.uart.any():
            self.uart.read()
        
        packet = []
        
        # Start code
        packet.extend([0xEF, 0x01])
        
        # Address (4 bytes)
        packet.extend([
            (self.address >> 24) & 0xFF,
            (self.address >> 16) & 0xFF,
            (self.address >> 8) & 0xFF,
            self.address & 0xFF
        ])
        
        # Packet type
        packet.append(packet_type)
        
        # Length
        length = len(data) + 2
        packet.extend([(length >> 8) & 0xFF, length & 0xFF])
        
        # Data
        packet.extend(data)
        
        # Checksum
        checksum = packet_type + ((length >> 8) & 0xFF) + (length & 0xFF)
        for byte in data:
            checksum += byte
        packet.extend([(checksum >> 8) & 0xFF, checksum & 0xFF])
        
        # Enviar
        self.uart.write(bytes(packet))

    def _read_packet(self, timeout=3):
        """Leer paquete del sensor"""
        packet = []
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            if self.uart.any():
                data = self.uart.read()
                packet.extend(data)
                
                # Verificar si tenemos paquete completo
                if len(packet) >= 12:
                    # Verificar start code
                    if packet[0] == 0xEF and packet[1] == 0x01:
                        length = (packet[7] << 8) | packet[8]
                        if len(packet) >= (9 + length):
                            return packet[6], packet[9:9+length-2]
            time.sleep(0.01)
        
        raise Exception("Timeout leyendo respuesta")

    def verifyPassword(self):
        """Verificar contraseña del sensor"""
        data = [
            self.FINGERPRINT_VERIFYPASSWORD,
            (self.password >> 24) & 0xFF,
            (self.password >> 16) & 0xFF,
            (self.password >> 8) & 0xFF,
            self.password & 0xFF
        ]

        
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        try:
            packet_type, response = self._read_packet()
            return response[0] == self.FINGERPRINT_OK
        except:
            return False

    def getImage(self):
        """Capturar imagen de huella"""
        data = [self.FINGERPRINT_GETIMAGE]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    def image2Tz(self, slot=1):
        """Convertir imagen a template"""
        data = [self.FINGERPRINT_IMAGE2TZ, slot]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    def fingerSearch(self, slot=1):
        """Buscar huella en base de datos"""
        # Usar toda la base de datos (0-162)
        data = [self.FINGERPRINT_SEARCH, slot, 0x00, 0x00, 0x00, 0xA3]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        
        if response[0] == self.FINGERPRINT_OK:
            finger_id = (response[1] << 8) | response[2]
            confidence = (response[3] << 8) | response[4]
            return response[0], finger_id, confidence
        else:
            return response[0], None, None

    def createModel(self):
        """Crear modelo desde dos templates"""
        data = [self.FINGERPRINT_REGMODEL]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    def storeModel(self, location, slot=1):
        """Guardar modelo en ubicación específica"""
        data = [self.FINGERPRINT_STORE, slot, (location >> 8) & 0xFF, location & 0xFF]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    def deleteModel(self, location, count=1):
        """Borrar modelo(s)"""
        data = [
            self.FINGERPRINT_DELETE,
            (location >> 8) & 0xFF, location & 0xFF,
            (count >> 8) & 0xFF, count & 0xFF
        ]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    def emptyDatabase(self):
        """Vaciar toda la base de datos"""
        data = [self.FINGERPRINT_EMPTY]
        self._write_packet(self.FINGERPRINT_COMMANDPACKET, data)
        
        packet_type, response = self._read_packet()
        return response[0]

    # Funciones de alto nivel estilo Adafruit
    def get_fingerprint(self):
        """Obtener y buscar huella (estilo Adafruit)"""
        print("🖐️ Coloca el dedo...")
        
        # Intentar capturar imagen
        for i in range(10):
            result = self.getImage()
            if result == self.FINGERPRINT_OK:
                break
            elif result == self.FINGERPRINT_NOFINGER:
                time.sleep(0.5)
                continue
            else:
                return None
        else:
            return None
        
        # Convertir imagen
        if self.image2Tz(1) != self.FINGERPRINT_OK:
            return None
        
        # Buscar en base de datos
        result, finger_id, confidence = self.fingerSearch(1)
        
        if result == self.FINGERPRINT_OK:
            print(f"✅ Huella encontrada: ID {finger_id}, Confianza {confidence}")
            return finger_id
        else:
            print("❌ Huella no encontrada")
            return None

    def enroll_finger(self, location):
        """Registrar nueva huella (estilo Adafruit)"""
        print(f"📝 Registrando huella en posición {location}")
        
        # Primera imagen
        print("1. Coloca el dedo...")
        for i in range(10):
            result = self.getImage()
            if result == self.FINGERPRINT_OK:
                break
            elif result == self.FINGERPRINT_NOFINGER:
                time.sleep(0.5)
                continue
            else:
                raise Exception(f"Error capturando imagen: {result}")
        
        if self.image2Tz(1) != self.FINGERPRINT_OK:
            raise Exception("Error convirtiendo primera imagen")
        
        print("2. Levanta el dedo...")
        time.sleep(1)
        
        print("3. Vuelve a colocar el mismo dedo...")
        for i in range(10):
            result = self.getImage()
            if result == self.FINGERPRINT_OK:
                break
            elif result == self.FINGERPRINT_NOFINGER:
                time.sleep(0.5)
                continue
            else:
                raise Exception(f"Error capturando segunda imagen: {result}")
        
        if self.image2Tz(2) != self.FINGERPRINT_OK:
            raise Exception("Error convirtiendo segunda imagen")
        
        # Crear y guardar modelo
        if self.createModel() != self.FINGERPRINT_OK:
            raise Exception("Error creando modelo")
        
        if self.storeModel(location) != self.FINGERPRINT_OK:
            raise Exception("Error guardando modelo")
        
        print(f"✅ Huella registrada en posición {location}")
        return True

def create_fingerprint_sensor(tx_pin=17, rx_pin=16, baudrate=57600):
    """Crear sensor con configuración específica (estilo Adafruit)"""
    return AdafruitFingerprint(uart_num=2, baudrate=baudrate, tx_pin=tx_pin, rx_pin=rx_pin)

def auto_detect_fingerprint():
    """Auto-detectar configuración del ZMFO40"""
    configuraciones = [
        (17, 16, 57600), (16, 17, 57600),
        (25, 26, 57600), (26, 25, 57600),
    ]
    
    for tx, rx, br in configuraciones:
        try:
            print(f"🔍 Probando TX={tx}, RX={rx}, Baudrate={br}")
            sensor = AdafruitFingerprint(uart_num=2, baudrate=br, tx_pin=tx, rx_pin=rx)
            print(f"✅ Configuración detectada: TX={tx}, RX={rx}, Baudrate={br}")
            return sensor
        except:
            continue
    
    raise Exception("❌ No se pudo detectar configuración automáticamente")

# Ejemplo de uso estilo Adafruit



# Conectar al sensor
finger = auto_detect_fingerprint()

# Registrar huella
#finger.enroll_finger(1)

# Verificar huella
while True:
    finger_id = finger.get_fingerprint()
    if finger_id:
        print(f"Bienvenido usuario {finger_id}")
    time.sleep(1)
    
