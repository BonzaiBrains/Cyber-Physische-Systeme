import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt

# Initialisiere den DHT22-Sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# MQTT-Verbindungsinformationen
mqtt_broker = "172.17.0.110"
mqtt_topic = "Group5/"

# Callback für die Verbindung zum MQTT-Broker
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT-Broker. Result Code: " + str(rc))

# Initialisiere den MQTT-Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Verbinde dich mit dem MQTT-Broker
client.connect(mqtt_broker, 1883, 60)

while True:
    try:
        # Lese die Werte vom DHT22-Sensor aus
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print(temperature_c)
        # Sende die Werte über MQTT
        client.publish(mqtt_topic+"Temp", payload=f"{temperature_c}", qos=0)
        client.publish(mqtt_topic+"Humid", payload=f"{humidity}", qos=0)
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5.0)

GPIO.cleanup()

