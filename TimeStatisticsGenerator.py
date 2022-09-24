"""
Sets up mqtt client to subscribe to the same topic that RandomNumberGenerator publishes to. On message event collects message
with random number inside, at every minute calculates sum of values divided by total of numbers, at every 5 and 30 minutes
calculates sum of values divided by minutes passed, publishes these calculations to different mqtt topic
"""
import sys
import json
import paho.mqtt.client as mqtt
import schedule

from Models.StatisticsResource import StatisticsResource
from Models.TimeRange import TimeRange

currentMinute = []
lastFiveMinutes = []
lastThirtyMinutes = []

# minuteCounter is not "determining" the time at which to calculate averages,
# only used to determine what "type" of calculation is needed
minuteCounter = 0

# callback for message event
def on_message(client, userdata, msg):
    result = json.loads(msg.payload.decode("utf-8"))
    currentMinute.append(result['value'])

# lists are passed by reference
# This function will calculate and send the average random number value for the last Minute, 5 Minute block AND 30 Minute block
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
        client.publish("random-number/average", calculateStatisticsToSend(currentMinute.copy(), TimeRange.LASTMINUTE, minuteCounter), 0)

        if(period == TimeRange.LASTFIVEMINUTES):
            client.publish("random-number/average", calculateStatisticsToSend(lastFiveMinutes, period, minuteCounter), 0)
            lastFiveMinutes.clear()

        if(period == TimeRange.LASTTHIRTYMINUTES):
            client.publish("random-number/average", calculateStatisticsToSend(lastFiveMinutes, TimeRange.LASTFIVEMINUTES, minuteCounter), 0)
            client.publish("random-number/average", calculateStatisticsToSend(lastThirtyMinutes, period, minuteCounter), 0)
            lastFiveMinutes.clear()
            lastThirtyMinutes.clear()

        currentMinute.clear()

# calculates average for list of random numbers and constructs an object which is then serialised to json
def calculateStatisticsToSend(messageList, timeRange, minuteCounter):
    if(timeRange == TimeRange.LASTMINUTE):
        return json.dumps(StatisticsResource(sum(messageList) / len(messageList), timeRange.name, minuteCounter).__dict__)

    if(timeRange == TimeRange.LASTFIVEMINUTES or timeRange == TimeRange.LASTTHIRTYMINUTES):
        return json.dumps(StatisticsResource(sum(sum(x) for x in messageList) / len(messageList),
                                  (timeRange.name), minuteCounter).__dict__)

# mqtt client config
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_message = on_message
client.subscribe("random-number")

def listenForMessages():
    client.loop()

# A scheduled job will run every 60 seconds to caculate and send random number average(s)
# another job runs every second which loops the mqtt client to listen for publish message events
schedule.every(60).seconds.do(calcAndSendAverage, currentMinute, lastFiveMinutes,
                              lastThirtyMinutes)
schedule.every().second.do(listenForMessages)

try:
    while True:
        schedule.run_pending()
except KeyboardInterrupt as e:
    print("statistics generator exited")
except Exception as e:
    print("Broker connection severed due to: " + str(e))
finally:
    client.disconnect()
    schedule.clear()
    sys.exit()