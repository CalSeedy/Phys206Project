import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.output(2,GPIO.LOW)
GPIO.output(3,GPIO.LOW)
GPIO.output(4,GPIO.LOW)

#2 -> too sharp
#3 -> spot on
#4 -> too flat

try:
    while True:
        GPIO.setup(2,GPIO.OUT)
        print("LED on")
        GPIO.output(2,GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(2,GPIO.LOW)

        GPIO.setup(3,GPIO.OUT)
        print("LED on")
        GPIO.output(3,GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(3,GPIO.LOW)

        GPIO.setup(4,GPIO.OUT)
        print("LED on")
        GPIO.output(4,GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(4,GPIO.LOW)
finally:
    GPIO.output(2,GPIO.LOW)
    GPIO.output(3,GPIO.LOW)
    GPIO.output(4,GPIO.LOW)
