import json

import paho.mqtt.client as mqtt
import schedule
from datetime import datetime
from Models.StatisticsResource import StatisticsResource
from Models.TimeRange import TimeRange
from Models.RandomNumber import RandomNumber

msgHistory = []
lastMinute = []
currentMinute = []
lastFiveMinutes = []
lastThirtyMinutes = []
minuteCounter = 0

timestamps = []

#callback for message event
def on_message(client, userdata, msg):
    # print("-------------Message received! Payload: "+ str(msg.payload.decode("utf-8")))
    msgDateTime = datetime.fromtimestamp(msg.timestamp)
    timestamps.append(msgDateTime)  # float

    result = json.loads(msg.payload.decode("utf-8"))
    currentMinute.append(result['value'])
    msgHistory.append(RandomNumber(result['value'], result['timeOfGeneration'], result['secondsUntilNextNumberGen']))

# lists are passed by reference
# This function will calculate and send the average random number value for the last Minute, 5 Minutes AND 30 Minutes
# (the latter two only when those time ranges have elapsed).
def calcAndSendAverage(currentMinute, lastFiveMinutes, lastThirtyMinutes):

    global minuteCounter
    minuteCounter += 1

    if(minuteCounter % 30 == 0):
        period = TimeRange.LASTTHIRTYMINUTES
    elif(minuteCounter % 5 == 0):
        period = TimeRange.LASTFIVEMINUTES
    else:
        period = TimeRange.LASTMINUTE

    if(len(currentMinute) != 0):
        lastFiveMinutes.append(currentMinute.copy())
        lastThirtyMinutes.append(currentMinute.copy())
        print("1 Min: "+str(currentMinute))
        print("5 Min: "+str(lastFiveMinutes))
        print("30 Min: "+str(lastThirtyMinutes))
        statsToPublish = json.dumps(calculateStatistics(currentMinute.copy(), TimeRange.LASTMINUTE, minuteCounter).__dict__)
        client.publish("random-number/average", statsToPublish, 0)

        if(period == TimeRange.LASTFIVEMINUTES):
            statsToPublish = json.dumps(calculateStatistics(lastFiveMinutes, period, minuteCounter).__dict__)
            client.publish("random-number/average", statsToPublish, 0)
            lastFiveMinutes.clear()

        if(period == TimeRange.LASTTHIRTYMINUTES):
            statsToPublish = json.dumps(calculateStatistics(lastFiveMinutes, TimeRange.LASTFIVEMINUTES, minuteCounter).__dict__)
            client.publish("random-number/average", statsToPublish, 0)
            statsToPublish = json.dumps(calculateStatistics(lastThirtyMinutes, period, minuteCounter).__dict__)
            client.publish("random-number/average", statsToPublish, 0)
            lastFiveMinutes.clear()
            lastThirtyMinutes.clear()

        currentMinute.clear()


def calculateStatistics(messageList, timeRange, minuteCounter):
    if(timeRange == TimeRange.LASTMINUTE):
        return StatisticsResource(sum(messageList) / len(messageList), timeRange.name, minuteCounter)

    if(timeRange == TimeRange.LASTFIVEMINUTES or timeRange == TimeRange.LASTTHIRTYMINUTES):
        return StatisticsResource(sum(sum(x) for x in messageList) / len(messageList),
                                  (timeRange.name), minuteCounter)

# mqtt client config
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_message = on_message
client.subscribe("random-number")

def listenForMessages():
    client.loop()

schedule.every(60).seconds.do(calcAndSendAverage, currentMinute, lastFiveMinutes,
                              lastThirtyMinutes)
schedule.every().second.do(listenForMessages)

try:
    while True:
        schedule.run_pending()
except Exception as e:
    print("Broker connection severed due to: " + str(e.with_traceback()))