import json

def sensordetect(filename,a):
    with open(filename) as json_file:
       sensorlib= json.load(json_file)
    required_index=input("Sensor detection! Please type in the index: ")
    required_information=input("PLease type in the required index information: ")
    print("Detecting Sensor information....")
    sensors = sensorlib["Sensors"]
    try:
       print(list(filter(lambda x:x[required_index]==required_information,sensors))) 
       a=a+1
       print("Sensor detected! The sensor is named as sensor ",a)
       list(filter(lambda x:x[required_index]==required_information,sensors))
       detectedsensor_new=list(filter(lambda x:x[required_index]==required_information,sensors))
    except (KeyError):
       print("Failed!")
    return detectedsensor_new

def collectsensor(b):
    if input("Dect sensor Y/n ?:")=='Y':
        detectedsensor.append(sensordetect('sensorlib.json',b))
        collectsensor(b+1)
    elif input("Dect sensor Y/n ?:")=='n':
        print("You have detected [",b,"] sensors!")
        print(detectedsensor)
    else:
        collectsensor(b)
#main code
sensornumber=0
detectedsensor=[]
collectsensor(sensornumber)