import json
import boto3
import os

iot = boto3.client('iot-data', region_name='ap-northeast-1')
thingname = os.environ['THING_NAME']

payload_data = {
    "state": {
        "desired": {
            "powerOn": 0
        }
    }
}

def lambda_handler(event, context):
    click = event['deviceEvent']['buttonClicked']['clickType']
    print(click)
    if( click == "SINGLE"):
        payload_data['state']['desired']['powerOn'] = 1
    elif( click == "DOUBLE"):
        payload_data['state']['desired']['powerOn'] = 0
    elif( click == "LONG"):
        payload_data['state']['desired']['powerOn'] = 2

    iot.update_thing_shadow(thingName=thingname, payload=json.dumps(payload_data))

    return {
        "statusCode": 200
    }
