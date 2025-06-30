from machine import Pin, PWM
import time

# Configurar el pin 27 para el buzzer
buzzer_pin = Pin(27, Pin.OUT)
led_pin=Pin(14, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)

def beep_simple(duration=0.5):
    """Sonido simple encendido/apagado"""
    buzzer_pin.on()
    time.sleep(duration)
    buzzer_pin.off()
    time.sleep(0.1)

def beep_tone(frequency, duration, duty=512):
    """Generar tono con frecuencia específica usando PWM"""
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty(duty)  # duty de 0-1023 (512 = 50%)
    time.sleep(duration)
    buzzer_pwm.duty(0)  # Silencio

def play_note(frequency, duration):
    """Tocar una nota musical"""
    if frequency > 0:
        beep_tone(frequency, duration)
    else:
        time.sleep(duration)  # Pausa/silencio
    time.sleep(0.05)  # Pequeña pausa entre notas

def play_melody():
    """Tocar una melodía simple"""
    # Frecuencias de notas musicales (Do, Re, Mi, Fa, Sol, La, Si, Do)
    melody = [262, 294, 330, 349, 392, 440, 494, 523]
    
    print("Tocando melodía...")
    for note in melody:
        play_note(note, 0.3)

def play_mario_theme():
    """Tema clásico de Mario Bros (fragmento)"""
    mario_notes = [
        659, 659, 0, 659, 0, 523, 659, 0, 784,
        392, 0, 523, 0, 392, 0, 330, 0, 440,
        0, 494, 0, 466, 440, 0, 392, 659, 784, 880
    ]
    
    mario_durations = [
        0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.3,
        0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.3, 0.15, 0.3,
        0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.3, 0.15, 0.15, 0.15
    ]
    
    print("Tocando tema de Mario...")
    for i in range(len(mario_notes)):
        play_note(mario_notes[i], mario_durations[i])

def alarm():
    """Sonido de alarma alternante"""
    print("¡ALARMA!")
    for i in range(10):
        beep_tone(2000, 0.15)
        beep_tone(1000, 0.15)
        
def buzz_on():
    """Encender buzzer continuo"""
    buzzer_pin.on()

def buzz_off():
    """Apagar buzzer"""
    buzzer_pin.off()
    buzzer_pwm.duty(0)

def cleanup():
    """Limpiar y apagar buzzer"""
    buzzer_pwm.duty(0)
    buzzer_pin.off()
    print("Buzzer apagado")

# Ejecutar prueba automáticamente
if __name__ == "__main__":
    try:
        led_pin.on()
        time.sleep(3)

        alarm()
        time.sleep(3)
        led_pin.off()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    finally:
        cleanup()

