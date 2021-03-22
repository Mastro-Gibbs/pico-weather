from ssd1306 import SSD1306_I2C
import filemanager

class Oled:
    def __init__(self, width, heigth, i2c):
        self.oled = SSD1306_I2C(width, heigth, i2c)
        
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
    
    def image(self, fb, x, y):
        self.oled.blit(fb, x, y)
        self.oled.show()
        
    def frame(self, x, y, w, h, c):
        self.oled.rect(x, y, w, h, c)
        self.oled.show()
    
    def info(self, name, step, descr):
        x = 64 - ((len(name) * 8) // 2)
        self.oled.text(name, x, 2)
        x = 64 - ((len(step) * 8) // 2)
        self.oled.text(step, x, 24)
        x = 64 - ((len(descr) * 8) // 2)
        self.oled.text(descr, x, 35)
        self.oled.show()
        
class Charts(Oled):
    def __init__(self, width, heigth, i2c):
        super().__init__(width, heigth, i2c)
   
    def temp_chart(self, record=None):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("temperature", 24, 0)
        self.oled.text(" 0", 0, 52)
        self.oled.text("20", 0, 30)
        self.oled.text("40", 0, 8)
        
        self.oled.hline(16, 34, 3, 1)
        self.oled.hline(16, 8, 3, 1)
        self.oled.hline(8, 60, 128, 1)
        self.oled.vline(17, 8, 56, 1)
        
        if record != None and len(record) != 0:
            self.returnon_pixels(record)
        self.oled.show()
        
    def hum_chart(self, record=None):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("humidity", 40, 0)
        self.oled.text("  0", 0, 52)
        self.oled.text(" 50", 0, 30)
        self.oled.text("100", 0, 8)
        
        self.oled.hline(24, 34, 3, 1)
        self.oled.hline(24, 8, 3, 1)
        self.oled.hline(8, 60, 128, 1)
        self.oled.vline(25, 8, 56, 1)
        
        if record != None and len(record) != 0:
            self.returnon_pixels(record)
        self.oled.show()
        
    def press_chart(self, record=None):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("pressure", 50, 0)
        self.oled.text(" 975", 0, 52)
        self.oled.text("1012", 0, 30)
        self.oled.text("1050", 0, 8)
        
        self.oled.hline(32, 34, 3, 1)
        self.oled.hline(32, 8, 3, 1)
        self.oled.hline(26, 60, 128, 1)
        self.oled.vline(33, 8, 56, 1)
        
        if record != None and len(record) != 0:
            self.returnon_pixels(record)
        self.oled.show()

    def turnon_pixel(self, type_chart, value, xcoord):
        file = ""
        ycoord = 0
        
        if type_chart == "temperature":
            ycoord = 60 - ((26 * value) // 20)
            file = filemanager.Filemanager("data/temperature")
            if xcoord == 128:
                file.erase()
                self.temp_chart()
          
        elif type_chart == "humidity":
            ycoord = 60 - ((26 * value) // 50)
            file = filemanager.Filemanager("data/humidity")
            if xcoord == 128:
                file.erase()
                self.hum_chart()
            
        else:
            perc = ((value - 975) * 100) // 75
            ycoord = 60 - ((26 * perc) // 50)
            file = filemanager.Filemanager("data/pressure")
            if xcoord == 128:
                file.erase()
                self.press_chart()
            
        listoftuple = file.read()
        if len(listoftuple) != 0:
            x, y = listoftuple[-1]
            if y < ycoord and ycoord >= 8:
                for i in range(y, ycoord, 1):
                    file.write(xcoord, i)
                    self.oled.pixel(xcoord, i, 1)
                    
            if y > ycoord and ycoord >= 8:
                for i in range(ycoord, y, 1):
                    file.write(xcoord, i)
                    self.oled.pixel(xcoord, i, 1)
        if ycoord >= 8 and ycoord <= 60:          
            file.write(xcoord, ycoord)           
            self.oled.pixel(xcoord, ycoord, 1)
        self.oled.show()
 
    def returnon_pixels(self, listoftuple):
        for x, y in listoftuple:
            self.oled.pixel(x, y, 1)      
            
             
class Snapshot(Oled):
    def __init__(self, width, heigth, i2c):
        super().__init__(width, heigth, i2c)
    
    def print_name(self, name):
        self.oled.fill(0)
        self.oled.show()
        x = 64 - ((len(name) * 8) // 2) 
        self.oled.text(name, x, 0)
        self.oled.show()
    
    def print_temperature(self, value):
        tstring = "Temp:" + str(value)
        tstring_len = len(tstring) * 8
        self.oled.pixel(tstring_len+2, 16, 1)
        self.oled.pixel(tstring_len+1, 17, 1)
        self.oled.pixel(tstring_len+3, 17, 1)
        self.oled.pixel(tstring_len+2, 18, 1)
        self.oled.text(tstring, 0, 16)
        self.oled.text("C", tstring_len+5, 16)
        self.oled.show()
    
    def print_pressure(self, value):
        pstring = "Pres:" + str(value) + "hPa"
        self.oled.text(pstring, 0, 48)
        self.oled.show()
        
    def print_humidity(self, value):
        hstring = "Umid:" + str(value) + "%"
        self.oled.text(hstring, 0, 32)
        self.oled.show()
        
    def clear_temp(self):
        for i in range(40, 84, 1):
            self.oled.pixel(i, 16, 0)
            self.oled.pixel(i, 17, 0)
            self.oled.pixel(i, 18, 0)
            self.oled.pixel(i, 19, 0)
            self.oled.pixel(i, 20, 0)
            self.oled.pixel(i, 21, 0)
            self.oled.pixel(i, 22, 0)
            self.oled.pixel(i, 23, 0)
        self.oled.show()
        
    def clear_hum(self):
        for i in range(40, 88, 1):
            self.oled.pixel(i, 32, 0)
            self.oled.pixel(i, 33, 0)
            self.oled.pixel(i, 34, 0)
            self.oled.pixel(i, 35, 0)
            self.oled.pixel(i, 36, 0)
            self.oled.pixel(i, 37, 0)
            self.oled.pixel(i, 38, 0)
            self.oled.pixel(i, 39, 0)
        self.oled.show()
        
    def clear_press(self):
        for i in range(40, 112, 1):
            self.oled.pixel(i, 48, 0)
            self.oled.pixel(i, 49, 0)
            self.oled.pixel(i, 50, 0)
            self.oled.pixel(i, 51, 0)
            self.oled.pixel(i, 52, 0)
            self.oled.pixel(i, 53, 0)
            self.oled.pixel(i, 54, 0)
            self.oled.pixel(i, 55, 0)
        self.oled.show()