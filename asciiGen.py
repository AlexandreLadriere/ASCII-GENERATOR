from PIL import Image, ImageDraw, ImageFont
import math

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1] #order by density desc
charArray = list(chars)
charLength = len(charArray)
interval = charLength/256
scaleFactor = 0.5
charWidth = 10
charHeight = 18

def getChar(inputValue):
    return charArray[math.floor(inputValue*interval)]

im = Image.open("img/sch.jpg")
width, height = im.size

im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(charWidth/charHeight))), Image.NEAREST)
width, height = im.size
pix = im.load()

outputImg = Image.new('RGB', (charWidth * width, charHeight * height), color = (0, 0, 0))
drawImg = ImageDraw.Draw(outputImg)


for i in range(height):
    for j in range(width):
        r, g, b = pix[j, i]
        avg = int(r/3 + g/3 + b/3)
        pix[j, i] = (avg, avg, avg)
        drawImg.text((j*charWidth, i*charHeight), getChar(avg), fill = (r, g, b))

outputImg.save("img/result.png")