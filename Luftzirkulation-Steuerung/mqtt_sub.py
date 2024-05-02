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
			temp_humid = float (msg.payload.decode())
			if temp_humid >= 40:
				if window_status == 1:
					print("OPEN")
					continue
				else:
					up()
					window_status = 1:
					print("OPEN")
		    			time.sleep(1)
			else:
				if window_status == 0: 
					print("CLOSED")
					continue
				else:
					down()
					window_status = 0:
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
					window_status == 0:
		    			time.sleep(1)
		    		return temp
		    	else:
				if window_status == 0:
					print("CLOSED")
					continue
				else:
					down()
					window_status = 0:
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

