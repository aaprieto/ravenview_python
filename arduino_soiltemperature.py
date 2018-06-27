#!/usr/bin/env python
import os
import time
import dht11
import time
import datetime
import http.client
import requests
# run by:  python3.5 arduino_soiltemperature.py

pod_value = "pod1"
mach_serialno = "QWERT1234"


def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20
 
def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius, farenheit
 
def loop(ds18b20):
    while True:
        if read(ds18b20) != None:
            #print "Current temperature : %0.3f C" % read(ds18b20)[0]
            #print "Current temperature : %0.3f F" % read(ds18b20)[1]
            #print(read(ds18b20)[0])
            #print(read(ds18b20)[1])
            #urlsms = 'http://172.16.1.71:3000/api/receivesoiltemperature/{"pod":"'+pod_value+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'","soilcelsius":"'+str(round(read(ds18b20)[0],1))+'","soilfahrenheit":"'+str(round(read(ds18b20)[1],1))+'"}'
            urlsms = 'https://ravenview.herokuapp.com/api/receivesoiltemperature/{"pod":"'+pod_value+'","machname":"'+mach_serialno+'","datetimereceived":"'+str(datetime.datetime.now())+'","soilcelsius":"'+str(round(read(ds18b20)[0],1))+'","soilfahrenheit":"'+str(round(read(ds18b20)[1],1))+'"}'
            #print(urlsms)
            respsms = requests.get(urlsms)
            #print(respsms)
            time.sleep(1)
 
def kill():
    quit()
 
if __name__ == '__main__':
    try:
        serialNum = sensor()
        loop(serialNum)
    except KeyboardInterrupt:
        kill()