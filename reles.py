from machine import Pin
import time

# Configurar los pines de los relés
rele1 = Pin(27, Pin.OUT)
rele2 = Pin(25, Pin.OUT)
rele3 = Pin(26, Pin.OUT)

# === OPCIÓN 1: Invertir directamente en el código ===
print("Activando relés con lógica invertida...")

# Para ACTIVAR el relé (cerrar circuito) usamos .off()
rele1.off()  # Relé 1 ACTIVADO (antes era .on())
time.sleep(1)
rele1.on()   # Relé 1 DESACTIVADO (antes era .off())
print("Relé 1 completado")

rele2.off()  # Relé 2 ACTIVADO
time.sleep(1)
rele2.on()   # Relé 2 DESACTIVADO
print("Relé 2 completado")

rele3.off()  # Relé 3 ACTIVADO
time.sleep(1)
rele3.on()   # Relé 3 DESACTIVADO
print("Relé 3 completado")

print("=== Secuencia completada ===")

# === OPCIÓN 2: Funciones para mayor claridad ===
def activar_rele(rele):
    """Activa el relé (lógica invertida)"""
    rele.off()

def desactivar_rele(rele):
    """Desactiva el relé (lógica invertida)"""
    rele.on()

def inicializar_reles():
    """Asegura que todos los relés estén desactivados al inicio"""
    rele1.on()
    rele2.on()
    rele3.on()
    print("Todos los relés inicializados (desactivados)")

# Ejemplo usando las funciones
print("\n=== Usando funciones claras ===")
inicializar_reles()
time.sleep(1)

print("Activando relé 1...")
activar_rele(rele1)
time.sleep(1)
desactivar_rele(rele1)
print("Relé 1 desactivado")

print("Activando relé 2...")
activar_rele(rele2)
time.sleep(1)
desactivar_rele(rele2)
print("Relé 2 desactivado")

print("Activando relé 3...")
activar_rele(rele3)
time.sleep(1)
desactivar_rele(rele3)
print("Relé 3 desactivado")

# === OPCIÓN 3: Clase para manejo más avanzado ===
class ReleInvertido:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.OUT)
        self.desactivar()  # Inicializar desactivado
    
    def activar(self):
        """Activa el relé (pin LOW)"""
        self.pin.off()
        self.estado = True
    
    def desactivar(self):
        """Desactiva el relé (pin HIGH)"""
        self.pin.on()
        self.estado = False
    
    def toggle(self):
        """Cambia el estado del relé"""
        if self.estado:
            self.desactivar()
        else:
            self.activar()
    
    def pulso(self, duracion=1):
        """Activa el relé por un tiempo determinado"""
        self.activar()
        time.sleep(duracion)
        self.desactivar()

# Ejemplo usando la clase
print("\n=== Usando clase ReleInvertido ===")
relay1 = ReleInvertido(27)
relay2 = ReleInvertido(25)
relay3 = ReleInvertido(26)

# Secuencia con pulsos
relay1.pulso(2)
print("Pulso relé 1 completado")

relay2.pulso(2)
print("Pulso relé 2 completado")

relay3.pulso(2)
print("Pulso relé 3 completado")

