from w1thermsensor import W1ThermSensor
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import smbus
import time
import json


def gpioset(option,Con):
    GPIO.setup(option,GPIO.OUT)
    GPIO.output(option,Con)

def fanon():
    GPIO.setmode(GPIO.BCM)
    gpioset(fan,True)

def compon():
    GPIO.setmode(GPIO.BCM)
    gpioset(comp,True) 

def compoff():
    GPIO.setmode(GPIO.BCM)
    gpioset(comp,False)

def fanoff():
    GPIO.setmode(GPIO.BCM)
    gpioset(fan,False)
    
def readdata():
    [humidity,cTemp]=gethumidity()
    sensortem=np.array(cTemp)
    sensorhum=np.array(humidity)
    sensortime=np.array(str(datetime.datetime.utcnow()))     
    sensordata=np.hstack((sensorhum,sensortem,sensortime))
    for sensor in W1ThermSensor.get_available_sensors(): 
       sensortem2=np.array(sensor.get_temperature())
    if np.around(sensortem-sensortem2) <= 1.8:
       door=np.array('door_open')
    else:
       door=np.array('door_close')
    return sensordata,sensortem,sensorhum,sensortime,sensortem2,door

def gethumidity():
   bus =smbus.SMBus(1)
   #SHT20 address, 0x40(64)
   addr = 0x40
   #Send temperature measurement 
   bus.write_byte(addr,0xF3)   
   time.sleep(0.1)
   data0=bus.read_byte(0x40)
   data1=bus.read_byte(0x40)
   #convert the data
   temp=data0*256+data1
   cTemp=-46.85+((temp*175.72)/65536.0)
   #send humidity measurement command
   bus.write_byte(0x40,0xF5)
   time.sleep(0.1)
   data0=bus.read_byte(0x40)
   data1=bus.read_byte(0x40)
   humidity=data0*256+data1
   humidity=-6+((humidity*125.0)/65536.0)
   return humidity,cTemp

def plotfunction(tim,tem,hum,tem2):   
    #outside temperature
    plt.figure(1)   
    plt.plot(tim,tem,'red',label='tem')
    plt.axhline(25,color='blue',linestyle='--',label='Threshold')
    plt.draw()
    plt.pause(0.0001)
    plt.xticks(rotation=-90, ha='right')
    plt.xlabel('UTC time')
    plt.ylabel('Celsius')
    plt.title('Outside Temperature record')
    plt.tight_layout()
    #inside temperature
    plt.figure(2)   
    plt.plot(tem2,'red',label='tem')
    plt.plot(tem-tem2,'green',linestyle='--')
    plt.axhline(25,color='blue',linestyle='--',label='Threshold')
    plt.draw()
    plt.pause(0.0001)
    plt.xticks(rotation=-90, ha='right')
    plt.xlabel('UTC time')
    plt.ylabel('Celsius')
    plt.title('Intside Temperature record')
    plt.tight_layout()
    #humidity
    plt.figure(3)
    plt.plot(tim,hum,'red',label='tem')
    plt.axhline(35,color='blue',linestyle='--',label='Threshold')
    plt.draw()
    plt.pause(0.0001)
    plt.xticks(rotation=-90, ha='right')
    plt.xlabel('UTC time')
    plt.ylabel('Humidity (%)')
    plt.title('Sensor Humidity record')
    plt.tight_layout()
    #fanfunction
    plt.figure(4)
    plt.plot(fancon,'red',label='fan con')
    plt.draw()
    plt.pause(0.0001)
    plt.ylabel('On(1)/Off(0)')
    plt.ylim(0,1)
    plt.yticks([-1,0,1,2],['-1','Off','On','2'])
    plt.title('Fan condition record')

########################################################################################
# main code start here
# GPIO.setwarnings(False)
# All the address(PIN)
comp = 22   # compressor click  
light = 5   # frdge light ledstrip
lcd = 6     # Fridge display
buzzer = 18 # beeeeee
fan = 12    # fancon

# Sensor check
from sensordetect import *

#read at the first time
[data,tem,hum,tim,tem2,door]=readdata() #test the readdata function and create the arries 
data={'Humidity (%)':[hum],'Outside Temperature (C)':[tem],'Inside Temperature (C)':[tem2],'Door open/close':[door],'Temperature Difference (C)':[tem-tem2],'UTC time (Netherlands)':[tim]}
data=pd.DataFrame(data)
#temperature threshold to control the fan
if tem2>=27.5 and hum>=40:
    from fanon import *
    compon()
    fancon=np.array(1)
    print("fan+compressor on: inside temperature/humidity is high")
elif door=='door_open':
    #from fanon import *
    #compon()
    fancon=np.array(0)
    print("Door opened")
else:
    from fanoff import *
    compoff()
    fancon=np.array(0)         
    print("fan+compressor off: inside temperature/humidity is low and stable") 
#50 times more test
for i in range (50): 
    [newdata,newtem,newhum,newtime,newtem2,newdoor]=readdata()
    newdata=pd.DataFrame({'Humidity (%)':[newhum],'Outside Temperature (C)':[newtem],'Inside Temperature (C)':[newtem2],'Door open/close':[newdoor],'Temperature Difference (C)':[newtem-newtem2],'UTC time (Netherlands)':[newtime]})
    data=data.append(newdata,ignore_index=True)
    pd.DataFrame(data).to_csv("/home/pi/JIP/readdata/data.ods",index=False)
    tem=np.hstack((tem,newtem))
    tim=np.hstack((tim,newtime))
    hum=np.hstack((hum,newhum))
    tem2=np.hstack((tem2,newtem2))
    door=np.hstack((door,newdoor))
    if newtem2>=27.5 and newhum>50:
        fancon=np.hstack((fancon,np.array(1)))
        from fanon import *
        if fancon[len(fancon) -2]==0:
            compon()
            print('Door close')
            print('fan+compressor on: inside temperapture/humidity is high')
    elif newdoor=='door_open' and tem2[len(tem2)-2]-newtem2<=0:
         fancon=np.hstack((fancon,np.array(0)))
         print('Door open')
         #from fanon import *
         if door[len(door)-2]=='door_open':
             #compon()
             print('You forget to close the door')
    elif newdoor=='door_open' and tem2[len(tem2)-2]-newtem2>=0:
         fancon=np.hstack((fancon,np.array(0)))
         from fanoff import *
         if fancon[len(fancon)-2]==1:
             compoff()
             print('fan+compressor off: inside temperature/humidity is low and stable')
    plotfunction(tim,tem,hum,tem2) #the temperature is not updated
    fanoff()
    compoff()