import os
from PIL import Image, ImageOps

f = Image.open('./tests/thumbnail.jpg').convert('L')
f.save('./tests/thumbgrey.png')


'''
def tint_image(src, color="#FFFFFF"):
    src.load()
    #r, g, b, alpha = src.split()
    gray = ImageOps.grayscale(src)
    gray = ImageOps.autocontrast(gray)
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    #result.putalpha(alpha)
    return result
'''

tinted = ImageOps.colorize(f, black='#1e1a12', white='#bfb196')

#tinted = tint_image(f, "#704214")
tinted.save('./tests/thumbtint.png')