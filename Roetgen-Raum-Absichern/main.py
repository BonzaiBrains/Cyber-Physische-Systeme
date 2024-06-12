#!/usr/bin/env python3
import time

#light_status = False
#xray_machine_status = False
global light_status
global door_status_1
global door_status_2



def get_sensor_status_1():
    global door_status_1
    door_status_1 = True
    if door_status_1 == True:
        print("LOG: door 1 is closed")
        time.sleep(1)
    else:
        print("LOG: door 1 is open")
        time.sleep(1)
    return door_status_1
    
def get_sensor_status_2():
    global door_status_2 
    door_status_2 = True
    if door_status_2 == True:
        print("LOG: door 2 is closed")
        time.sleep(1)
    else:
        print("LOG: door 2 is open")
        time.sleep(1)
    return door_status_2
    
def light_blink():
    light_on()
    time.sleep(.2)
    light_off()
    
def light_on():
    global light_status
    light_status = True
    print("LOG: light is on")
    #time.sleep(1)
    #return light_status

def light_off():
    global light_status
    light_status = False
    print("LOG: light is off")
    #time.sleep(1)
    #return light_status

def xray_machine_on():
    global xray_machine_status
    xray_machine_status = True
    print("LOG: xray machine is on")
    time.sleep(1)
    #return xray_machine_status
    
def xray_machine_off():
    global xray_machine_status
    xray_machine_status = False
    print("LOG: xray machine is off")
    time.sleep(1)
    #return xray_machine_status

def main():
    light_off()
    xray_machine_off()
    xray_machine_on()
    
    try:
        while True:
            if xray_machine_status == False:
                if get_sensor_status_1() == False or get_sensor_status_2() == False:
                    light_on()
                else:
                    light_off()
                    
            elif xray_machine_status == True and get_sensor_status_1() == True and get_sensor_status_2() == True:
                while xray_machine_status == True:
                    light_blink()
                    print("LOG: machine running")
                    time.sleep(1)
                else:
                    print        
            else:  
                light_off()
                xray_machine_off()
            
                
    except KeyboardInterrupt:
        print("EXITING...")
        exit()

if __name__ == "__main__":
    main()
