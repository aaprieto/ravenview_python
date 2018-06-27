import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client
import requests

########Soil Moisture Sensor ###################
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
sms = ""
if GPIO.input(channel):
     sms = "{'pod1','no_water_detected'}"
     #sms.extend(['pod1','no_water_detected'])
     print(("No Water Detected! First Pass " + str(GPIO.input(channel))))
     #url = "http://172.16.1.80:3000/api/receiveflagresult/"+sms
     url = "https://immense-lake-27426.herokuapp.com/api/receiveflagresult/No Water Detected"
     print(url)
     resp = requests.get(url)
     print(resp)
     
else:
     sms = "{'pod1','water_detected'}"
     # sms = []

     # sms.extend(['pod1','water_detected'])
     print(("Water Detected!  First Pass " + str(GPIO.input(channel))))
     #url = "http://172.16.1.80:3000/api/receiveflagresult/"+sms
     url = "https://immense-lake-27426.herokuapp.com/api/receiveflagresult/Water Detected"
     print(url)
     resp = requests.get(url)
     print(resp)
 
def callback(channel):
        if GPIO.input(channel):
                #sms = [] 
                #sms.extend(['pod1','no_water_detected'])
                sms = "{'pod1','no_water_detected'}"
                print(("No Water Detected! " + str(GPIO.input(channel))))
                #url = "http://172.16.1.80:3000/api/receiveflagresult/"+sms
                url = "https://immense-lake-27426.herokuapp.com/api/receiveflagresult/No Water Detected"
                print(url)
                resp = requests.get(url)
                print(resp)
        else:
                #sms = []
                #sms.extend(['pod1','water_detected'])
                sms = "{'pod1','water_detected'}"
                print(("Water Detected! " + str(GPIO.input(channel))))
                #url = "http://172.16.1.80:3000/api/receiveflagresult/"+sms
                url = "https://immense-lake-27426.herokuapp.com/api/receiveflagresult/Water Detected"
                print(url)
                resp = requests.get(url)
                print(resp)
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# while True:
#         time.sleep(1)



# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=14)

while True:
     result = instance.read()
     print(result.is_valid())
     if result.is_valid():
         print(("Last valid input: " + str(datetime.datetime.now())))
         print(("Temperature: %d C" % result.temperature))
         print(("Temperature: %d F" % ((result.temperature * 9/5)+32)))
         #print("Humidity: %d %%" % result.humidity)
         print(("Humidity: " + str(result.humidity)))
         temphumid = str(datetime.datetime.now()) + ";" + str(result.temperature) + ";" + str(((result.temperature * 9/5)+32)) + ";" + str(result.humidity)
         #url = "http://172.16.1.80:3000/api/receivetemperaturehumidity/" + str(temphumid)
         url = "https://immense-lake-27426.herokuapp.com/api/receivetemperaturehumidity/" + str(temphumid)
         resp = requests.get(url)
         print(resp)
     time.sleep(5)
