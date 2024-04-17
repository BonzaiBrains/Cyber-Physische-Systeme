import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Initialisiere den DHT22-Sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# MQTT-Verbindungsinformationen
mqtt_broker = "172.17.0.103"
mqtt_topic = "Group5/"

GPIO.setmode(GPIO.BCM)

# PIN-Zuweisung am Raspberry
A=18
B=23
C=24
D=25
time = 0.001

# PINS definieren
GPIO.setup(A,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(D,GPIO.OUT)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)


# Callback für die Verbindung zum MQTT-Broker
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT-Broker. Result Code: " + str(rc))

def on_message(client, userdata, msg):
    if msg.topic == "Group5/Humid":
        temp = float (msg.payload.decode())
        print(temp)
        if temp <=56:
            down() # Unten  90° = 5 differenz zwischen den Cycle
            time.sleep(5)
            
            
        return humid

    if msg.topic == "Group5/Temp":
        temp = float (msg.payload.decode())
        print(temp)
        if temp <=23.5:
            up() # Oben 90° = 5 differenz zwischen den Cycle
            time.sleep(5)
            
        return temp

# Initialisiere den MQTT-Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Verbinde dich mit dem MQTT-Broker
client.connect(mqtt_broker, 1883, 60)

client.subscribe(mqtt_topic)
client.on_message = on_message

client.loop_start()

# Ansteuerung der Spulen des Motors
def Step1():
    GPIO.output(D, True)
    sleep (time)
    GPIO.output(D, False)

def Step2():
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(C, False)

def Step3():
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(C, False)
def Step4():
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(B, False)
    GPIO.output(C, False)

def Step5():
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(B, False)

def Step6():
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(A, False)
    GPIO.output(B, False)

def Step7():
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(A, False)

def Step8():
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(A, False)

def up():
    for i in range (128):
        Step1()    
        Step2()
        Step3()
        Step4()
def down():
    for i in range (128):
        Step4()    
        Step3()
        Step2()
        Step1()

while True:
    try:
        
        # Lese die Werte vom DHT22-Sensor aus
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        
        print(temperature_c)
        time.sleep(1)
        print(humidity)
        
        #client.on_message()
        # Sende die Werte über MQTT
        client.publish(mqtt_topic+"Temp", payload=f"{temperature_c}", qos=0)
        client.publish(mqtt_topic+"Humid", payload=f"{humidity}", qos=0)
       
            
    except RuntimeError as error:
        print(error.args[0])
        #time.sleep(2)
        print('ERROR')
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    

