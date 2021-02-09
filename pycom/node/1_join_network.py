from network import LoRa
import time
import binascii
import socket

lora = LoRa(mode=LoRa.LORAWAN, region= LoRa.EU868)

app_eui = binascii.unhexlify('0000000000000000')
app_key = binascii.unhexlify('00000000000000000000000000000000')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

#send message
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.send(bytes([1,2,3]))
print('Message sent')

#receive message
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.send(bytes([1,2,3]))
s.settimeout(3.0)
try:
    rx_pkt = s.recv(64)
    print(rx_pkt)
except socket.error:
    print("No packet receive")