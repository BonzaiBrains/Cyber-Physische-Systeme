#!/usr/bin/python3
import threading
import mqtt_pub, mqtt_sub

def pub():
	mqtt_pub.main()

def sub():
	mqtt_sub.main()
	
def main():
	thread_pub.start()
	thread_sub.start()
	
if __name__ == "__main__":
	thread_pub = threading.Thread(target=mqtt_pub)
	thread_sub = threading.Thread(target=mqtt_sub)
	main()
