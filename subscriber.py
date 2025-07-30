import paho.mqtt.client as mqtt
import asyncio
import publisher

class Subscriber:

    def __init__(self, broker, loop):
        self.broker = broker
        self.publisher = publisher.Publisher(broker)
        self.loop = loop

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print(f"Failed to connect: {rc}")

    ##handing string received
    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        print("Received Message: " + payload)

        asyncio.run_coroutine_threadsafe(
            self.publisher.send_str(topic + "/response", "received"), self.loop
        )

    ##Handing txt file received
    async def on_message_txt_async(self, topic, payload):
        try:
            with open("Received.txt", "w") as f:
                f.write(payload)
            print("File Saved")
            await asyncio.sleep(3)
            await self.publisher.send_str(topic + "/response", "received")
        except Exception as e:
            print(f"Error saving text file: {e}")

    def on_message_txt(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")

        asyncio.run_coroutine_threadsafe(
            self.on_message_txt_async(topic, payload), self.loop
        )


    ##handing exe file received
    def on_message_file(self, client, userdata, message):
        topic = message.topic
        try:
            with open("Received.exe", "ab") as f:
                f.write(message.payload)
            print("File Saved")

            asyncio.run_coroutine_threadsafe(
                self.publisher.send_str(topic + "/response", "received"), self.loop
            )
        except Exception as e:
            print(f"Error saving file: {e}")

    ## Receiving String
    async def get_string(self, topic):
        client = mqtt.Client()
        try:
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.connect(self.broker, 1883, 60)
            client.subscribe(topic)
            client.loop_start()

            await asyncio.Event().wait()
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    ## Receiving txt file
    async def get_txt(self, topic):
        client = mqtt.Client()
        try:
            client.on_connect = self.on_connect
            client.on_message = self.on_message_txt
            client.connect(self.broker, 1883, 60)
            client.subscribe(topic)
            client.loop_start()

            await asyncio.Event().wait()
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    ## Receiving file
    async def get_file(self, topic):
        client = mqtt.Client()
        try:
            client.on_connect = self.on_connect
            client.on_message = self.on_message_file
            client.connect(self.broker, 1883, 60)
            client.subscribe(topic)
            client.loop_start()
            await asyncio.Event().wait()
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()


##Testing
async def main():
    loop = asyncio.get_running_loop()
    broker = "broker.emqx.io"
    string_topic = "testmee/string"
    txt_topic = "testmee/txt"
    file_topic = "testmee/file"

    device = Subscriber(broker, loop)
    await asyncio.gather(device.get_txt(txt_topic), device.get_string(string_topic))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Subscriber stopped")

