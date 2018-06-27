import pyfirmata
import time
from pyfirmata import Arduino, util
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client
import requests
# run by:  python3.5 arduino_soilmoisturelevel.py

board = pyfirmata.Arduino('/dev/ttyACM0')
analog_0 = board.get_pin('a:0:i')
pod_value = "pod1"
mach_serialno = "QWERT1234"

while True:
   
    # soil moisture sensor and level     
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    res = (board.analog[0].read())
     
    if res is None:
        #print('Detecting')
        ret = "0"
    else:
        #print("res: " + str(res))
        #print("res: " + str(res))
        #resround = round(res * 100,0)
        #resround = 0
        #print("resround " + str(resround))
        if res <.0049:
            ret = "0"
        elif res >= .0050 and res <= .4145:
            ret = "25"
        elif res >= .4146 and res <= .5000:
           ret = "50"
        elif res >= .5001 and res <= .5601:
            ret = "75"
        elif res >= .5602: 
            ret = "100"


        #resround = 0
        #print("resround " + str(resround))
        #if resround>65:
        #    ret = "0"
        #elif resround >= 41 and resround <= 65:
        #    ret = "25"
        #elif resround >= 31 and resround <= 40:
        #   ret = "50"
        #elif resround >= 27 and resround <= 30:
        #    ret = "75"
        #elif resround <= 26: 
        #ret = "100"
 
        #print("ret: " + ret) 
        #ret = str(100 - round(res * 100,0))
        #print(ret + '%') 

        if res < .8000:
            #urlsms = 'http://172.16.1.71:3000/api/receiveflagresult/{ "pod": "'+ pod_value+'", "status": "'+ret+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'" }'
            urlsms = 'https://ravenview.herokuapp.com/api/receiveflagresult/{ "pod": "'+ pod_value+'", "status": "'+ret+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'" }'
            #print(urlsms)
            respsms = requests.get(urlsms)
            #print(respsms)
            time.sleep(60)
