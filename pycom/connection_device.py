from network import LoRa
import time
import binascii
import socket 

def send_tomuch_message():
    i = 0
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    while True:
      try:
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        s.setblocking(False)
        s.send(bytes([i]))
        print('Message sent')
        i += 1
        # time.sleep(1)
      except OSError as e:
        # the LoRaWAN command queue is full
        print(e)
        break

### Activate Device ###
lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)

app_eui = binascii.unhexlify('70B3D57ED003C0E9')
app_key = binascii.unhexlify('674D6B3050B39D82AE946DFC9AB4DCBB')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

### Send Message ###
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.send(bytes([1, 2, 3]))
print('Message sent')

send_tomuch_message()

### Receive Message ###
"""
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.send(bytes([1, 2, 3]))
s.settimeout(3.0) # configure a timeout value of 3 seconds
try:
   rx_pkt = s.recv(64)   # get the packet received (if any)
   print(rx_pkt)
except socket.timeout:
  print('No packet received')
"""