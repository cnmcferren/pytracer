class Image():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(self.width)] for _ in range(self.height)]

    def setPixel(self, x, y, color):
        self.pixels[y][x] = color

    @staticmethod
    def writePPMHeader(imgFile, height=None, width=None):
        imgFile.write("P3 {} {}\n255\n".format(width, height))

    def writePPM(self, imgFile):
        Image.writePPMHeader(imgFile, height=self.height, width=self.width)
        self.writePPMRaw(imgFile)

    def writePPMRaw(self, imgFile):
        def toBytes(c):
            return round(max(min(c * 255, 255), 0))

        for row in self.pixels:
            for color in row:
                imgFile.write("{} {} {} ".format(toBytes(color.x),
                                                toBytes(color.y),
                                                toBytes(color.z)
                                                ))
            imgFile.write("\n")