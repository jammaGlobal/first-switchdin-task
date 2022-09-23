#This will grab all messages currently in the rabbitmq queue with the
# "random-number/averages" topic and display them

# perhaps when these messages are ack'd they should be sent to a different queue
# as a historical log
import json

from tabulate import tabulate
import paho.mqtt.client as mqtt
from Models.TimeRange import TimeRange

def deserialise(T):
    return json.loads(T);

def on_message(client, userdata, msg):
    result = json.loads(msg.payload.decode("utf-8"))
    periodicStats = list(map(deserialise, result['statistics']))
    statsToTabulate = []

    for stat in periodicStats:
        if(stat["timeRange"] == TimeRange.LASTMINUTE.name):
            stat.pop("timeRange")
            statList = list(stat.values())
            statList.insert(0, "last min")
            statsToTabulate.append(statList)
        elif(stat["timeRange"] == TimeRange.LASTFIVEMINUTES.name):
            stat.pop("timeRange")
            statList = list(stat.values())
            statList.insert(0, "last 5 mins")
            statsToTabulate.append(statList)
        else:
            stat.pop("timeRange")
            statList = list(stat.values())
            statList.insert(0, "last 30 mins")
            statsToTabulate.append(statList)

    tableHeaders = ["time window", "avg random number", "avg msgs per minute"]

    print(tabulate(statsToTabulate, tableHeaders, missingval="-", numalign='left', tablefmt="github"), end='\n')



client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_message = on_message
client.subscribe("random-number/average")

try:
    while 1:
        client.loop()

except Exception as e:
    print("Broker connection severed due to: " + str(e))

