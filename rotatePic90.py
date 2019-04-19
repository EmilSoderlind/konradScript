# coding=utf-8

from fractions import Fraction
import picamera
from PIL import Image
import time
import RPi.GPIO as GPIO

def takePhoto():
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
    
    #camera.framerate = Fraction(1, 6)
    #time.sleep(5)
    #camera.shutter_speed = 6000000
    camera.exposure_mode = 'night'
    #camera.iso = 800
    #camera.awb_mode = 'night'
    #print camera.awb_gains
    #camera.awb_gains = (1.0, 1.0)
    # Camera warm-up time
    camera.start_preview()
    # STARTA LAMPA
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21,GPIO.HIGH)
    time.sleep(5)

    standardName = "mailImage.jpg"
    rotatedName = "rotatedMailImage.jpg"

    camera.capture(standardName)
    camera.stop_preview()
    # STÄNG LAMPA
    GPIO.cleanup()
    print("Photo taken")
    camera.close()
    img = Image.open(standardName)
    img2 = img.rotate(-180)
    img2.save(rotatedName)
    time.sleep(1)
    print("Photo rotated")
    img.close()
    img2.close()
