"""
Generates random number between and including 1 and 100, and publishes it to specific mqtt topic in rabbitmq,
waits a random interval between and including 1 and 30 seconds and repeats
"""
import sys
import json
import paho.mqtt.client as mqtt
import random
import time
import datetime
from Models.RandomNumber import RandomNumber

# mqtt client config
client = mqtt.Client()
client.connect("localhost", 1883, 60)

try:
    while True:
        randomNumber = random.randint(1, 100)
        timeInterval = random.randint(1, 30)

        randomNumberObj = RandomNumber(randomNumber, str(datetime.datetime.now()), timeInterval)

        # publish random number to client with a quality of service of 0
        client.publish("random-number", json.dumps(randomNumberObj.__dict__), 0)

        # delay interval of a random amount between 1 and 30 seconds
        time.sleep(timeInterval)
except (Exception, KeyboardInterrupt) as e:
    print("Unable to publish due to: " + str(e))
finally:
    client.disconnect()
    sys.exit()
