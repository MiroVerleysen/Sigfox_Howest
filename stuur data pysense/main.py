import micropython
from network import Sigfox
import socket
import pycom
from pysense import Pysense
import time
import binascii
import ubinascii
import struct

from SI7006A20 import SI7006A20

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def get_temperature_humidity():
    si=SI7006A20(py)
    t=si.temperature()
    t_hex=float_to_hex(t)

    h=si.humidity()
    h_hex=float_to_hex(h)

    print("Temperature: " + str(t)+ " deg C and Relative Humidity: " + str(h) + " %RH")



    return t_hex, h_hex

def get_battery():
    bat=py.read_battery_voltage()
    bat_hex=float_to_hex(bat)
    print("Battery voltage: " + str(bat))
    #print(bat_hex[2:])
    #bat=struct.unpack('f',struct.pack('i',int(bat_hex,16)))
    #print(bat[0])

    return bat_hex

# Colors
off   = 0x000000
red   = 0xff0000
green = 0x00ff00
blue  = 0x0000ff

# Turn off hearbeat LED
pycom.heartbeat(False)
micropython.kbd_intr(ord('q'))
try:
    while True:
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

        py=Pysense()
        pycom.rgbled(blue)

        (t_hex,h_hex)=get_temperature_humidity()
        bat_hex=get_battery()

        # send max 12 bytes
        payload=t_hex[2:]+h_hex[2:]+bat_hex[2:]
        print("\npayload (hexadecimal): "+str(payload))
        b_payload=ubinascii.unhexlify(payload)
        print("payload (binary)     : "+str(b_payload))
        s.send(b_payload)

        pycom.rgbled(green)
        time.sleep(10)
        #break

        s.close()
        print("verzonden, volgende bericht wordt over een kwartier verzonden.")

        pycom.rgbled(red)
        time.sleep(1)
        pycom.rgbled(off)
        time.sleep(1)
        time.sleep(900)

except KeyboardInterrupt:
    print("Exiting ...")

s.close()
pycom.rgbled(red)
time.sleep(2)
pycom.rgbled(off)