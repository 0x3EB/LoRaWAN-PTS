#!/usr/bin/env python


### Configuration ###

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "fr.pool.ntp.org" #"pool.ntp.org"
NTP_PERIOD_S = 350

WIFI_SSID = 'OnePlus7T' # my wifi
WIFI_PASS = '123456789' # my wifi password

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5



### OTAA Node ###

from network import LoRa
import socket
import binascii
import struct
import time

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTA authentication params
dev_eui = binascii.unhexlify('70B3D5499CCFCD77')
app_eui = binascii.unhexlify('70B3D57ED003C0E9')
app_key = binascii.unhexlify('DB1D29A8BAE112E22A50370B378BCD17')

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency= LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency= LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency= LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr= LORA_NODE_DR)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR,  LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

time.sleep(5.0)

for i in range (200):
    pkt = b'PKT #' + bytes([i])
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
