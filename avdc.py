from machine import ADC, Pin
import time
 
# === CONFIGURACIÓN ADC (GPIO34) ===
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)         # Para leer hasta ~3.6V
adc.width(ADC.WIDTH_12BIT)      # Resolución 12 bits (0-4095)
 
# === CONFIGURACIÓN DEL RELÉ ===
# IN5 del módulo de 8 relés conectado al GPIO26 del ESP32
rele = Pin(26, Pin.OUT)
rele.value(1)  # Inicialmente desactivado (relé OFF si se activa con LOW)
 
# === CONFIGURACIÓN DEL DIVISOR DE VOLTAJE ===
# R1 = 68kΩ, R2 = 20kΩ → factor = (R1 + R2)/R2 = 4
factor = 4.7
 
# === BUCLE PRINCIPAL ===
def Adc():
    valor_adc = adc.read()
    voltaje_adc = valor_adc * (3.3 / 4095)
    voltaje_real = voltaje_adc * factor
 
    print("Voltaje real:", round(voltaje_real, 2), "V")
 
    if voltaje_real > 3.5:
        rele.value(0)  # ACTIVAR relé (LOW)
    else:
        rele.value(1)  # DESACTIVAR relé (HIGH)
 
    time.sleep(0.5)
while True:
    Adc()