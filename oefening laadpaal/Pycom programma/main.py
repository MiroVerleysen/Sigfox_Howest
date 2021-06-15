import micropython
from machine import Pin
import pycom
import time
from network import Sigfox
import socket
import struct
import ubinascii
import binascii
import socket
import os
from SI7006A20 import SI7006A20

# Colors
off   = 0x000000
red   = 0xff0000
green = 0x00ff00
blue  = 0x0000ff

pycom.heartbeat(False)

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def send_data(data):
    pycom.rgbled(blue)
    b_payload=ubinascii.unhexlify(data)
    s.send(b_payload)
    print("Data sturen naar sigfox backend....")

def watchdog():
    while 1 == 1:
        print("watchdog")
        time.sleep(2)

def genereernummerplaat():
    pn = os.urandom(1)[0] % 2 + 1
    pn_hex = float_to_hex(pn)[2:]
    #genereer 3 random letters, l1, l2, l3
    l1 = os.urandom(1)[0] % 26 + 1
    l2 = os.urandom(1)[0] % 26 + 1
    l3 = os.urandom(1)[0] % 26 + 1
    #genereer 3 random nummers, n1, n2, n3
    n1 = os.urandom(1)[0] % 10
    n1_hex = float_to_hex(n1)[2:]
    n2 = os.urandom(1)[0] % 10
    n2_hex = float_to_hex(n2)[2:]
    n3 = os.urandom(1)[0] % 10
    n3_hex = float_to_hex(n3)[2:]
    #combineren + printen
    letter1 = chr(ord('@')+l1)
    letter1_hex = hex(ord(letter1))[2:]
    letter2 = chr(ord('@')+l2)
    letter2_hex = hex(ord(letter2))[2:]
    letter3 = chr(ord('@')+l3)
    letter3_hex = hex(ord(letter3))[2:]

    nummerplaat = str(pn) + letter1 + letter2 + letter3 + str(n1) + str(n2) + str(n3)
    s = nummerplaat.encode('utf-8')
    hex_nummerplaat = binascii.hexlify(s)
    send_data(hex_nummerplaat)
    return (str(pn)+"-"+letter1+letter2+letter3+'-'+str(n1)+str(n2)+str(n3))

# make `P10` an input with the pull-up enabled
p_in = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
nummerplaat =""
aantalkeer = 0
state = -1
# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
# print Sigfox Device ID
print(binascii.hexlify(sigfox.id()))
# print Sigfox PAC number
print(binascii.hexlify(sigfox.pac()))
print("\nConnecting to the Sigfox network ...")
pycom.rgbled(red)
time.sleep(2)
print('Joined')
pycom.rgbled(green)
time.sleep(2)
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# make the socket blocking
s.setblocking(True)
# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

watchdogtijd = time.time()

while True:
    time.sleep(0.5)
    newwatchdogtijd = time.time()
    print(newwatchdogtijd - watchdogtijd)
    if newwatchdogtijd - watchdogtijd >= 43200: #43200 = 12h
        # the True argument is what sets the SiPy to expect a downlink message
        s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

        s.send("Alive?")

        print(binascii.hexlify(s.recv(32)))
        s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
        watchdogtijd = time.time()
    new_state = p_in() # get value, 0 or 1
    if new_state != state and new_state == 1:
        pycom.rgbled(red)
        time.sleep(0.1)
        aantalkeer = aantalkeer +1
        if aantalkeer > 1:
            print("Gestopt met opladen.")
            tijd = time.time() - start_time
            tijd_hex = float_to_hex(tijd)[2:]
            send_data(tijd_hex)
            pycom.rgbled(red)
            print("Voertuig heeft gedurende %s seconden opgeladen." % (tijd))
        state = new_state
    elif new_state != state and new_state == 0:
        time.sleep(0.1)
        print("Er begon een voertuig op te laden met het kenteken: " + genereernummerplaat() + ".")
        start_time = time.time()
        pycom.rgbled(green)
        state = new_state
