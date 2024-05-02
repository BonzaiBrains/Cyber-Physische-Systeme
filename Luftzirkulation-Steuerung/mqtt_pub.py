#!/usr/bin/python3
import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json

def main():

	def get_value_from_json(json_file, key, sub_key):
		try:
			with open(json_file) as f:
				data = json.load(f)
				return data[key][sub_key]
		except Exception as e:
			print("ERROR: ", e)

	# MQTT Connection Details
	mqtt_broker = get_value_from_json("secrets.json", "mqtt_broker_pub", "host")
	mqtt_topic = get_value_from_json("secrets.json", "mqtt_broker_pub", "topic")


	# Initialisation of DHT22-Sensor
	dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

	# MQTT-Client Initialisation
	client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	client.on_connect = on_connect

	# MQTT-Broker Connection
	client.connect(mqtt_broker, 1883, 60)

	# Callback of the connection to the MQTT-Broker
	def on_connect(client, userdata, flags, rc):
	    print("Connected to MQTT-Broker. Result Code: " + str(rc))

	while True:
		try:
			# Read DHT22-Sensor Values
			read_temperature = dhtDevice.temperature
			read_humidity = dhtDevice.humidity
			print(read_temperature)
			print(read_humidity)        
			# Publish read values
			client.publish(mqtt_topic+"Temp", payload=f"{read_temperature}", qos=0)
			client.publish(mqtt_topic+"Humid", payload=f"{read_humidity}", qos=0)
		except RuntimeError as error:
			print(error.args[0])
			time.sleep(1.0)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error

if __name__ == "__main__":
	main()
