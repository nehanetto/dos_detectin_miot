import time
import random
import paho.mqtt.client as mqtt

broker="localhost"
client= mqtt.Client()
client.connect(broker)

while True:
	heart_rate= random.randint(60,100)
	bp=random.randint(110,130)

	message = f"HeartRate:{heart_rate},BP:{bp}"
	client.publish("hospital/patient1/vitals",message)

	print("Sent:",message)
	time.sleep(2)
