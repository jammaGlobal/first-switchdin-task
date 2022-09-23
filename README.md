pip install paho-mqtt
pip install tabulate

- write random number generator

run the rabbitmq locally

docker build -t myrabbitmq .

docker run -d -p 1883:1883 -p 15675:15675 -p 15672:15672 --hostname my-rabbit --name some-rabbit myrabbitmq