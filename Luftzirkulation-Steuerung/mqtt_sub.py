import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


mqtt_broker = "172.17.110"
mqtt_topic = "Group5/#"
#temp = "Group5/Temp"
#humid = "Group5/Humid"

# PIN-Zuweisung am Raspberry
A=18
B=23
C=24
D=25
time_t = 0.001

# PINS definieren
GPIO.setup(A,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(D,GPIO.OUT)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)

def Step1():
    GPIO.output(D, True)
    time.sleep(time_t)
    GPIO.output(D, False)

def Step2():
    GPIO.output(D, True)
    GPIO.output(C, True)
    time.sleep(time_t)
    GPIO.output(D, False)
    GPIO.output(C, False)

def Step3():
    GPIO.output(C, True)
    time.sleep(time_t)
    GPIO.output(C, False)
def Step4():
    GPIO.output(B, True)
    GPIO.output(C, True)
    time.sleep(time_t)
    GPIO.output(B, False)
    GPIO.output(C, False)

def Step5():
    GPIO.output(B, True)
    time.sleep(time_t)
    GPIO.output(B, False)

def Step6():
    GPIO.output(A, True)
    GPIO.output(B, True)
    time.sleep(time_t)
    GPIO.output(A, False)
    GPIO.output(B, False)

def Step7():
    GPIO.output(A, True)
    time.sleep(time_t)
    GPIO.output(A, False)

def Step8():
    GPIO.output(D, True)
    GPIO.output(A, True)
    time.sleep(time_t)
    GPIO.output(D, False)
    GPIO.output(A, False)

def up():
    for i in range (128):
        Step1()    
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()
def down():
    for i in range (128):
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()

def on_connect(client, userdata, flags, rc, msg):
    print("Connected with result code " + str(rc))

temp = 20.0
humid = 50.0

def on_message(client, userdata, msg):
    
    if msg.topic == "Group5/Humid":
        temp_humid = float (msg.payload.decode())
        print(temp_humid)
        if temp_humid >= 40:
            up()
            time.sleep(1)
            
            
        return humid
    
    if msg.topic == "Group5/Temp":
        temp_temperature = float (msg.payload.decode())
        print(temp_temperature)
        if temp_temperature >= 23.5:
            up()
            time.sleep(1)
            
        return temp



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(mqtt_broker, 1883, 60)

client.subscribe(mqtt_topic)
client.on_message = on_message


client.loop_start()

