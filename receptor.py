# ========================================
# RECEPTOR LORA CON RELÉS CORREGIDOS
# ========================================

from machine import UART, Pin, PWM
from time import sleep

# Configuración correcta confirmada
uart2 = UART(2, baudrate=115200, rx=Pin(17), tx=Pin(16))

# Relés para control de motor/dispositivo
rele1 = Pin(2, Pin.OUT)   # Motor Adelante A
rele2 = Pin(4, Pin.OUT)   # Motor Adelante B  
rele3 = Pin(5, Pin.OUT)   # Motor Atrás A
rele4 = Pin(18, Pin.OUT)  # Motor Atrás B
D=Pin(19, Pin.IN,Pin.PULL_UP)
R=Pin(20, Pin.IN,Pin.PULL_UP)
Acelerador=Pin(21, Pin.IN,Pin.PULL_UP)

# PWM para velocidad (opcional)
pwm_motor = None

# Botón power y LED
boton_power = Pin(19, Pin.OUT)
led_status = Pin(23, Pin.OUT)

# Estado del sistema
system_on = False

def send_cmd(cmd):
    """Envía comando AT simple"""
    uart2.write(cmd + '\r\n')
    sleep(1)
    if uart2.any():
        response = uart2.read().decode('utf-8')
        return "+OK" in response
    return False

def setup_lora():
    """Configuración mínima"""
    print("Configurando LoRa...")
    
    # Verificar módulo
    if not send_cmd("AT"):
        print("❌ Módulo no responde")
        return False
    
    # Configurar receptor
    send_cmd("AT+ADDRESS=2")
    send_cmd("AT+NETWORKID=5")
    
    print("✅ LoRa configurado")
    return True

def detener_todos_reles():
    """Apaga todos los relés - POSICIÓN SEGURA"""
    rele1.off()
    rele2.off()
    rele3.off()
    rele4.off()
    
    # Detener PWM si existe
    global pwm_motor
    if pwm_motor:
        pwm_motor.deinit()
        pwm_motor = None
    
    print("🛑 Todos los relés apagados")

def motor_adelante():
    """Motor girando hacia adelante"""
    print("⬆️ MOTOR ADELANTE")
    
    # Apagar relés opuestos primero (seguridad)
    rele3.off()
    rele4.off()
    sleep(0.1)  # Pausa de seguridad
    
    # Activar relés para adelante
    rele1.on()
    rele2.on()
    
    # Activar PWM para velocidad
    iniciar_pwm()

def motor_atras():
    """Motor girando hacia atrás"""
    print("⬇️ MOTOR ATRÁS")
    
    # Apagar relés opuestos primero (seguridad)
    rele1.off()
    rele2.off()
    sleep(0.1)  # Pausa de seguridad
    
    # Activar relés para atrás
    rele3.on()
    rele4.on()
    
    # Activar PWM para velocidad
    iniciar_pwm()

def motor_derecha():
    """Motor/dispositivo hacia la derecha"""
    print("➡️ DERECHA")
    
    # Apagar todos primero
    detener_todos_reles()
    sleep(0.1)
    
    # Configuración para derecha (ejemplo: solo rele1 y rele4)
    rele1.on()
    rele4.on()
    
    # PWM opcional
    iniciar_pwm()

def motor_izquierda():
    """Motor/dispositivo hacia la izquierda"""
    print("⬅️ IZQUIERDA")
    
    # Apagar todos primero
    detener_todos_reles()
    sleep(0.1)
    
    # Configuración para izquierda (ejemplo: solo rele2 y rele3)
    rele2.on()
    rele3.on()
    
    # PWM opcional
    iniciar_pwm()

def iniciar_pwm():
    """Inicia PWM para control de velocidad"""
    global pwm_motor
    
    try:
        # Usar pin 21 para PWM (diferente a los relés)
        pwm_motor = PWM(Pin(21))
        pwm_motor.freq(1000)
        pwm_motor.duty(512)  # 50% velocidad inicial
        print("⚡ PWM activado - 50% velocidad")
    except Exception as e:
        print(f"⚠️ Error PWM: {e}")

def acelerar_motor():
    """Aumenta velocidad del motor"""
    global pwm_motor
    
    if pwm_motor:
        try:
            pwm_motor.duty(800)  # 80% velocidad
            print("🚀 Motor acelerado - 80% velocidad")
        except:
            print("❌ Error acelerando")

def presionar_boton(pin, nombre):
    """Simula presión de botón"""
    print(f"🔘 {nombre}")
    pin.on()
    sleep(0.3)
    pin.off()

def procesar_codigo(codigo):
    """Procesa códigos recibidos - CORREGIDO"""
    global system_on
    
    if codigo == "1" and system_on:
        motor_derecha()
        
    elif codigo == "2" and system_on :
        motor_adelante()
        
    elif codigo == "3" and system_on:
        motor_izquierda()
        
    elif codigo == "4" and system_on :
        motor_atras()
        
    elif codigo == "5":  # POWER - CORREGIDO
        system_on = not system_on
        
        if system_on:
            print("✅ SISTEMA ENCENDIDO")
            led_status.on()
        else:
            print("❌ SISTEMA APAGADO")
            led_status.off()
            # Apagar todo al apagar sistema
            detener_todos_reles()
        
             
        if D.value()==0:
           if Acelerador.value()==0:
             if codigo == "1" or codigo == "4":
                pass
             else:
                motor_adelante()

        elif R.value()==0:
            if Acelerador.value()==0:
             if codigo == "1" or codigo == "4":
                pass
             else:
                motor_atras()
            
        
        # Activar botón power físico
        presionar_boton(boton_power, "POWER")
    
    # Código extra para detener (opcional)
    elif codigo == "0" and system_on:
        print("🛑 DETENER TODO")
        detener_todos_reles()

# ========================================
# PROGRAMA PRINCIPAL
# ========================================

print("📡 === RECEPTOR LORA CON RELÉS ===")
print("🔧 Control de motor con 4 relés + PWM")

# Inicializar - POSICIÓN SEGURA
detener_todos_reles()
led_status.off()

# Configurar LoRa
if not setup_lora():
    print("💥 Error configuración")
    exit()

print("\n🔌 === CONFIGURACIÓN DE RELÉS ===")
print("Pin 2  = Relé 1 (Motor Adelante A)")
print("Pin 4  = Relé 2 (Motor Adelante B)")
print("Pin 5  = Relé 3 (Motor Atrás A)")
print("Pin 18 = Relé 4 (Motor Atrás B)")
print("Pin 21 = PWM Motor (velocidad)")
print("Pin 19 = Botón Power")
print("Pin 23 = LED Status")

print("\n👂 Esperando comandos...")
print("1=DERECHA | 2=ADELANTE | 3=IZQUIERDA | 4=ATRÁS | 5=POWER")
print("=" * 50)

# Bucle principal
try:
    while True:
        if uart2.any():
            data = uart2.read()
            try:
                texto = data.decode('utf-8')
                print(f"\n📡 {texto.strip()}")
                
                # Buscar patrón +RCV
                if "+RCV=" in texto:
                    partes = texto.split('+RCV=')[1].split(',')
                    if len(partes) >= 3:
                        datos = partes[2]
                        procesar_codigo(datos.strip())
                
                # Buscar códigos directos
                else:
                    for char in "012345":  # Agregué 0 para DETENER
                        if char in texto:
                            procesar_codigo(char)
                            break
                            
            except Exception as e:
                print(f"❌ Error: {e}")
                print(f"📡 RAW: {data}")
        
        sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Programa detenido")

# Limpiar al salir - SEGURIDAD
print("🔒 Apagando todos los relés por seguridad...")
detener_todos_reles()
led_status.off()

print("✅ Programa terminado")