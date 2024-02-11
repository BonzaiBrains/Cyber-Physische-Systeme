# English translation
```
#!/usr/bin/env python3 # Shebang
import RPi.GPIO as GPIO
import time, date time

# Pins
servo_pin = 15 # Board pin for the servo
buzzer_pin = 11 # Board pin for the buzzer
input_magnet = 13 # Board pin for the magnet sensor
input_button = 35 # Board pin for the button

GPIO.setmode(GPIO.BOARD)# Define numbers of the GPIO pins on BOARD
GPIO.setup(servo_pin, GPIO.OUT) # Sets servo_pin as output
GPIO.setup(buzzer_pin, GPIO.OUT) # Sets buzzer_pin as outputs
GPIO.output(buzzer_pin, GPIO.HIGH) # Sets buzzer_pin high(+3.3V) to turn off the buzzer
GPIO.setup(input_magnet, GPIO.IN) # Sets input_magnet as input
GPIO.setup(input_button, GPIO.IN) # Sets input_button as input
pwm = GPIO.PWM(servo_pin, 50) # Sets heart number for the servo_pin
pwm.start(0) # Starts PWM for the servo_pin

global button_status # Global variable button_status
global magnet_status # Global variable magnet_status

def servo_lock():
     pwm.ChangeDutyCycle(11.5) # Rotate servo to lock
     time.sleep(.1)
    
def servo_unlock():
     pwm.ChangeDutyCycle(1.9) # Rotate servo to unlock
     time.sleep(.1)

def alarm():
     while True: # Lets the buzzer run until interrupted
         GPIO.output(buzzer_pin, GPIO.LOW) # Buzzer set to On
         time.sleep(0.1)
         GPIO.output(buzzer_pin, GPIO.HIGH) # Buzzer set to off
         time.sleep(0.1)

def button_press():
     global button_status
     if (GPIO.input(input_button) == True): # If the input_button is de-energized
         button_status = 1 # button_status set to 1
     else: # If the input_button has power
         button_status = 0 # button status set to 0
         time.sleep(10) # Wait while the button is pressed
         print("button pressed")
     return button_status

def magnet():
     global magnet_status
     if (GPIO.input(input_magnet) == True): # If the input_magnet is de-energized
         magnet_status = 0 # magnet_status set to 0
         print("Not Open")
     else: # If the input_magnet has power
         magnet_status = 1 # magnet_status set to 0
         print("Open")
     return magnet_status
    
def main():
     whileTrue:
         if (datetime.datetime.now().strftime("%M") == "19"): # If a certain time is returned and is equal to the value
             servo_lock() # Lock servo
             print("Locked")
         elif (datetime.datetime.now().strftime("%M") == "20"): # If a certain time is returned and is equal to the value
             servo_unlock() # Unlock servo
             print("Not Locked")
         button_press() # Status check of input_button
         magnet() # Check status of input_magnet
         if button_status == 1 and magnet_status == 1: # If the status of button_status and magnet_status are both equal to 1 (the input_button has not been printed and the input_magnet is not active)
             print("Alarm triggered")
             alarm() # Trigger alarm
         else: # Otherwise sure
             print("Sure")
        
    
def destroy():
     GPIO.output(buzzer_pin, GPIO.HIGH) # Turn buzzer off
     GPIO.cleanup() # Free GPIO for new processes

if __name__ == '__main__': # Program start from here
     print("Press Ctrl+C to exit the program...")
    
     try: #
         Main()
     except KeyboardInterrupt: # When 'Ctrl+C' is pressed
         destroy()
```


