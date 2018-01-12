#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
from subprocess import call



def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)
    
    

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)

sleep(3)
SetAngle(100)
sleep(0.2)
SetAngle(22)
sleep(0.2)
SetAngle(100)
pwm.stop()
print("DONE")
speech="Your kettle is ON"
call(["espeak",speech, "&> /dev/null"])
GPIO.cleanup()
