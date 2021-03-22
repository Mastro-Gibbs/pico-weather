from machine import I2C, Pin
from bme280 import BME280

import time
import framebuf

import oled
import filemanager


tdata = ("data/temperature", 17, 128)
hdata = ("data/humidity", 25, 128)
pdata = ("data/pressure", 33, 128)

WIDTH  = 128
HEIGTH = 64

buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

i2c0 = I2C(0, scl = Pin(1), sda = Pin(0), freq = 400000)
i2c1 = I2C(1, scl = Pin(3), sda = Pin(2), freq = 400000)

oled0 = oled.Charts(WIDTH, HEIGTH, i2c0)
oled1 = oled.Snapshot(WIDTH, HEIGTH, i2c1)

sensor = BME280(i2c = i2c0)

tfile = filemanager.Filemanager(tdata[0])
hfile = filemanager.Filemanager(hdata[0])
pfile = filemanager.Filemanager(pdata[0])


#*********LOGO FUNCTION*********#

def logo():
    oled1.frame(0, 0, 128, 64, 1)
    oled1.info("Pico Weather", "BOOTING", "(maybe)")
    dx = 1
    dy = 1
    x = 2
    y = 2
    oled0.frame(0, 0, 128, 64, 1)
    for loop in range(705):
        oled0.image(fb, x, y)
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

def temperature_snapshot():
    temp = sensor.temperature
    oled1.clear_temp()
    oled1.print_temperature(temp)
    return temp
    
def humidity_snapshot():
    hum = sensor.humidity
    oled1.clear_hum()
    oled1.print_humidity(hum)
    return hum
    
def pressure_snapshot():
    press = sensor.pressure
    oled1.clear_press()
    oled1.print_pressure(press)
    return press


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
    
    sec0 = time.time()
    ticket = 1
    
    mutex = [True, False, False]
    t_xcoord = tdata[1]
    p_xcoord = pdata[1]
    h_xcoord = hdata[1]
    
    while True:
        sec1 = time.time()
        temp_value = temperature_snapshot()
        hum_value = humidity_snapshot()
        press_value = pressure_snapshot()
        
        if (sec1 - sec0) >= 60:
            sec0 = sec1
            ticket = ticket % 3
            mutex[ticket] = True
            ticket += 1
        
        if mutex[0]:
            mutex[0] = False
            tfiledata = tfile.read()
            temperature_chart(tfiledata, temp_value, t_xcoord)
            t_xcoord += 1
            if t_xcoord == tdata[2]:
                t_xcoord = tdata[1]
                tfile.erase()
        
        if mutex[1]:
            mutex[1] = False
            hfiledata = hfile.read()
            humidity_chart(hfiledata, hum_value, h_xcoord)
            h_xcoord += 1
            if h_xcoord == hdata[2]:
                h_xcoord = hdata[1]
                hfile.erase()
            
        if mutex[2]:
            mutex[2] = False
            pfiledata = pfile.read()
            pressure_chart(pfiledata, press_value, p_xcoord)
            p_xcoord += 1
            if p_xcoord == pdata[2]:
                p_xcoord = pdata[1]
                pfile.erase()
        
        time.sleep(2)

logo()
app_name()
main()