import pyfirmata
import time
from pyfirmata import Arduino, util
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client
import requests
# run by:  python3.5 arduino_airtemperature.py

# initialize GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
#GPIO.cleanup()
# read data using pin 14
instance = dht11.DHT11(pin=14)

pod_value = "pod1"
mach_serialno = "QWERT1234"


while True:
    result = instance.read()
    #print(result.is_valid())
    if result.is_valid():
         #print(("Last valid input: " + str(datetime.datetime.now())))
         #print(("Temperature: %d C" % result.temperature))
         #print(("Temperature: %d F" % ((result.temperature * 9/5)+32)))
         #print(("Humidity: " + str(result.humidity)))
         temphumid = str(datetime.datetime.now()) + ";" + str(result.temperature) + ";" + str(((result.temperature * 9/5)+32)) + ";" + str(result.humidity)
         #url = 'http://172.16.1.71:3000/api/receivetemperaturehumidity/{"pod":"'+pod_value+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'","aircelsius":"'+str(result.temperature)+'","airfahrenheit":"'+str(((result.temperature * 9/5)+32))+'","humidity":"'+str(result.humidity)+'"}'
         url = 'https://ravenview.herokuapp.com/api/receivetemperaturehumidity/{"pod":"'+pod_value+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'","aircelsius":"'+str(result.temperature)+'","airfahrenheit":"'+str(((result.temperature * 9/5)+32))+'","humidity":"'+str(result.humidity)+'"}'
         #print(url) 
         resp = requests.get(url)
         #print(resp)
         time.sleep(60)
