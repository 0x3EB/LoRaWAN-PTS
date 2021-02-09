import paho.mqtt.client as mqtt
import time
import re

def on_message(client, userdata, message):
    match = re.compile("frequency\":([0-9]+)")
    res = match.sub("frequency\":200", message.payload.decode("utf-8"))
    client.publish("gateway/cdcdcdcdcdcdcdcd/event/up", res)

client = mqtt.Client("FQMISLEAD")
client.connect("localhost")
client.subscribe("gateway/abababababababab/event/up")
client.on_message = on_message
client.loop_start()
time.sleep(100)
client.loop_stop()