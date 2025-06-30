import machine
import time

# Pines
in1 = machine.Pin(32, machine.Pin.OUT)
in2 = machine.Pin(33, machine.Pin.OUT)
in3 = machine.Pin(25, machine.Pin.OUT)
in4 = machine.Pin(26, machine.Pin.OUT)

print("=== TEST SIMPLE ===")

# Todo apagado
in1.off()
in2.off()
in3.off()
in4.off()

print("1. Todo apagado")
time.sleep(10)

# Dirección 1
print("2. Probando dirección 1...")
in1.on()
in2.off()
in3.on()
in4.off()

time.sleep(10)

# Parar
in1.off() 
in2.off()
in3.off() 
in4.off()
print("3. Parado")
time.sleep(10)

# Dirección 2
print("4. Probando dirección 2...")
in1.off()
in2.on()
in3.off()
in4.on()
time.sleep(10)

print("2. Probando dirección 1...")
in1.on()
in2.off()
in3.on()
in4.off()

time.sleep(10)



print("\n¿Se movió el motor? Si no:")
print("- Revisar alimentación 12V")
print("- Revisar jumper ENA")
print("- Revisar cables OUT1/OUT2")

