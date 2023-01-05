
"""
MQTT客户端主体，与HomeAssistant交互，并负责调用Hardware的方法
"""
import paho.mqtt.client as mqtt

#mosquitto -p 6000
#首先启用broker，监听6000端口

MQTTHOST = "127.0.0.1"
MQTTPORT = 6000
mqttClient = mqtt.Client()


def on_mqtt_connect():
    """连接到broker"""
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()


# publish 消息
def on_publish(topic, payload):
    """
    :param topic: 目前的功能只有投喂(topic=feed)，摄像头转动再说吧
    :param payload: 生成随机令牌，防止多次投喂
    """
    mqttClient.publish(topic, payload)

# 消息处理函数


def on_message_come(msg):

    """解析msg，调用对应的Hardware模块"""

    print(msg.topic + " " + ":" + str(msg.payload))


# subscribe 消息
def on_subscribe():
    """订阅HomeAssistant，获取指令"""
    mqttClient.subscribe("/HA")  # HomeAssistant上配置
    mqttClient.on_message = on_message_come  # 消息到来处理函数


def main():
    """主循环"""
    on_mqtt_connect()
    on_publish("/test/server", "Hello Python!")
    on_subscribe()
    while True:
        pass


if __name__ == '__main__':
    main()
