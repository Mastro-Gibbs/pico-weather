from machine import I2C, Pin
from bme280 import BME280
from time import time, sleep
import framebuf

import oled
import filemanager

#=======VARS========

#I2C BUSSES
i2c0 = I2C(0, scl = Pin(1), sda = Pin(0), freq = 400000)
i2c1 = I2C(1, scl = Pin(3), sda = Pin(2), freq = 400000)

#OLED OBJS INITS
oled0 = oled.Charts_and_Images(128, 64, i2c0)
oled1 = oled.Snapshot(128, 64, i2c1)

#BME280 SENSOR OBJ INIT
sensor = BME280(i2c = i2c0)

#FILES MANAGER OBJS INIT 
temperatureFile = filemanager.Filemanager("data/temperature")
humidityFile    = filemanager.Filemanager("data/humidity")
pressureFile    = filemanager.Filemanager("data/pressure")


#*********LOGO FUNCTION*********#

#Print on oled1 infos, on oled0 a raspberry logo about 5 secs 
def logo():
    oled1.frame(0, 0, 128, 64, 1)
    oled1.frame(1, 1, 126, 62, 1)
    oled1.threewords("Pico Weather", "BOOTING", "(maybe)")
    oled0.xtransl_logo()
    oled1.clear()
    
#************FUNCTIONS**************#

def app_name():
    oled1.print_name("Pico Weather")
    
#This function below print the snapshot of the bme280 sensor on oled1
def sensor_snapshot():
    temp = sensor.temperature
    hum = sensor.humidity
    press = sensor.pressure
    oled1.print_temperature(temp)
    oled1.print_humidity(hum)
    oled1.print_pressure(press)
    return temp, hum, press


#These three functions below create the graph and light up the pixel relative to the past value (ycoord) and x coordinate.
#The first parameter is the content of the file, to recreate the previously deleted graph.
def temperature_chart(tfile, temp, xcoord):
    oled0.temp_chart(tfile.read())
    oled0.turnon_pixel("temperature", int(temp), xcoord, tfile)

def humidity_chart(hfile, hum, xcoord):
    oled0.hum_chart(hfile.read())
    oled0.turnon_pixel("humidity", int(hum), xcoord, hfile)
    
def pressure_chart(pfile, press, xcoord):
    oled0.press_chart(pfile.read())
    oled0.turnon_pixel("pressure", int(press), xcoord, pfile)
    

#************MAIN***********#  
  
def main():
    temperatureFile.erase()
    humidityFile.erase()
    pressureFile.erase()
    
    sec0 = time() #get the time
    
    ticket = 1
    mutex = [True, False, False] #like an array of semaphores for mutex
    
    #min xcoord for each chart
    t_xcoord = 18
    h_xcoord = 26
    p_xcoord = 34
    
    while True:
        sec1 = time() #reget the time
        
        #print shapshots and return values
        temp_value, hum_value, press_value = sensor_snapshot()
        
        #If 120 seconds have elapsed, change the value of the next element to the first True of the semaphore array
        if (sec1 - sec0) >= 120:
            sec0 = sec1
            ticket = ticket % 3
            mutex[ticket] = True
            ticket += 1
        
        if mutex[0]:
            if t_xcoord > 128:
                t_xcoord = 18
                temperatureFile.erase()
            temperature_chart(temperatureFile, temp_value, t_xcoord)
            t_xcoord += 1
            mutex[0] = False
        
        if mutex[1]:
            if h_xcoord > 128:
                h_xcoord = 26
                humidityFile.erase()
            humidity_chart(humidityFile, hum_value, h_xcoord)
            h_xcoord += 1
            mutex[1] = False
            
        if mutex[2]:
            if p_xcoord > 128:
                p_xcoord = 34
                pressureFile.erase()
            oled0.pressure_image(press_value)
            pressure_chart(pressureFile, press_value, p_xcoord)
            p_xcoord += 1
            mutex[2] = False
        
        sleep(20)

logo()
app_name()
main()