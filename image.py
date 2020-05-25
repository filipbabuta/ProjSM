# Copyright (c) 2014 Adafruit Industries Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
def get_concat_h(im1, im2):
    dst = Image.new('L', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0



# Get drawing object to draw on image.



# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

padding=-2
top=-2
x=0
font=ImageFont.load_default()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
i=90
# Load image based on OLED display height.  Note that image is converted to 1 bit color.
#if disp.height == 64:
#    image = Image.open('happycat_oled_64.ppm').convert('1')
#else:
#    image = Image.open('happycat_oled_32.ppm').convert('1')

# Alternatively load a different format image, resize it, and convert to 1 bit color.
while 1: 
    
    disp.clear()
    img1=Image.open('newMotoF3.png').convert('1')
    img2=Image.open('newMotoL2.png').convert('1')
    img=get_concat_h(img1.rotate(0), img2.rotate(0))
    image=img.resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    #image = Image.open('motocombo.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    draw=ImageDraw.Draw(image)
    draw.text((x, top),       "IP: " + str(123.5)+str(i),  font=font, fill=255)
    disp.image(image)
    disp.display()
    i=i+90
    time.sleep(3)
    
    #image = Image.open('moto-face.png').convert('1')
    #disp.image(image)
    
