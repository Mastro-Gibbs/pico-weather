class Filemanager:
    def __init__(self, filename):
        self.filename = filename
        
    def erase(self):
        file = open(self.filename, "w")
        file.close()
        
    def write(self, xcoord, ycoord):
        coords = str(xcoord) + "," + str(ycoord) + "\n"
        file = open(self.filename, "a")
        file.write(coords)
        file.close()
        
    def read(self):
        coords = []
        
        file = open(self.filename, "r")
        lines = file.readlines()
        file.close()
        
        for line in lines:
            line = "{}".format(line.strip())
            index = line.find(",")
            xcoord = line[0:index]
            ycoord = line[index+1:]
            coords.append((int(xcoord), int(ycoord)))
        
        return coords
