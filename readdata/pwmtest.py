'''
Control the Brightness of LED using PWM on Raspberry Pi
http://www.electronicwings.com
'''

import RPi.GPIO as GPIO
from time import sleep


ledpin=12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle
for duty in range(0,60,1):
        pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
        sleep(0.01)
sleep(0.5)