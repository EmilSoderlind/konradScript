import RPi.GPIO as GPIO
from gpiozero import LED
import time
import konradTweet
import rotatePic90
import sys, os
import datetime
import sys, traceback


print("Starting Konrad Hallonpaj")

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
print("Starting in 5 sec.")

for t in range(0,5):
	print(t)
	time.sleep(0.5)
	GPIO.output(17,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(17,GPIO.LOW)

def mainLoop():
	time.sleep(0.02)
	print("Waiting for mail.")
	input_state = GPIO.input(18)
	GPIO.output(17,GPIO.LOW)
	if(input_state == True):
            print('Curcuit broken')
            GPIO.output(17,GPIO.HIGH)
            time.sleep(0.7)
            input_state = GPIO.input(18)
            if(input_state == True):
                print("Mail arrived. Take photo in 3 sec.")
                print("Take photo")
                rotatePic90.takePhoto()
                print("Take photo - DONE")
                print("Post tweet")
                konradTweet.konradTweet()
                print("Post tweet - DONE")
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
                GPIO.setup(17,GPIO.OUT)
                GPIO.output(17,GPIO.HIGH)
                print("Sover i 3 sek")
                time.sleep(3)

logf = open("errorOut.txt", "w")
while True:
	try:
		mainLoop()
	except Exception as e:     # most generic exception you can catch
		now = datetime.datetime.now()
		logf.write("ERROR! {0}: {1}\n".format(str(now),str(e)))
		print("ERROR! {0}: {1}\n".format(str(now),str(e)))
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		time.sleep(10)
