import paho.mqtt.client as mqtt
import asyncio

class Publisher:

    def __init__(self, broker):
        self.broker = broker

    ## Sending txt File
    async def send_txt(self, topic, path):
        client = mqtt.Client()
        try:
            client.connect(self.broker, 1883, 60)
            client.loop_start()
            with open(path, "r") as f:
                txt = f.read()
                result = client.publish(topic, txt)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published txt")
                await self.str_response(topic)
            else:
                print("Failed to publish txt")
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    ## Sending file
    async def send_file(self, topic, path):
        client = mqtt.Client()
        try:
            client.connect(self.broker, 1883, 60)
            client.loop_start()
            with open(path, "rb") as f:
                file = f.read()
                result = client.publish(topic, file)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published file")
                await self.str_response(topic)
            else:
                print("Failed to publish file")
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print(f"Failed to connect: {rc}")

    def on_message(self, client, userdata, message):
        print("Received Message: " + message.payload.decode("utf-8"))

    ##Handing getting response
    async def str_response(self, topic):
        client = mqtt.Client()
        try:
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.connect(self.broker, 1883, 60)
            client.loop_start()
            client.subscribe(topic + "/response")
            await asyncio.sleep(10)
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    ## Sending Text
    async def send_str(self, topic, message):
        client = mqtt.Client()
        try:
            client.connect(self.broker, 1883, 60)
            client.loop_start()
            result = client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published string")
                await self.str_response(topic)
            else:
                print("Failed to publish string")
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()


##Testing
async def main():
    ##broker
    device = Publisher("broker.emqx.io")

    ##Topic
    txt_topic = "testmee/txt"
    string_topic = "testmee/string"
    file_topic = "testmee/file"

    msg = "testing"
    path = "test.txt"
    exe_path = "record.py"

    await asyncio.gather(
        device.send_str(string_topic, msg),
        device.send_txt(txt_topic, path),
        # device.send_file(file_topic, exe_path)
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Publisher stopped")


