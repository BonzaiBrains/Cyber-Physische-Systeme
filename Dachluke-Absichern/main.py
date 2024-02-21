#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time, datetime

# Pins
servo_pin = 15 # Board Pin für den Servo
buzzer_pin = 11 # Board Pin für den Buzzer
input_magnet = 13 # Board Pin für den Magnet-Sensor
input_button = 40 # Board Pin für den Knopf

GPIO.setmode(GPIO.BOARD)# Numern der GPIO Pins auf BOARD definieren
GPIO.setup(servo_pin, GPIO.OUT) # Setzt servo_pin als Ausgang
GPIO.setup(buzzer_pin, GPIO.OUT) # Setzt buzzer_pin als Ausgange
GPIO.output(buzzer_pin, GPIO.HIGH) # Setzt buzzer_pin high(+3.3V) um den buzzer auszuschalten
GPIO.setup(input_magnet, GPIO.IN) # Setzt input_magnet als Eingang
GPIO.setup(input_button, GPIO.IN) # Setzt input_button als Eingang
pwm = GPIO.PWM(servo_pin, 50) # Setzt Herz Zahl für den servo_pin  
pwm.start(0) # Startet PWM für den servo_pin

global button_status # Globale Variable button_status 
global magnet_status # Globale Variable magnet_status

def servo_lock():
    pwm.ChangeDutyCycle(11.5) # Servo rotieren zum verriegeln 
    time.sleep(.1)
    
def servo_unlock():
    pwm.ChangeDutyCycle(6) # Servo rotieren zum entriegeln
    time.sleep(.1)
	
def alarm():
    while True: # Lässt den Buzzer laufen bis interupt
        GPIO.output(buzzer_pin, GPIO.LOW) # Buzzer auf An gesetzt
        time.sleep(0.1)
        GPIO.output(buzzer_pin, GPIO.HIGH) # Buzzer auf Aus gesetzt
        time.sleep(0.1)

def button_press():
    global button_status
    if (GPIO.input(input_button) == True): # Wenn der input_button stromlos ist
        button_status = 1 # button_status auf 1 gesetzt
    else:  # Wenn der input_button strom hat
        button_status = 0 # button-status auf 0 gesetzt
        time.sleep(10) # Warten wen knopf gedrückt ist
        print("Knopf gedrückt")
    return button_status

def magnet():
    global magnet_status 
    if (GPIO.input(input_magnet) == True): # Wenn der input_magnet stromlos ist
        magnet_status = 0 # magnet_status auf 0 gesetzt
        print("Nicht Offen")
    else: # Wenn der input_magnet strom hat
        magnet_status = 1 # magnet_status auf 0 gesetzt
        print("Offen")
    return magnet_status
    
def main():
    while True:
        if (datetime.datetime.now().strftime("%M") == "19"): # Wenn eine Gewisse Uhrzeit zurück gegeben ist und gleich dem Wert ist 
            servo_lock() # Servo verriegeln
            print("Verschloßen")
        elif (datetime.datetime.now().strftime("%M") == "20"): # Wenn eine Gewisse Uhrzeit zurück gegeben ist und gleich dem Wert ist
            servo_unlock() # Servo entriegeln
            print("Nicht Verschloßen")
        button_press() # Status Prüfung von input_button
        magnet() # Status Prüfung von input_magnet
        if button_status == 1 and magnet_status == 1: # Wenn der status von button_status und magnet_status beide gleich 1 ist (der input_button wurde nicht gedruckt und der input_magnet ist nicht aktiv)  
            print("Alarm ausgelöst") 
            alarm() # Alarm Auslösen
        else: # Ansonsten sicher
            print("Sicher")
        
    
def destroy():
    GPIO.output(buzzer_pin, GPIO.HIGH) # Buzzer aus machen
    GPIO.cleanup() # GPIO freigeben für neue Prozesse

if __name__ == '__main__':     # Program start from here
    print("Drücken Sie Ctrl+C um das Program zu beenden...")
    
    try: # Versuche main auszuführen 
        main()
    except KeyboardInterrupt:  # Wenn 'Ctrl+C' gedrückt wird
        destroy()
