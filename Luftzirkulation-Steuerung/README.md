# Projekt Luftzirkulation Steuerung

## Ausführung

In einem Terminal Emulator `./main.py` ausführen. Mit `Strg-C` können sie das Programm stoppen.

## Abhängigkeiten 

Liste on benötigten Libraries:

* RPi.GPIO 
* time(Builtin)
* datetime(Builtin)
* json(Builtin)
* board
* Adafruit-DHT

Installation von Abhängigkeiten:

**Mit pip**

```
$ pip install RPi.GPIO paho.mqtt.client board adafruit_dht
```

oder

**Mit pipx**
```
$ pipx install RPi.GPIO paho.mqtt.client board adafruit_dht
```

oder

**Mit apt**
```
$ sudo apt install rpi.gpio python3-paho-mqtt
```
## Prozess

### Schritt 1: Skizze der geplanten Box

Um das Projekt zu beginnen, haben wir eine Skizze unserer geplanten Box erstellt. Diese Skizze diente als Grundlage für das Design und half uns dabei, die Platzierung der Komponenten sowie die Größe der Box zu bestimmen.

Die Skizze beinhaltet die Positionen für den Schrittmotor (welche später angepasst wurde) und den Temperatur/Feuchtigkeit-Sensor. Sie ermöglichte es uns, eine klare Vorstellung von der äußeren Erscheinung der Box zu erhalten und half bei der Planung des Zusammenbaus.

![Skizze-Dachluken-Steuerung](skizze-dachluken-steuerung.png)

### Schritt 2: Vorbereitung

Im Vorbereitungsprozess haben wir den Temperatur/Feuchtigkeit-Sensor, Eclipse-MQTT-Broker und den Schrittmotor einzeln getestet und zum Laufen gebracht. Dies wurde durch die Entwicklung separater Programmcodes für jeden Sensor erreicht. Hier sind die durchgeführten Tests:

Schrittmotor: 
* Es wurde Sample-Code verwendet um die funktion zu testen des Schrittmotors. 
* Ein Programm wurde erfasst um die funktion mit einem MQTT Subscription process zu verknüpfen. 

Temperatur/Feuchtigkeit-Sensor:
* Der Temperatur/Feuchtigkeit-Sensor wurde, mit hilfe offizieller Dokumentation und Sample-Code, ausgelesen.
* Ein Programm wurde erfasst um die funktion mit einem MQTT Publish process zu verknüpfen. 

Eclipse-MQTT-Broker
* Wir haben die logs in `/var/log/mosquitto.log` analysiert und ausgewertet. 
* Wir haben einen -PUB und MQTT-SUB nachgestellt.

### Schritt 3: Entwicklung des Hauptprogramms

Im Hauptprogramm 

## Schaltplan

![Schaltplan-Luftzirkulations-Steuerung](schaltplan-luftzirkulations-steuerung.png)

## Projekt Bilder

![Bild-Luftzirkulations-Steuerung](bild-luftzirkulations-steuerung.png)

## Code

### Main

```
#!/usr/bin/python3
import threading
import mqtt_pub, mqtt_sub

def pub():
	mqtt_pub.main()

def sub():
	mqtt_sub.main()
	
def main():
	thread_pub.start() # Start thread for publish 
	thread_sub.start() # Start thread for subscribe
	
if __name__ == "__main__":
	thread_pub = threading.Thread(target=pub)
	thread_sub = threading.Thread(target=sub)
	main()

```

### MQTT Subscribe

```
#!/usr/bin/python3
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time

def main():
	def get_value_from_json(json_file, key, sub_key):
		try:
			with open(json_file) as f:
				data = json.load(f)
				return data[key][sub_key]
		except Exception as e:
			print("ERROR: ", e)

	# MQTT Connection Details
	mqtt_broker = get_value_from_json("secrets.json", "mqtt_broker_sub", "host")
	mqtt_topic = get_value_from_json("secrets.json", "mqtt_broker_sub", "topic")

	# PIN-Zuweisung am Raspberry
	A=18
	B=23
	C=24
	D=25
	time_t = 0.001

	# GPIO Setup
	gpio.setup(A,gpio.OUT)
	gpio.setup(B,gpio.OUT)
	gpio.setup(C,gpio.OUT)
	gpio.setup(D,gpio.OUT)
	gpio.output(A, False)
	gpio.output(B, False)
	gpio.output(C, False)
	gpio.output(D, False)
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)

	# Motor steps
	def Step1():
		gpio.output(D, True)
		time.sleep(time_t)
		gpio.output(D, False)

	def Step2():
		gpio.output(D, True)
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(D, False)
		gpio.output(C, False)

	def Step3():
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(C, False)
	def Step4():
		gpio.output(B, True)
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(B, False)
		gpio.output(C, False)

	def Step5():
		gpio.output(B, True)
		time.sleep(time_t)
		gpio.output(B, False)

	def Step6():
		gpio.output(A, True)
		gpio.output(B, True)
		time.sleep(time_t)
		gpio.output(A, False)
		gpio.output(B, False)

	def Step7():
		gpio.output(A, True)
		time.sleep(time_t)
		gpio.output(A, False)

	def Step8():
		gpio.output(D, True)
		gpio.output(A, True)
		time.sleep(time_t)
		gpio.output(D, False)
		gpio.output(A, False)

	# Motor up rotation
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
	# Motor down rotation
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

	# MQTT connection
	def on_connect(client, userdata, flags, rc, msg):
	    print("Connected with result code " + str(rc))

	temp = 20.0
	humid = 50.0

	# Message Handeling
	def on_message(client, userdata, msg):
	    match msg.topic:
	    	case "Group5/Humid":
				temp_humid = float(msg.payload.decode())
				if temp_humid >= 40:
					if window_status == 1:
						print("OPEN")
					else:
						up()
						window_status = 1
						print("OPEN")
						time.sleep(1)
				else:
					if window_status == 0: 
						print("CLOSED")
					else:
						down()
						window_status = 0
						print("CLOSED")
						time.sleep(1)
				return humid
					
	    	case "Group5/Temp":
	    	    temp_temperature = float (msg.payload.decode())
	    		if temp_temperature >= 23:
					if window_status == 1:
						print("OPEN")
						continue	
					else:
						up()
						window_status == 0
						time.sleep(1)
						return temp
				else:
					if window_status == 0:
						print("CLOSED")
					else:
						down()
						window_status = 0
						print("CLOSED")
						time.sleep(1)
				return temp	
	    	case _:
	    		print("INVALID")


	# MQTT-Broker Connection
	client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	client.on_connect = on_connect
	client.connect(mqtt_broker, 1883, 60)
	client.subscribe(mqtt_topic)
	client.on_message = on_message
	client.loop_start()

if __name__ == "__main__":
	main()
```

### MQTT Publish

```
#!/usr/bin/python3
import time, json, board, adafruit_dht
import paho.mqtt.client as mqtt

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
```




420


## Schaltplan

![Schaltplan-Luftzirkulations-Steuerung](schaltplan-luftzirkulations-steuerung.png)

## Projekt Bilder

![Bild-Luftzirkulations-Steuerung](bild-luftzirkulations-steuerung.png)

## Code

### Main

```
#!/usr/bin/python3
import threading
import mqtt_pub, mqtt_sub

def pub():
	mqtt_pub.main()

def sub():
	mqtt_sub.main()
	
def main():
	thread_pub.start() # Start thread for publish 
	thread_sub.start() # Start thread for subscribe
	
if __name__ == "__main__":
	thread_pub = threading.Thread(target=pub)
	thread_sub = threading.Thread(target=sub)
	main()

```

### MQTT Subscribe

```
#!/usr/bin/python3
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time

def main():
	def get_value_from_json(json_file, key, sub_key):
		try:
			with open(json_file) as f:
				data = json.load(f)
				return data[key][sub_key]
		except Exception as e:
			print("ERROR: ", e)

	# MQTT Connection Details
	mqtt_broker = get_value_from_json("secrets.json", "mqtt_broker_sub", "host")
	mqtt_topic = get_value_from_json("secrets.json", "mqtt_broker_sub", "topic")

	# PIN-Zuweisung am Raspberry
	A=18
	B=23
	C=24
	D=25
	time_t = 0.001

	# GPIO Setup
	gpio.setup(A,gpio.OUT)
	gpio.setup(B,gpio.OUT)
	gpio.setup(C,gpio.OUT)
	gpio.setup(D,gpio.OUT)
	gpio.output(A, False)
	gpio.output(B, False)
	gpio.output(C, False)
	gpio.output(D, False)
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)

	# Motor steps
	def Step1():
		gpio.output(D, True)
		time.sleep(time_t)
		gpio.output(D, False)

	def Step2():
		gpio.output(D, True)
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(D, False)
		gpio.output(C, False)

	def Step3():
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(C, False)
	def Step4():
		gpio.output(B, True)
		gpio.output(C, True)
		time.sleep(time_t)
		gpio.output(B, False)
		gpio.output(C, False)

	def Step5():
		gpio.output(B, True)
		time.sleep(time_t)
		gpio.output(B, False)

	def Step6():
		gpio.output(A, True)
		gpio.output(B, True)
		time.sleep(time_t)
		gpio.output(A, False)
		gpio.output(B, False)

	def Step7():
		gpio.output(A, True)
		time.sleep(time_t)
		gpio.output(A, False)

	def Step8():
		gpio.output(D, True)
		gpio.output(A, True)
		time.sleep(time_t)
		gpio.output(D, False)
		gpio.output(A, False)

	# Motor up rotation
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
	# Motor down rotation
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

	# MQTT connection
	def on_connect(client, userdata, flags, rc, msg):
	    print("Connected with result code " + str(rc))

	temp = 20.0
	humid = 50.0

	# Message Handeling
	def on_message(client, userdata, msg):
	    match msg.topic:
	    	case "Group5/Humid":
				temp_humid = float(msg.payload.decode())
				if temp_humid >= 40:
					if window_status == 1:
						print("OPEN")
					else:
						up()
						window_status = 1
						print("OPEN")
						time.sleep(1)
				else:
					if window_status == 0: 
						print("CLOSED")
					else:
						down()
						window_status = 0
						print("CLOSED")
						time.sleep(1)
				return humid
					
	    	case "Group5/Temp":
	    	    temp_temperature = float (msg.payload.decode())
	    		if temp_temperature >= 23:
					if window_status == 1:
						print("OPEN")
						continue	
					else:
						up()
						window_status == 0
						time.sleep(1)
						return temp
				else:
					if window_status == 0:
						print("CLOSED")
					else:
						down()
						window_status = 0
						print("CLOSED")
						time.sleep(1)
				return temp	
	    	case _:
	    		print("INVALID")


	# MQTT-Broker Connection
	client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
	client.on_connect = on_connect
	client.connect(mqtt_broker, 1883, 60)
	client.subscribe(mqtt_topic)
	client.on_message = on_message
	client.loop_start()

if __name__ == "__main__":
	main()
```

### MQTT Publish

```
#!/usr/bin/python3
import time, json, board, adafruit_dht
import paho.mqtt.client as mqtt

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
```