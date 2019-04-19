from TwitterSearch import *
import twitterAPIinformation

import numpy as np
import scipy.stats as st
#import matplotlib.pyplot as plt

# returns confidence interval of mean
def confIntMean(a, conf=0.95):
    mean, sem, m = np.mean(a), st.sem(a), st.t.ppf((1+conf)/2., len(a)-1)
    return mean - m*sem, mean + m*sem

#Convert sec from 00:00 to timetuple ex. (12,04)
def secToTimeString(s):

    averageHours = int(s/(60*60))
    averageMinute = int((s-(averageHours*60*60))/60)

    if(averageMinute<10):
        averageMinute = "0{}".format(averageMinute)

    return (averageHours, averageMinute)

#Parse tweets from konrad, return posting times (in sec from 00:00) in array.
def extractAverageSecFromTweets():

    timesSinceMidnightArray = []
    try:
        tuo = TwitterUserOrder('KonradHallonpaj') # create a TwitterUserOrder

        #tso.set_keywords(['#nukommerpostenkonrad']) # let's define all words we would like to have a look for
        #tso.set_language('en') # we want to see German tweets only
        #tso.set_include_entities(True) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
                consumer_key = twitterAPIinformation.APP_KEY
                consumer_secret = twitterAPIinformation.APP_SECRET
                access_token = twitterAPIinformation.OAUTH_TOKEN
                access_token_secret = twitterAPIinformation.OAUTH_TOKEN_SECRET
        )

        # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tuo):
            hourString = tweet['text'][19:21]
            minString = tweet['text'][22:24]
            secSinceMidnight = (int(hourString)*60*60)+(int(minString)*60)
            #print(hourString,minString,secSinceMidnight)
            timesSinceMidnightArray.append(secSinceMidnight)
            #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

        return timesSinceMidnightArray
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

def getConfIntervString():
    a = extractAverageSecFromTweets()
    startHour = secToTimeString(int(confIntMean(a)[0]))[0]
    startMin = secToTimeString(int(confIntMean(a)[0]))[1]
    endHour = secToTimeString(int(confIntMean(a)[1]))[0]
    endMin = secToTimeString(int(confIntMean(a)[1]))[1]

    return "Posten kommer med 95% sannolikhet mellan {}:{} och {}:{}.".format(startHour,startMin,endHour,endMin)

def getAverageTimeString():
    # Array with sec since 00:00
    arr = extractAverageSecFromTweets()
    averageSecSinceMid = int(sum(arr)/len(arr))
    return secToTimeString(averageSecSinceMid)

def plotTimes():
    arr = extractAverageSecFromTweets()
    plt.plot(arr,'ro')
    plt.ylabel('Sec since 00:00')
    plt.show()


#print(getConfIntervString())
#print(getAverageTimeString())
#plotTimes()
