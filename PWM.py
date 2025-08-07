from machine import Pin, PWM
from time import sleep

def acelerar_pwm(pin_numero, velocidad_inicial=0, velocidad_final=1023, tiempo_total=2.0, tipo="lineal"):
    """
    Acelera PWM gradualmente desde velocidad inicial hasta final
    
    Parámetros:
    - pin_numero: Número del pin GPIO
    - velocidad_inicial: Valor PWM inicial (0-1023)
    - velocidad_final: Valor PWM final (0-1023)  
    - tiempo_total: Tiempo total de aceleración en segundos
    - tipo: "lineal", "suave", "rapido"
    
    Retorna: Objeto PWM configurado al valor final
    """
    
    # Crear objeto PWM
    pwm = PWM(Pin(pin_numero))
    pwm.freq(1000)  # Frecuencia 1kHz
    
    # Calcular pasos
    diferencia = velocidad_final - velocidad_inicial
    pasos = 50  # Número de pasos para suavidad
    incremento = diferencia / pasos
    delay = tiempo_total / pasos
    
    print(f"🚀 Acelerando PWM Pin {pin_numero}")
    print(f"   {velocidad_inicial} → {velocidad_final} en {tiempo_total}s")
    
    # Establecer velocidad inicial
    pwm.duty(velocidad_inicial)
    
    # Acelerar gradualmente
    for paso in range(pasos + 1):
        if tipo == "lineal":
            # Aceleración lineal constante
            valor = velocidad_inicial + (incremento * paso)
            
        elif tipo == "suave":
            # Aceleración suave (curva seno)
            import math
            progreso = paso / pasos
            factor_suave = math.sin(progreso * math.pi / 2)
            valor = velocidad_inicial + (diferencia * factor_suave)
            
        elif tipo == "rapido":
            # Aceleración rápida al inicio, lenta al final
            import math
            progreso = paso / pasos
            factor_rapido = math.sqrt(progreso)
            valor = velocidad_inicial + (diferencia * factor_rapido)
        
        # Aplicar valor PWM
        pwm.duty(int(valor))
        
        # Mostrar progreso cada 10 pasos
        if paso % 10 == 0:
            porcentaje = (paso / pasos) * 100
            print(f"   {porcentaje:3.0f}% - PWM: {int(valor)}")
        
        sleep(delay)
    
    print(f"✅ Aceleración completada - PWM: {velocidad_final}")
    return pwm

# ========================================
# FUNCIÓN DE DESACELERACIÓN
# ========================================

def desacelerar_pwm(pwm_obj, velocidad_final=0, tiempo_total=1.0):
    """
    Desacelera PWM gradualmente hasta velocidad final
    
    Parámetros:
    - pwm_obj: Objeto PWM ya creado
    - velocidad_final: Valor PWM final (generalmente 0)
    - tiempo_total: Tiempo de desaceleración
    
    Retorna: Valor final aplicado
    """
    
    # Obtener velocidad actual (aproximada)
    velocidad_actual = 1023  # Asumir máxima si no se puede leer
    
    diferencia = velocidad_actual - velocidad_final
    pasos = 30
    incremento = diferencia / pasos
    delay = tiempo_total / pasos
    
    print(f"🛑 Desacelerando PWM")
    print(f"   {velocidad_actual} → {velocidad_final} en {tiempo_total}s")
    
    # Desacelerar gradualmente
    for paso in range(pasos + 1):
        valor = velocidad_actual - (incremento * paso)
        pwm_obj.duty(int(valor))
        
        if paso % 10 == 0:
            porcentaje = (paso / pasos) * 100
            print(f"   {porcentaje:3.0f}% - PWM: {int(valor)}")
        
        sleep(delay)
    
    print(f"✅ Desaceleración completada - PWM: {velocidad_final}")
    return velocidad_final
