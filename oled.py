from ssd1306 import SSD1306_I2C

class Oled:
    def __init__(self, width, heigth, i2c):
        self.oled = SSD1306_I2C(width, heigth, i2c)
        
    def clear(self):
        self.oled.fill(0)
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

class Charts(Oled):
    def __init__(self, width, heigth, i2c):
        super().__init__(width, heigth, i2c)
    
    def generic_chart(self, name, ypoints=None, valuelist=None):
        self.oled.fill(0)
        self.oled.show()
        
        x = 64 - ((len(name) * 8) // 2) 
        self.oled.text(name, x, 0)
        
        if ypoints != None and valuelist != None:
            max_len = 0
            for i in valuelist:
                if len(i) > max_len:
                    max_len = len(i)
            max_len *= 8
            self.oled.vline(max_len+1, 8, 56, 1)
            self.oled.hline(max_len-4, 60, 128, 1)
            
            y = 60 // ypoints
            adder = 0
            for i in range(ypoints - 1):
                self.oled.hline(max_len, y+adder-5, 3, 1)
                adder += y
            
            ytext = 52
            for i in valuelist:
                self.oled.text(i, 0, ytext)
                ytext -= y
        else:
            self.oled.hline(0, 60, 128, 1)
            self.oled.vline(4, 8, 56, 1) 
        self.oled.show()     
    
    def temp_chart(self):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("temperature", 24, 0)
        self.oled.text(" 0", 0, 52)
        self.oled.text("20", 0, 30)
        self.oled.text("40", 0, 8)
        
        self.oled.hline(16, 34, 3, 1)
        self.oled.hline(16, 12, 3, 1)
        self.oled.hline(8, 60, 128, 1)
        self.oled.vline(17, 8, 56, 1)
        self.oled.show()
        
    def hum_chart(self):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("humidity", 40, 0)
        self.oled.text("  0", 0, 52)
        self.oled.text(" 50", 0, 30)
        self.oled.text("100", 0, 8)
        
        self.oled.hline(24, 34, 3, 1)
        self.oled.hline(24, 12, 3, 1)
        self.oled.hline(8, 60, 128, 1)
        self.oled.vline(25, 8, 56, 1)
        self.oled.show()
        
    def press_chart(self):
        self.oled.fill(0)
        self.oled.show()
        self.oled.text("pressure", 50, 0)
        self.oled.text(" 975", 0, 52)
        self.oled.text("1025", 0, 30)
        self.oled.text("1050", 0, 8)
        
        self.oled.hline(32, 34, 3, 1)
        self.oled.hline(32, 12, 3, 1)
        self.oled.hline(26, 60, 128, 1)
        self.oled.vline(33, 8, 56, 1)
        self.oled.show()
        
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
