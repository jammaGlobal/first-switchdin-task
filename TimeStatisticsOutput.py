import json

import paho.mqtt.client as mqtt
from prettytable import PrettyTable
from Models.TimeRange import TimeRange

table = PrettyTable(['time period          ','random number average'])
table.align['time period          '] = 'l'
table.align['random number average'] = 'l'
table.hrules = 1

def deserialise(T):
    return json.loads(T);

def on_message(client, userdata, msg):
    result = json.loads(msg.payload.decode("utf-8"))
    printTable(result)

def printTable(result):
    avg = "{:.2f}".format(result["randomNumberAverage"])

    if (result["timeRange"] == TimeRange.LASTMINUTE.name):
        table.add_row(['minute ' + str(result["minute"]), avg])
        if (result["minute"] == 1):
            print(table)
        else:
            print("\n".join(table.get_string().splitlines()[-2:]))

    elif (result["timeRange"] == TimeRange.LASTFIVEMINUTES.name):
        table.add_row(['LAST 5 MIN BLOCK', avg])
        print("\n".join(table.get_string().splitlines()[-2:]))
    else:
        table.add_row(['LAST 30 MIN BLOCK', avg])
        print("\n".join(table.get_string().splitlines()[-2:]))

# mqtt client config
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.on_message = on_message
client.subscribe("random-number/average")

try:
    while 1:
        client.loop()
except Exception as e:
    print("Broker connection severed due to: " + str(e))
finally:
    client.disconnect()

