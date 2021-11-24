import json, urllib3
from datetime import datetime

def lambda_handler(event, context):
    message = event['body']['message']

    f = open('/tmp/vault_secret.json',)
    dataOld = json.load(f)
    f.close()

    print(message)

#set current datetime as a kv val

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    payload = '{"date":' + date_time + '}"'

    print("+++++")
    print(payload)
    print(message)
    print("+++++")

    http = urllib3.PoolManager()
    data=json.dumps(payload)
    date_update = http.request('PUT', "http://127.0.0.1:8200/v1/pipeline/lambda/data"+data, headers={'Content-Type':'application/json'})
    f = open('/tmp/vault_secret.json',)
    dataChange = json.load(f)
    f.close()

#re reade datetime kv val
    date_update = http.request('GET', "http://127.0.0.1:8200/v1/pipeline/lambda/data")
    f = open('/tmp/vault_secret.json',)
    dataNew = json.load(f)
    f.close()

    return {
        'statusCode': 200,
        'message': message,
        'request_id': dataOld['request_id'],
        'dateOld': dataOld['data']['date'],
        'dataChange': dataChange,
        'date_update': date_update,
        'dateNew': dataNew['data']['date']
    }
