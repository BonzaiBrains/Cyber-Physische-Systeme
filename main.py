#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time, datetime

# Pins
ServoPin = 15
BeepPin = 11
InputMagnet = 13
InputButton = 35

GPIO.setmode(GPIO.BOARD)# Numbers GPIOs by BCM
GPIO.setup(ServoPin, GPIO.OUT) #SetServoControl Pin is output
GPIO.setup(BeepPin, GPIO.OUT)   # Set BeepPin's mode is output
GPIO.output(BeepPin, GPIO.HIGH) # Set BeepPin high(+3.3V) to off beep
GPIO.setup(InputMagnet, GPIO.IN)
GPIO.setup(InputButton, GPIO.IN)
p = GPIO.PWM(ServoPin, 50)
p.start(0)

global button_status
global magnet_status

def servo_lock():
    print("bar")
    p.ChangeDutyCycle(11.5)
    time.sleep(.1)
def servo_unlock():
    p.ChangeDutyCycle(1.9)
    time.sleep(.1)
    print("foo")

def alarm():
    while True:
        GPIO.output(BeepPin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(BeepPin, GPIO.HIGH)
        time.sleep(0.1)

def button_press():
    global button_status
    if (GPIO.input(InputButton) == True):
        button_status = 1
    else:
        button_status = 0
        #time.sleep(10)
        print("Knopf gedrückt")
    return button_status

def magnet():
    global magnet_status 
    if (GPIO.input(InputMagnet) == True):
        magnet_status = 0
        print("Nicht Offen")
    else:
        magnet_status = 1
        print("Offen")
    return magnet_status
    
def main():
    while True:
        if (datetime.datetime.now().strftime("%M") == "19"):
            servo_lock()
            print("Verschloßen")
        elif (datetime.datetime.now().strftime("%M") == "20"):
            servo_unlock()
            print("Nicht Verschloßen")
        button_press()
        magnet()
        if button_status == 1 and magnet_status == 1:
            print("Alarm ausgelöst")
            alarm()
        else:
            print("Sicher")
        
    
def destroy():
    GPIO.output(BeepPin, GPIO.HIGH)    # beep off
    GPIO.cleanup()                     # Release resource    

if __name__ == '__main__':     # Program start from here
    print("Press Ctrl+C to end the program...")
    
    try:
        main()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

