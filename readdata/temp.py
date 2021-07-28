from w1thermsensor import W1ThermSensor

from fanon import *
print("Start the test with fan on")

for sensor in W1ThermSensor.get_available_sensors():
   print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
while True:
  if sensor.get_temperature() <=28:
     from fanon import *
    #from pwmtest import
     print("Sensor %s has temperature %.2f, fan on" % (sensor.id, sensor.get_temperature()))
  if sensor.get_temperature() >=28:
     print("Sensor %s has temperature %.2f, fan off" % (sensor.id, sensor.get_temperature()))
     print("Tem higher than 20 celsius, the fan is off")
     from fanoff import *
     from pwmtest import *
     sleep(1)