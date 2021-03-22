from machine import I2C, Pin
from time import sleep

import oled
import filemanager

t_filename = "data/temperature"
h_filename = "data/humidity"
p_filename = "data/pressure"

WIDTH  = 128
HEIGTH = 64

i2c0 = I2C(0, scl = Pin(1), sda = Pin(0), freq = 400000)
i2c1 = I2C(1, scl = Pin(3), sda = Pin(2), freq = 400000)

oled0 = oled.Charts(WIDTH, HEIGTH, i2c0)
oled1 = oled.Snapshot(WIDTH, HEIGTH, i2c1)

oled0.temp_chart()

oled1.print_name("Weather Pico")
oled1.print_temperature(15.3)
oled1.print_pressure(1014.2)
oled1.print_humidity(45.6)

file = filemanager.Filemanager(filename = t_filename)
file.write(1, 3)