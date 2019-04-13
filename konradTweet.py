#!/usr/bin/python
import time;
from twython import Twython
import averageTimesFromKonrad
import os, errno
import subprocess
import twitterAPIinformation

APP_KEY = twitterAPIinformation.APP_KEY
APP_SECRET = twitterAPIinformation.APP_SECRET
OAUTH_TOKEN = twitterAPIinformation.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = twitterAPIinformation.OAUTH_TOKEN_SECRET


def konradTweet():
    
    #Updating local json-file
    print("Trying to log time in json-file")
    subprocess.call('sudo node /home/pi/Desktop/konradAPI/updateFileWithCurrentTime.js /home/pi/Desktop/konradAPI/resultData.json &', shell=True)
    print("Trying to log time in json-file - DONE")

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    localtime = time.localtime(time.time())
    print(localtime)

    min = localtime.tm_hour
    sec = localtime.tm_min

    if(min<10):
        min = "0{}".format(min)
    if(sec<10):
        sec = "0{}".format(sec)

    #mess = "Posten har kommit! {}:{}. {} #nukommerpostenkonrad".format(min,sec,averageTimesFromKonrad.getConfIntervString())
    mess = "Posten har kommit! {}:{}.".format(min,sec)

    photo = open('rotatedMailImage.jpg', 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status=mess, media_ids=[response['media_id']])
    time.sleep(1)
    photo.close()
    #silentremove('/home/pi/Desktop/konradScript/rotatedMailImage.jpg')
    #print("Removed picture.")
