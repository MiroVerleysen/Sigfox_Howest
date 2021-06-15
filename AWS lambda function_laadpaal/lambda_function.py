import json
from datetime import datetime
import struct
import os



plaat1 = "unknown"
prijs = 1


        


def lambda_handler(event, context):

    prijs_kwh = 0.22
    
    if len(event["data"]) == 14:
        txt = event["data"]
        plaat = ''.join([chr(int(''.join(c), 16)) for c in zip(txt[0::2],txt[1::2])])
        print(plaat)
        global plaat1
        plaat1 = plaat[:1] + "-" + plaat[1:4] + "-" + plaat[4:]
        print("Voertuig met nummerplaat " + plaat1 + " is begonnen met opladen.")
        return {
            'statusCode': 200,
            'body': json.dumps('Nummerplaat')
        }
    elif len(event["data"]) == 8:
        tijd_hex = event["data"]
        tijd = struct.unpack('!f', bytes.fromhex(tijd_hex))[0]
        print(tijd)
        global prijs
        prijs = tijd * prijs_kwh
        print("Voertuig heeft met nummerplaat" + plaat1 + str(tijd) + " seconden opgeladen de totale kostprijs bedraagd €" + str(prijs))

        return {
            'statusCode': 200,
            'body': json.dumps('Tijd')
        }

    

    