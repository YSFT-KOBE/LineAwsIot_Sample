import json
import os
import boto3

import base64
import hashlib
import hmac

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

channelAccessToken = os.environ["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(channelAccessToken)

iot = boto3.client('iot-data', region_name='ap-northeast-1')

def lambda_handler(event, context):
    print(json.dumps(event))

    reptext = ""
    if "state" in event :
        if "reported" in event["state"] :
            poweron = event["state"]["reported"]["powerOn"]
            if 1 == poweron :
                reptext = "玄関の電灯が点灯しました。"
            else :
                reptext = "玄関の電灯が消灯しました。"

    try:
        if reptext != "":
            lineUserId = os.environ["LINE_USER_ID"]
            line_bot_api.push_message(lineUserId, TextSendMessage(text=reptext))
    except LineBotApiError as e:
        pass

    return {
        "statusCode": 200
    }

def lambda_iotEvents_powerOnDetect_handler(event, context):
    # TODO implement
    print(json.dumps(event))

    reptext = "玄関の電灯が点灯しています。"
    try:
        lineUserId = os.environ["LINE_USER_ID"]
        line_bot_api.push_message(lineUserId, TextSendMessage(text=reptext))
    except LineBotApiError as e:
        pass

    return {
        'statusCode': 200,
    }

def lambda_getStatus_handler(event, context):
    print(json.dumps(event))

    # Line Signature Check
    if ('headers' in event) and ('x-line-signature' in event['headers']) :
        line_head_sig = event['headers']['x-line-signature']
    else:
        return {
            "statusCode": 401
        }

    if ('body' in event) :
        line_body = json.loads(event['body'])
    else:
        return {
            "statusCode": 400
        }

    LineChannelSecret = os.environ["LINE_CHANNEL_SECRET"]
    hash = hmac.new(LineChannelSecret.encode('utf-8'), event['body'].encode('utf-8'), hashlib.sha256).digest() 
    signature = base64.b64encode(hash).decode()
    
    if line_head_sig != signature:
        return {
            "statusCode": 401
        }

    if "events" in line_body :
        for linereq in line_body['events']:
            print(json.dumps(linereq))
            if "replyToken" in linereq:
                reply_token = linereq['replyToken']
                resp_message = ''
                if linereq['type'] == 'message':
                    if linereq['source']['type'] == 'user' and linereq['message']['type'] == 'text':
                        message = linereq['message']['text']
                        if '点灯状態' == message:
                            thingname = os.environ['THING_NAME']
                            try:
                                resp = iot.get_thing_shadow( thingName=thingname)
                                print(resp)
                                res = json.load(resp['payload'])
                                if 'reported' not in res['state']:
                                    resp_message = '玄関の電灯は、消灯しています。'
                                else :
                                    poweron = res['state']['reported']['powerOn']
                                    if poweron == 1:
                                        resp_message = '玄関の電灯は、点灯中です。'
                                    else:
                                        resp_message = '玄関の電灯は、消灯しています。'
                            except Exception as e:
                                print(e.args)
                                resp_message = '玄関の電灯は、消灯しています。'
                if resp_message == '':
                    resp_message = 'メッセージが正しくありません。'
                line_bot_api.reply_message(reply_token, TextSendMessage(text=resp_message))

    return {
        "statusCode": 200
    }
