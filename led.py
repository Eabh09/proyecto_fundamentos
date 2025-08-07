import machine
import time

# Configuración del LED con PWM
# Conexión: LED en pin 2 con resistencia de 220Ω a GND
LED_PIN = 4

# Crear objeto PWM
led_pwm = machine.PWM(machine.Pin(LED_PIN))
led_pwm.freq(1000)  # Frecuencia de 1kHz

def set_brillo(brillo):
    """
    Establece el brillo del LED
    brillo: 0-100 (porcentaje)
    """
    if brillo < 0:
        brillo = 0
    elif brillo > 100:
        brillo = 100
    
    # Convertir porcentaje a duty cycle (0-1023 en ESP32)
    duty = int((brillo / 100) * 1023)
    led_pwm.duty(duty)
    print(f"Brillo: {brillo}% (duty: {duty})")

def fade_in_out():
    """Efecto de fade in y fade out"""
    # Fade in (encender gradualmente)
    for brillo in range(0, 101, 2):
        set_brillo(brillo)
        time.sleep_ms(50)
    
    time.sleep_ms(500)
    
    # Fade out (apagar gradualmente)
    for brillo in range(100, -1, -2):
        set_brillo(brillo)
        time.sleep_ms(50)
    
    time.sleep_ms(500)

def respiracion():
    """Efecto de respiración suave"""
    import math
    
    for i in range(360):
        # Usar función seno para efecto suave
        brillo = int((math.sin(math.radians(i)) + 1) * 50)
        set_brillo(brillo)
        time.sleep_ms(20)

def parpadeo(veces=5, brillo=100):
    """Parpadeo rápido"""
    for _ in range(veces):
        set_brillo(brillo)
        time.sleep_ms(200)
        set_brillo(0)
        time.sleep_ms(200)

# Programa principal
print("Control LED con PWM en MicroPython")
print("Iniciando efectos...")

try:
    while True:
        print("\n=== Fade In/Out ===")
        fade_in_out()
        
        print("\n=== Respiración ===")
        respiracion()
        
        print("\n=== Parpadeo ===")
        parpadeo(3, 80)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDeteniendo...")
    set_brillo(0)  # Apagar LED
    led_pwm.deinit()  # Liberar PWM