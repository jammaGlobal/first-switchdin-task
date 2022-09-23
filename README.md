pip install paho-mqtt
pip install tabulate
pip install timeloop

- write random number generator

run the rabbitmq locally

docker build -t myrabbitmq .

docker run -d -p 1883:1883 -p 15675:15675 -p 15672:15672 --hostname my-rabbit --name some-rabbit myrabbitmq

Only one periodic task as schedule has no priority for jobs and multiple periodic tasks that over lap such as in this 
situation need to run in a certain sequence 