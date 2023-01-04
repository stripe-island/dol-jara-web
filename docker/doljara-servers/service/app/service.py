import os
import json

from paho.mqtt import client
import redis


class Service():

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "1883"))

    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "6379"))

    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


    def __init__(self):

        def on_connect(client, userdata, flags, rc):

            print("Connected with result code " + str(rc))


        def on_message(client, userdata, msg):

            if msg.topic == "rooms/show":
                self.__show_rooms()
            else:
                pass


        self.__client = client.Client()

        self.__client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)

        self.__client.on_connect = on_connect
        self.__client.on_message = on_message


    def run(self):

        self.__redis = redis.Redis(self.REDIS_HOST, self.REDIS_PORT, decode_responses = True)


        self.__client.connect(self.MQTT_BROKER_HOST, self.MQTT_BROKER_PORT)


        self.__client.subscribe("rooms/show")


        self.__client.loop_forever()



    def __show_rooms(self):

        payload = dict()

        payload["rooms"] = self.__redis.keys()

        self.__client.publish("rooms", json.dumps(payload, ensure_ascii = False))



if __name__ == "__main__":

    service = Service()
    service.run()

