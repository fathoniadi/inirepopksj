import RPi.GPIO as GPIO
import time
import logging

def readConfig():
    data = ''
    with open('./.env', 'rb') as file:
        data = file.read()

    configs = {}
    config_all = data.split('\n')
    for config in config_all:
        configs[config.split('=')[0]] = config.split('=')[1]

    return configs

configs = readConfig()

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

p = GPIO.PWM(17,80)

p.start(7.5)

iterasi = 50
waktu = float(configs['timer'])
span = 5/float(iterasi)
span = span * 1.3
sleep = waktu/float(iterasi)
for i in range(0,iterasi):
   p.ChangeDutyCycle(7.5-span*i)
   time.sleep(sleep)

p.stop()

GPIO.cleanup()
