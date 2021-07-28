import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED = 12
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,True)
GPIO.setwarnings(False)