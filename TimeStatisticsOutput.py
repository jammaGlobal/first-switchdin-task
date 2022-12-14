"""
Mqtt client subscribes to the same topic that TimeStatisticsGenerator publishes to. On message event collects message
with averages and the relative minute the calculation was made, prints these results in continuous tabular form in the console
"""
import sys
import json
import paho.mqtt.client as mqtt

from prettytable import PrettyTable
from Models.TimeRange import TimeRange

print("[ Random Number Averages Output ]")
print("[ processing .... ]")
print(" ")
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
except KeyboardInterrupt as e:
    print("table output exited")
except Exception as e:
    print("Broker connection severed due to: " + str(e))
finally:
    client.disconnect()
    sys.exit()

