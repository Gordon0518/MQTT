import paho.mqtt.client as mqtt

class Publisher:

    def __init__(self, broker):
        self.broker = broker


    ##Sending Text
    def send_str(self, topic, message):
        client = mqtt.Client()
        try:
            client.connect(self.broker, 1883, 60)
            client.loop_start()
            result = client.publish(topic, message)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published")
            else:
                print("Failed to publish")
        except Exception as e:
            print(e)
        finally:
            client.loop_stop()
            client.disconnect()

    ##Sending txt File
    def send_txt(self, topic, path):
        client = mqtt.Client()

        try:
            client.connect(self.broker, 1883, 60)
            client.loop_start()

            with open(path, "r") as f:
                txt = f.read()
                result = client.publish(topic, txt)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published")
            else:
                print("Failed to publish")
        except Exception as e:
            print(e)

        finally:
            client.loop_stop()
            client.disconnect()

if __name__ == '__main__':
    device = Publisher("broker.emqx.io")

    txt_topic = "testmee/txt"
    string_topic = "testmee/string"

    msg = "testing"
    path = "test.txt"

    device.send_str(string_topic, msg)

    device.send_txt(txt_topic, path)




