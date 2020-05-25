# Copyright (c) 2014 Adafruit Industries Author: Tony DiCola for Adafruit Library
#import library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO
import time
import smbus
import math
import smtplib
import sys
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 # Use physical pin numbering
def sendMail(msg):
    smtpUser='test.gyro.sm@gmail.com'
    smtpPass='testac123'
    toAdd='test.gyro.sm@gmail.com'
    fromAdd=smtpUser
    now=datetime.now()
    dt_string=now.strftime("%d-%b-%Y (%H:%M:%S)")
    subject=msg+dt_string
    header='To: '+toAdd+'\n'+'From:'+fromAdd+'\n'+'Subject:'+subject
    body='From within a Python script'
    print (header +'\n'+body)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtpUser,smtpPass)
    server.sendmail(fromAdd,toAdd,header+'\n'+body)
    server.quit()

mode=1
# Power management registers for gyroscope
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
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
# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# setup for button
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#gyro
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command
bus.write_byte_data(address, power_mgmt_1, 0)
padding=-2
top=-2
x=0
font=ImageFont.load_default()

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
#initialize system
mode=1 #1-> Drive mode 2-> Alarm mode
calibrare=0
buzz=18
GPIO.setup(buzz,GPIO.OUT)
# Load image based on OLED display height.  Note that image is converted to 1 bit color.
#if disp.height == 64:
#    image = Image.open('happycat_oled_64.ppm').convert('1')
#else:
#    image = Image.open('happycat_oled_32.ppm').convert('1')

# Alternatively load a different format image, resize it, and convert to 1 bit color.
start=1
while 1: 
    if GPIO.input(15) == GPIO.HIGH:
            print("Button was pushed!")
            if mode==2:
                mode=1
                calibrare=0
                start=1
                time.sleep(0.2)
                
            elif mode==1:
                mode=2
                calibrare=0
                start=1
                time.sleep(0.2)
                
    if mode==2:
        print ('Mode Alarma')
        disp.clear()
        if start ==1:
            start=0
            disp.display()
            img1=Image.open('alarm.png').convert('1')
            disp.image(img1)
            disp.display()
            time.sleep(2)
        if calibrare ==0:
            img1=Image.open('calib.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "-SYSTEM CALIBRATION-",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            time.sleep(1.5)
            gyro_xout = read_word_2c(0x43)
            gyro_yout = read_word_2c(0x45)
            gyro_zout = read_word_2c(0x47)
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            pozX=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            pozY=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            disp.clear()
            img1=Image.open('calib.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "CALIBRATION COMPLETE",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            time.sleep(1)
            disp.clear()
            print ("Calibrare Completa pozX=%2.2f  pozy=%2.2f"%(pozX,pozY))
            calibrare=1
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        newPozX=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        newPozY=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        degX=(pozX-newPozX)*1.125
        degY=(pozY-newPozY)*1.125
        if abs(degX) >10 or abs(degY)>10:
            disp.clear()
            img1=Image.open('atentie.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "DON`T TOUCH GO AWAY!",  font=font, fill=255)
            #draw.text((x, top+6),       "GO AWAY THIEF",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            GPIO.output(buzz, GPIO.HIGH)
            sendMail("The alarm on your motocycle has been activated at ")
            time.sleep(1.5)
            GPIO.output(buzz,GPIO.LOW)
        else:
            disp.clear()
            img1=Image.open('alarm.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "ALARM IS ACTIVATED ",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            
            
        
    elif mode==1:
        print ('Mode Drive')
        disp.clear()
        if start==1:
            start=0
            img1=Image.open('drive.png').convert('1')
            disp.image(img1)
            disp.display()
            time.sleep(1)
        
        if calibrare ==0:
            disp.clear()
            img1=Image.open('calib.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "-SYSTEM CALIBRATION-",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            time.sleep(1.5)
            gyro_xout = read_word_2c(0x43)
            gyro_yout = read_word_2c(0x45)
            gyro_zout = read_word_2c(0x47)
            accel_xout = read_word_2c(0x3b)
            accel_yout = read_word_2c(0x3d)
            accel_zout = read_word_2c(0x3f)
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            pozX=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            pozY=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            disp.clear()
            img1=Image.open('calib.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top),       "CALIBRATION COMPLETE",  font=font, fill=255)
            disp.image(img1)
            disp.display()
            time.sleep(1)
            disp.clear()
            print ("Calibrare Completa pozX=%2.2f  pozy=%2.2f"%(pozX,pozY))
            calibrare=1
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        newPozX=get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        newPozY=get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        degX=(pozX-newPozX)*1.125
        degY=(pozY-newPozY)*1.125
        img1=Image.open('newMotoF3.png').convert('1')
        img2=Image.open('newMotoL2.png').convert('1')
        if abs(degX) >1:
            img1=img1.rotate(degX)
        if abs(degY) >1:
            img2=img2.rotate(degY)
        
        disp.clear()
        
        img=get_concat_h(img1, img2)
        image=img.resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    #image = Image.open('motocombo.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1'Dra
        if abs(degX)>80 or abs(degY)>80:
            img1=Image.open('atentie.png').convert('1')
            draw=ImageDraw.Draw(img1)
            draw.text((x, top), "!  DANGER  GET  UP  !" ,  font=font, fill=255)
            disp.image(img1)
            disp.display()
            GPIO.output(buzz,GPIO.HIGH)
            sendMail("The driver of the Motocycle has fallen at ")
            time.sleep(1)
            GPIO.output(buzz,GPIO.LOW)
        else:
            
            draw=ImageDraw.Draw(image)
            if degX>0 :
                str1="< %2.2f"%(abs(degX))
            else:
                str1="> %2.2f"%(abs(degX))
            if degY>0 :
                str2="^ %2.2f"%(abs(degY))
            else:
                str2="v %2.2f"%(abs(degY))
            draw.text((x, top), str1+"       "+str2 ,  font=font, fill=255)
            disp.image(image)
            disp.display()
        
        
    
    #image = Image.open('moto-face.png').convert('1')
    #disp.image(image)
    

