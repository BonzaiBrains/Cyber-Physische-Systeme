import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Initialisiere den DHT22-Sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# MQTT-Verbindungsinformationen
mqtt_broker = "172.17.0.102"
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

# Initialisiere den MQTT-Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Verbinde dich mit dem MQTT-Broker
client.connect(mqtt_broker, 1883, 60)

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


while True:
    try:
        # Lese die Werte vom DHT22-Sensor aus
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        
        print(temperature_c)
        print(humidity)
        # Sende die Werte über MQTT
        #client.publish(mqtt_topic+"Temp", payload=f"{temperature_c}", qos=0)
        #client.publish(mqtt_topic+"Humid", payload=f"{humidity}", qos=0)
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5.0)

