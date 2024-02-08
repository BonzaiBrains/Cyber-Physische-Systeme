#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time, datetime

# Pins
ServoPin = 15 # Board Pin für den Servo
BuzzerPin = 11 # Board Pin für den Buzzer
InputMagnet = 13# Board Pin für den Magnet-Sensor
InputButton = 35# Board Pin für den Knopf

GPIO.setmode(GPIO.BOARD)# Nummern GPIOs by BOARD
GPIO.setup(ServoPin, GPIO.OUT) # Setzt ServoPin als Ausgang
GPIO.setup(BuzzerPin, GPIO.OUT) # Setzt BuzzerPin als Ausgange
GPIO.output(BuzzerPin, GPIO.HIGH) # Setzt BuzzerPin high(+3.3V) um den buzzer auszuschalten
GPIO.setup(InputMagnet, GPIO.IN) # Setzt InputMagnet als Eingang
GPIO.setup(InputButton, GPIO.IN) # Setzt InputButton als Eingang
p = GPIO.PWM(ServoPin, 50) # Setzt Herz Zahl für den ServoPin  
p.start(0) # Startet PWM für den ServoPin

global button_status # Globale Variable button_status 
global magnet_status # Globale Variable magnet_status

def servo_lock():
    p.ChangeDutyCycle(11.5) # Servo rotieren zum verriegeln 
    time.sleep(.1)
    
def servo_unlock():
    p.ChangeDutyCycle(1.9) # Servo rotieren zum entriegeln
    time.sleep(.1)

def alarm():
    while True: # Lässt den Buzzer laufen bis interupt
        GPIO.output(BuzzerPin, GPIO.LOW) # Buzzer auf An gesetzt
        time.sleep(0.1)
        GPIO.output(BuzzerPin, GPIO.HIGH) # Buzzer auf Aus gesetzt
        time.sleep(0.1)

def button_press():
    global button_status
    if (GPIO.input(InputButton) == True): # Wenn der InputButton stromlos ist
        button_status = 1 # button_status auf 1 gesetzt
    else:  # Wenn der InputButton strom hat
        button_status = 0 # button-status auf 0 gesetzt
        time.sleep(10) # Warten wen knopf gedrückt ist
        print("Knopf gedrückt")
    return button_status

def magnet():
    global magnet_status 
    if (GPIO.input(InputMagnet) == True): # Wenn der InputMagnet stromlos ist
        magnet_status = 0 # magnet_status auf 0 gesetzt
        print("Nicht Offen")
    else: # Wenn der InputMagnet strom hat
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
        button_press()
        magnet()
        if button_status == 1 and magnet_status == 1:
            print("Alarm ausgelöst")
            alarm()
        else:
            print("Sicher")
        
    
def destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)    # beep off
    GPIO.cleanup()                     # Release resource    

if __name__ == '__main__':     # Program start from here
    print("Press Ctrl+C to end the program...")
    
    try:
        main()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

