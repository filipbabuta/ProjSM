import RPi.GPIO as GPIO
import time

        

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
mode=1
while True:
        if GPIO.input(10) == GPIO.HIGH:
            print("Button was pushed!")
            if mode==2:
                
                mode=1
                time.sleep(0.2)
           
            elif mode==1:
                mode=2
                time.sleep(0.2)
        if mode==2:
            print ('Mode Alarma')
        elif mode==1:
            print ('Mode Drive')
           
            
                