import sys
sys.path.append("..")
import main
from fastapi_mqtt.fastmqtt import FastMQTT

from fastapi_mqtt.config import MQTTConfig

mqtt_config = MQTTConfig()

mqtt = FastMQTT(config=mqtt_config)
app=main.app
mqtt.init_app(app)

async def temp(data):
    mqtt.publish("/HA-temp", data) #publishing mqtt topic

    return {"result": True,"message":"Published" }

async def oxygen(data):
    mqtt.publish("/HA-oxygen", data) #publishing mqtt topic

    return {"result": True,"message":"Published" }

async def temp(data):
    mqtt.publish("/HA-quality", data) #publishing mqtt topic

    return {"result": True,"message":"Published" }

