from machine import I2C, Pin
from bme280 import BME280

import time
import framebuf

import oled
import filemanager

#=======VARS========

#I2C BUSSES
i2c0 = I2C(0, scl = Pin(1), sda = Pin(0), freq = 400000)
i2c1 = I2C(1, scl = Pin(3), sda = Pin(2), freq = 400000)

#OLED'S WIDTH AND HEIGTH
WIDTH  = 128
HEIGTH = 64

#OLED OBJS INITS
oled0 = oled.Charts_and_Images(WIDTH, HEIGTH, i2c0)
oled1 = oled.Snapshot(WIDTH, HEIGTH, i2c1)

#BME280 SENSOR OBJ INIT
sensor = BME280(i2c = i2c0)

#DATA TUPLES FOR CHARTS "(FILE_PATH, MIN_XCOORD, MAX_XCOORD)"
tdata = ("data/temperature", 18, 128)
hdata = ("data/humidity", 26, 128)
pdata = ("data/pressure", 34, 128)

#FILES MANAGER OBJS INIT 
tfile = filemanager.Filemanager(tdata[0])
hfile = filemanager.Filemanager(hdata[0])
pfile = filemanager.Filemanager(pdata[0])

#LOGO IMAGE
raspy_logo = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
raspi = framebuf.FrameBuffer(raspy_logo, 32, 32, framebuf.MONO_HLSB)


#*********LOGO FUNCTION*********#

#Print on oled1 infos, on oled0 a bouncing rasperry logo about 7 seconds
def logo():
    oled1.frame(0, 0, 128, 64, 1)
    oled1.info("Pico Weather", "BOOTING", "(maybe)")
    dx = 1
    dy = 1
    x = 1
    y = 1
    oled0.frame(0, 0, 128, 64, 1)
    for loop in range(705):
        oled0.image(raspi, x, y)
        x = x + dx
        y = y + dy
        if (x == 95) or (x == 1):
            dx = dx * -1
        if (y == 31) or (y == 1):
            dy = dy * -1
    oled0.clear()
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
def temperature_chart(tfiledata, temp, xcoord):
    oled0.temp_chart(tfiledata)
    oled0.turnon_pixel("temperature", int(temp), xcoord)

def humidity_chart(hfiledata, hum, xcoord):
    oled0.hum_chart(hfiledata)
    oled0.turnon_pixel("humidity", int(hum), xcoord)
    
def pressure_chart(pfiledata, press, xcoord):
    oled0.press_chart(pfiledata)
    oled0.turnon_pixel("pressure", int(press), xcoord)


#************MAIN***********#  
  
def main():
    tfile.erase()
    pfile.erase()
    hfile.erase()
    
    sec0 = time.time() #get the time
    
    ticket = 1
    mutex = [True, False, False] #like an array of semaphores for mutex
    
    #min xcoord for each chart
    t_xcoord = tdata[1]
    p_xcoord = pdata[1]
    h_xcoord = hdata[1]
    
    #obj for store the content of the files
    tfiledata = None
    hfiledata = None
    pfiledata = None
    
    while True:
        sec1 = time.time() #reget the time
        
        #print shapshots and return values
        temp_value, hum_value, press_value = sensor_snapshot()
        
        #If 50 seconds have elapsed, change the value of the next element to the first True of the semaphore array
        if (sec1 - sec0) >= 45:
            sec0 = sec1
            ticket = ticket % 3
            mutex[ticket] = True
            ticket += 1
        
        if mutex[0]:
            #If there are records, it prints the relative image of the previous graph
            if pfiledata != None and len(pfiledata) != 0:
                oled0.pressure_image(pfiledata[-1])
            mutex[0] = False
            tfiledata = tfile.read()
            temperature_chart(tfiledata, temp_value, t_xcoord)
            t_xcoord += 1
            if t_xcoord == tdata[2]:
                t_xcoord = tdata[1]
                tfile.erase()
        
        if mutex[1]:
            if tfiledata != None and len(tfiledata) > 0:
                t_ycoord = 60 - ((26 * temp_value) // 20)
                oled0.temperature_image(tfiledata[-1], t_ycoord)
            mutex[1] = False
            hfiledata = hfile.read()
            humidity_chart(hfiledata, hum_value, h_xcoord)
            h_xcoord += 1
            if h_xcoord == hdata[2]:
                h_xcoord = hdata[1]
                hfile.erase()
            
        if mutex[2]:
            if hfiledata != None and len(hfiledata) > 0:
                h_ycoord = 60 - ((26 * hum_value) // 50)
                oled0.humidity_image(hfiledata[-1], h_ycoord)
            mutex[2] = False
            pfiledata = pfile.read()
            pressure_chart(pfiledata, press_value, p_xcoord)
            p_xcoord += 1
            if p_xcoord == pdata[2]:
                p_xcoord = pdata[1]
                pfile.erase()
        
        time.sleep(5)

logo()
app_name()
main()