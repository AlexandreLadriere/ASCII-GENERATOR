from PIL import Image, ImageDraw, ImageFont
import math
import argparse

def getChar(inputValue, chars):
    """ 
    Return a character in the given char list, according to the given input value

    Parameters
    ----------
    inputValue : float
        Value you want to tranform to char
    chars : str
        List of chars you will use to select a char to represent the input value
    """
    charArray = list(chars)
    interval = len(charArray)/256
    return charArray[math.floor(inputValue*interval)]


def transformImage(inputImgPath, outputImgPath, scaleFactor, chars):
    """
    Load the given image, transform it to an ascii image and save it

    Parameters
    ----------
    inputImg : str
        Path of the image you want to use
    outputImg : str
        Path of the output image you want to save
    scaleFactor : float
        scale factor for the ouput image
    chars : str
        String of all the char you want to use for your transformation
    """
    charWidth = 10
    charHeight = 10
    im = Image.open(inputImgPath)
    width, height = im.size
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(charWidth/charHeight))), Image.NEAREST)
    pix = im.load()
    widthResized, heightResized = im.size
    outputImg = Image.new('RGB', (charWidth * widthResized, charHeight * heightResized), color = (0, 0, 0))
    drawImg = ImageDraw.Draw(outputImg)
    for i in range(heightResized):
        for j in range(widthResized):
            r, g, b = pix[j, i]
            avg = int(r/3 + g/3 + b/3)
            pix[j, i] = (avg, avg, avg)
            drawImg.text((j*charWidth, i*charHeight), getChar(avg, chars), fill = (r, g, b))
    outputImg.save(outputImgPath)

def main(inPath, outPath, scaleFactor):
    charsValues = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1] #order by density desc
    transformImage(inPath, outPath, scaleFactor, charsValues)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'ASCII Image Generator',
                                     description = 'Generate an ASCCI representation of the given image')
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        required=True,
                        help='Path (str) of the original image')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        required=True,
                        help='Path (str) where you want the script to save the transformed image')
    parser.add_argument('-s',
                        '--scale',
                        type=float,
                        required=False,
                        default=0.5,
                        help='Scale factor between the original image and the transformed image')
    args = parser.parse_args()
    main(args.input, args.output, args.scale)
    