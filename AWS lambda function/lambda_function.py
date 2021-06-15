#!/usr/bin/env python3
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import struct
import textwrap

# InfluxDB Configuratie
token = "<influxdb_token>"
org = "<influxdb_organisation>"
bucket = "<influxdb_bucket>"

client = InfluxDBClient(url="<influxdb_url>", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

def lambda_handler(event, context):
    data = textwrap.wrap(event["data"], 8)
    temp = data[0]
    hum = data[1]
    bat = data[2]

    temperature = struct.unpack('!f', bytes.fromhex(temp))[0]
    humidity = struct.unpack('!f', bytes.fromhex(hum))[0]
    battery = struct.unpack('!f', bytes.fromhex(bat))[0]
    print("device: " + event["device"] + " data: " + event["data"])

    sequence = ["sigfox,devicename={} Temperature={}".format(event["device"], temperature),
                "sigfox,devicename={} Humidity={}".format(event["device"], humidity),
                "sigfox,devicename={} Battery={}".format(event["device"], battery)]
    write_api.write(bucket, org, sequence)
    return "device: " + event["device"] + " data: " + event["data"]