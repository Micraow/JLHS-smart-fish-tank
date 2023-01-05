
"""
MQTT客户端主体，与HomeAssistant交互，并负责调用Hardware的方法
"""
import time
import paho.mqtt.client as mqtt
from Hardware import temp, oxygen, quality, motor


# mosquitto -p 6000
# 首先启用broker，监听6000端口

MQTTHOST = "127.0.0.1"
MQTTPORT = 6000
mqttClient = mqtt.Client()


def on_mqtt_connect():
    """连接到broker"""
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()


# publish 消息
def on_publish():
    """
    发布温度，含氧量等

    """

    mqttClient.publish("/temp", temp.get())
    mqttClient.publish("/oxygen", oxygen.get())
    mqttClient.publish("/quality", quality.get())

# 消息处理函数


def on_message_come():
    """
    topic: 目前的功能只有投喂(topic=feed)，摄像头转动再说吧
    payload: 投喂ID，防止多次投喂
    解析msg，调用对应的Hardware模块
    """
    motor.feed()


# subscribe 消息
def on_subscribe():
    """订阅HomeAssistant，获取指令"""
    mqttClient.subscribe("/HA-feed")  # HomeAssistant上配置
    mqttClient.on_message = on_message_come  # 消息到来处理函数


def main():
    """主循环"""
    on_mqtt_connect()
    on_subscribe()
    while True:
        on_publish()
        time.sleep(5)  # 等5秒发布一次


if __name__ == '__main__':
    main()
