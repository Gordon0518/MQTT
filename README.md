# MQTT Publisher and Subscriber Project Report

##Introduction

    - Allow Sending and Receving String or txt file though MQTT

##Project Structure

    -Publisher.py
    -Subscriber.py

##publisher.py

    -Two main Fucntion:

        1.send_str(topic, message)
            - For String 
            - Send the message to the topic in mqtt broker

        2.send_txt(topic, path)
            - For txt file
            - Send the data from the txt file to the topic in mqtt broker

    -Example Usage

        ##Input the address of mqtt broker
        device = Publisher("broker.hivemq.com")
        
        ##Topic
        txt_topic = "testmee/txt"
        string_topic = "testmee/string"
        
        ##Message and Path of the file
        msg = "testing"
        path = "test.txt"
        
        ##Run the function
        device.send_str(string_topic, msg)
        device.send_txt(txt_topic, path)

##Subscriber.py

    Two Main Function:
        1.get_string(topic)
            -For String
            -Subscribe the topic and wait for response and return the message recieved
        
        2.get_txt(topic)
            -For txt file
            -Subscribe the topic and wait for response and save the data recieved to a new txt file

    
    -Example Usage
        
        
        async def main():
            ##Input the address of mqtt broker
            broker = "broker.hivemq.com"
            
            ##Input the topic wanted to subscribe
            string_topic = "testmee/string"
            txt_topic = "testmee/txt"

            device = Subscriber(broker)
            
            ##Run both function at the same time and wait for response
            await asyncio.gather(device.get_txt(txt_topic), device.get_string(string_topic))