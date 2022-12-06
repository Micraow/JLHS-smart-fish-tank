import sys
sys.path.append("..")

from controller.act import *
import main
from fastapi_mqtt.fastmqtt import FastMQTT

from fastapi_mqtt.config import MQTTConfig

def run():
    app = main.app

    mqtt_config = MQTTConfig()

    mqtt = FastMQTT(config=mqtt_config)

    mqtt.init_app(app)

    @mqtt.on_connect()
    def connect(client, flags, rc, properties):
        mqtt.client.subscribe("/HA-food") #subscribing homeassistant food command
        print("Connected: ", client, flags, rc, properties)

    @mqtt.on_message()
    async def message (topic):
        if topic=="/HA-food":
            act.food()
        return 0


    @mqtt.on_disconnect()
    def disconnect():
        print("Disconnected")

    @mqtt.on_subscribe()
    def subscribe(client, mid, qos, properties):
        print("subscribed", client, mid, qos, properties)


