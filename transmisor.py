# ========================================
# CÓDIGO LORA CORREGIDO - CON VERIFICACIÓN
# ========================================

from machine import UART, Pin
from time import sleep

# ⚡ CONFIGURACIÓN CORRECTA (CORREGIDA)
RXD2 = 17  # CORREGIDO: era 16
TXD2 = 16  # CORREGIDO: era 17
uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, rx=Pin(RXD2), tx=Pin(TXD2))

# LED de estado para mostrar éxito/error
led_status = Pin(2, Pin.OUT)
led_tx = Pin(4, Pin.OUT)

# Estadísticas
envios_exitosos = 0
envios_fallidos = 0

# Función que SÍ verifica si se envió
def send_cmd(cmd):
    global envios_exitosos, envios_fallidos
    
    print(f"-> {cmd}")
    
    # Limpiar buffer antes de enviar
    while uart2.any():
        uart2.read()
    
    # Enviar comando
    uart2.write(cmd + '\r\n')
    sleep(1.5)  # Esperar respuesta
    
    # Verificar respuesta
    if uart2.any():
        response = uart2.read()
        try:
            decoded = response.decode('utf-8')
            print(f"✓ Respuesta: {decoded.strip()}")
            
            if "+OK" in decoded:
                print("✅ COMANDO EXITOSO")
                led_status.on()
                sleep(0.1)
                led_status.off()
                envios_exitosos += 1
                return True
            else:
                print("⚠️  Respuesta inesperada")
                envios_fallidos += 1
                return False
                
        except Exception as e:
            print(f"❌ Error decodificando: {e}")
            print(f"RAW: {response}")
            envios_fallidos += 1
            return False
    else:
        print("❌ SIN RESPUESTA - Módulo no conectado")
        # Parpadeo de error
        for _ in range(3):
            led_status.on()
            sleep(0.1)
            led_status.off()
            sleep(0.1)
        envios_fallidos += 1
        return False

# Configurar LoRa CON VERIFICACIÓN
def setup_lora():
    print("🔧 Configurando LoRa CON VERIFICACIÓN...")
    
    # Test básico de conectividad
    if not send_cmd("AT"):
        print("❌ MÓDULO LORA NO RESPONDE")
        print("🔍 Verifica conexiones:")
        print(f"   RX: Pin {RXD2}")
        print(f"   TX: Pin {TXD2}")
        print("   VCC: 3.3V")
        print("   GND: GND")
        return False
    
    print("✅ Módulo LoRa responde correctamente")
    
    # Configurar parámetros
    success = True
    success &= send_cmd("AT+ADDRESS=1")      # Transmisor
    success &= send_cmd("AT+NETWORKID=5")    # Red
    
    # Verificar configuración aplicada
    print("\n📋 Verificando configuración...")
    send_cmd("AT+ADDRESS?")
    send_cmd("AT+NETWORKID?")
    send_cmd("AT+PARAMETER?")
    
    if success:
        print("✅ LoRa configurado exitosamente")
        # Triple parpadeo de éxito
        for _ in range(3):
            led_status.on()
            sleep(0.2)
            led_status.off()
            sleep(0.1)
        return True
    else:
        print("❌ Error en configuración LoRa")
        return False

# Enviar código CON VERIFICACIÓN
def send_code(codigo):
    global envios_exitosos, envios_fallidos
    
    codigo = str(codigo)
    cmd = f"AT+SEND=2,{len(codigo)},{codigo}"
    
    print(f"\n📤 Enviando código: {codigo}")
    
    # Indicador visual de transmisión
    led_tx.on()
    
    success = send_cmd(cmd)
    
    led_tx.off()
    
    if success:
        print(f"🎯 Código {codigo} enviado AL RECEPTOR")
        return True
    else:
        print(f"💥 ERROR enviando código {codigo}")
        return False

# ========================================
# PROGRAMA PRINCIPAL MEJORADO
# ========================================

print("🚀 === CONTROL REMOTO LORA VERIFICADO ===")
print(f"📡 Configuración: RX=Pin{RXD2}, TX=Pin{TXD2}")

# Inicializar LEDs
led_status.off()
led_tx.off()

# Configurar LoRa con verificación
if not setup_lora():
    print("💥 FALLO CRÍTICO: No se pudo configurar LoRa")
    print("🛑 Programa detenido")
    exit()

# Pines de botones
n1 = Pin(14, Pin.IN, Pin.PULL_UP)  # derecha
n3 = Pin(19, Pin.IN, Pin.PULL_UP)  # atras
n4 = Pin(21, Pin.IN, Pin.PULL_UP)  # izquierda
n5 = Pin(22, Pin.IN, Pin.PULL_UP)  # adelante
n6 = Pin(23, Pin.IN, Pin.PULL_UP)  # encender/apagar

# Estados anteriores
last_n1 = last_n3 = last_n4 = last_n5 = last_n6 = 1

print("\n🎮 BOTONES CONFIGURADOS:")
print("Pin 14 = 🡢 DERECHA   (código 1)")
print("Pin 19 = 🡣 ABAJO     (código 2)")
print("Pin 21 = 🡠 IZQUIERDA (código 3)")
print("Pin 22 = 🡡 ARRIBA    (código 4)")
print("Pin 23 = ⚡ POWER     (código 5)")
print("\n💡 INDICADORES:")
print("Pin 2 = LED STATUS (parpadea al enviar)")
print("Pin 4 = LED TX (encendido durante transmisión)")
print("=====================================")

button_count = 0

try:
    while True:
        # Leer botones
        c1, c3, c4, c5, c6 = n1.value(), n3.value(), n4.value(), n5.value(), n6.value()
        
        # Detectar presiones (flanco descendente)
        if last_n1 == 1 and c1 == 0:
            button_count += 1
            print(f"\n🎮 BOTÓN #{button_count}: 🡢 DERECHA")
            send_code("1")
        
        if last_n3 == 1 and c3 == 0:
            button_count += 1
            print(f"\n🎮 BOTÓN #{button_count}: 🡣 ABAJO")
            send_code("2")
        
        if last_n4 == 1 and c4 == 0:
            button_count += 1
            print(f"\n🎮 BOTÓN #{button_count}: 🡠 IZQUIERDA")
            send_code("3")
        
        if last_n5 == 1 and c5 == 0:
            button_count += 1
            print(f"\n🎮 BOTÓN #{button_count}: 🡡 ARRIBA")
            send_code("4")
        
        if last_n6 == 1 and c6 == 0:
            button_count += 1
            print(f"\n🎮 BOTÓN #{button_count}: ⚡ POWER")
            send_code("5")
        
        # Actualizar estados
        last_n1, last_n3, last_n4, last_n5, last_n6 = c1, c3, c4, c5, c6
        
        # Mostrar estadísticas cada 10 botones
        if button_count > 0 and button_count % 10 == 0:
            total = envios_exitosos + envios_fallidos
            tasa = (envios_exitosos / total * 100) if total > 0 else 0
            print(f"\n📊 ESTADÍSTICAS:")
            print(f"   Botones presionados: {button_count}")
            print(f"   Envíos exitosos: {envios_exitosos}")
            print(f"   Envíos fallidos: {envios_fallidos}")
            print(f"   Tasa de éxito: {tasa:.1f}%")
        
        sleep(0.05)  # Anti-rebote

except KeyboardInterrupt:
    print(f"\n🛑 Control remoto detenido")
    total = envios_exitosos + envios_fallidos
    tasa = (envios_exitosos / total * 100) if total > 0 else 0
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   Botones presionados: {button_count}")
    print(f"   Envíos exitosos: {envios_exitosos}")
    print(f"   Envíos fallidos: {envios_fallidos}")
    print(f"   Tasa de éxito: {tasa:.1f}%")
    
    if tasa < 80:
        print("⚠️  BAJA TASA DE ÉXITO:")
        print("   - Verifica alimentación del módulo")
        print("   - Acerca módulos para pruebas")
        print("   - Revisa configuración del receptor")

# Limpiar LEDs al salir
led_status.off()
led_tx.off()

print("✅ Programa terminado")