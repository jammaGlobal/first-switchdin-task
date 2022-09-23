FROM rabbitmq:3.8.3-alpine

ENV RABBITMQ_VERSION=3.8.3

RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt
RUN rabbitmq-plugins enable --offline rabbitmq_web_mqtt

EXPOSE 15675
EXPOSE 1883
EXPOSE 15672
