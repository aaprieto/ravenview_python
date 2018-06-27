import pyfirmata
import time
from pyfirmata import Arduino, util
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client
import requests



board = pyfirmata.Arduino('/dev/ttyACM0')
analog_0 = board.get_pin('a:0:i')


# initialize GPIO

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM) 
#GPIO.cleanup()
# read data using pin 14
#instance = dht11.DHT11(pin=14)



while True:
   
    # soil moisture sensor and level     
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    res = (board.analog[0].read())
     
    if res is None:
        print('Detecting')
        ret = "Detecting ..."
    else:
        
        ret = str(100 - round(res * 100,0))
        print(ret + '%')

    urlsms = "https://immense-lake-27426.herokuapp.com/api/receiveflagresult/" + ret
    print(urlsms)
    respsms = requests.get(urlsms)
    print(respsms)
    

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    instance = dht11.DHT11(pin=14)
    result = instance.read()
    print(result.is_valid())
    if result.is_valid():
         print(("Last valid input: " + str(datetime.datetime.now())))
         print(("Temperature: %d C" % result.temperature))
         print(("Temperature: %d F" % ((result.temperature * 9/5)+32)))
         print(("Humidity: " + str(result.humidity)))
         temphumid = str(datetime.datetime.now()) + ";" + str(result.temperature) + ";" + str(((result.temperature * 9/5)+32)) + ";" + str(result.humidity)
         url = "https://immense-lake-27426.herokuapp.com/api/receivetemperaturehumidity/" + str(temphumid)
         print(url)
         resp = requests.get(url)
         print(resp)
    
         
    time.sleep(5)
