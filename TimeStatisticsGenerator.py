import json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import sched, time
from datetime import datetime
from Models.StatisticsResource import StatisticsResource
from Models.TimeRange import TimeRange
from Models.RandomNumber import RandomNumber
from Models.PeriodicStatistics import PeriodicStatistics

msgHistory = []
lastMinute = []
currentMinute = []
lastFiveMinutes = []
lastThirtyMinutes = []

timestamps = []

#callback for message event
def on_message(client, userdata, msg):
    print("Payload: " + str(msg.payload.decode("utf-8")))
    yeah = msg.payload.decode("utf-8")

    msgTime = msg.timestamp
    msgDateTime = datetime.fromtimestamp(msgTime)
    timestamps.append(msgDateTime)  # float

    result = json.loads(msg.payload.decode("utf-8"))
    currentMinute.append(result['value'])
    msgHistory.append((result['value'], result['timeOfGeneration'], result['secondsUntilNextNumberGen']))

# This function will calculate the average random number value AND average amount of
# messages for the LAST Minute, 5 Minutes, AND 30 Minutes. Until 5 minutes has elapsed, the 5 minute averages will be null,
# same for the 30 minute averages
def getAverages(currentMinute, lastFiveMinutes, lastThirtyMinutes):

    updateMessageList(lastFiveMinutes, TimeRange.LASTFIVEMINUTES, currentMinute)
    updateMessageList(lastThirtyMinutes, TimeRange.LASTTHIRTYMINUTES, currentMinute)

    statsToPublish = PeriodicStatistics([json.dumps(calculateStatistics(currentMinute, TimeRange.LASTMINUTE).__dict__),
                                         json.dumps(calculateStatistics(lastFiveMinutes, TimeRange.LASTFIVEMINUTES).__dict__),
                                         json.dumps(calculateStatistics(lastThirtyMinutes, TimeRange.LASTTHIRTYMINUTES).__dict__)])

    client.publish("random-number/average", json.dumps(statsToPublish.__dict__), 0)

#Removes the oldest minute of the messages lists to keep it within the last 5 or 30 minutes that have passed
def updateMessageList(messageList, timeRange, currentMinute):
    if (timeRange == TimeRange.LASTTHIRTYMINUTES):
        yeah = 1

    if ((len(messageList) == 5 and timeRange == TimeRange.LASTFIVEMINUTES) or (len(messageList) == 30 and timeRange == TimeRange.LASTTHIRTYMINUTES)):
        messageList.pop(0)

    messageList.append(currentMinute)
    return messageList

def calculateStatistics(messageList, timeRange):
    if(timeRange==TimeRange.LASTTHIRTYMINUTES):
        yeah =1

    #the message rate / avg messages per minute for one minute is useless information
    if(len(messageList) == 0 and timeRange == TimeRange.LASTMINUTE):
        return StatisticsResource(0, None, timeRange.LASTMINUTE)

    if(timeRange == TimeRange.LASTMINUTE):
        return StatisticsResource(sum(messageList) / len(messageList), None, timeRange.name)

    #   When 5 minutes or 30 minutes hasn't elapsed we can't calculate what the averages are for those time ranges
    if((len(messageList) < 30 and timeRange == TimeRange.LASTTHIRTYMINUTES) or (len(messageList) < 5 and timeRange == TimeRange.LASTFIVEMINUTES)):
        return StatisticsResource(None, None, timeRange.name)
    else:
        return StatisticsResource(sum(sum(x) for x in messageList) / len(messageList),
                                  (len([item for items in messageList for item in items]) / timeRange.value),
                                  (timeRange.name))

# mqtt client config
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_message = on_message
client.subscribe("random-number")

try:
    now = time.monotonic()
    while 1:
        client.loop()
        if(time.monotonic() - now > 60.00):
            print(str(msgHistory))
            getAverages(currentMinute, lastFiveMinutes, lastThirtyMinutes)
            lastMinute = currentMinute
            currentMinute = []
            now = time.monotonic()

except Exception as e:
    print("Broker connection severed due to: " + str(e))
