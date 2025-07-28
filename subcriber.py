import paho.mqtt.client as mqtt
import asyncio


class Subscriber:

    def __init__(self, broker):
        self.broker = broker

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print(f"Failed to connect: {rc}")

    def on_message(self, client, userdata, message):
        print(message.payload.decode("utf-8"))

    def on_message_txt(self, client, userdata, message):
        with open("Recieved.txt", "w") as f:
            f.write(message.payload.decode("utf-8"))
        print("File Saved")


    ##Recieving String
    async def get_string(self, topic):
        client = mqtt.Client()
        try:
            while(True):
                client.on_connect = self.on_connect
                client.on_message = self.on_message
                client.connect(self.broker, 1883, 60)
                client.loop_start()
                client.subscribe(topic)

                await asyncio.sleep(60)

        except Exception as e:
            print(e)

        finally:
            client.loop_stop()
            client.disconnect()

    ##Recieving txt file
    async def get_txt(self, topic):
        client = mqtt.Client()
        try:
            while(True):
                client.on_connect = self.on_connect
                client.on_message = self.on_message_txt
                client.connect(self.broker, 1883, 60)
                client.loop_start()
                client.subscribe(topic)

                await asyncio.sleep(60)

        except Exception as e:
            print(e)

        finally:
            client.loop_stop()
            client.disconnect()


async def main():
    broker = "broker.hivemq.com"
    string_topic = "testmee/string"
    txt_topic = "testmee/txt"
    device = Subscriber(broker)

    await asyncio.gather(device.get_txt(txt_topic), device.get_string(string_topic))


if __name__ == "__main__":
    asyncio.run(main())