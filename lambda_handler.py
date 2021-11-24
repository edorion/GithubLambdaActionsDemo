import json, urllib3
from datetime import datetime

def lambda_handler(event, context):
    message = event['body']['message']

    f = open('/tmp/vault_secret.json',)
    dataInitial = json.load(f)
    f.close()

#set current datetime as a kv val

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    payload = '{"date":"' + date_time + '"}'

    http = urllib3.PoolManager()
    date_update = http.request('PUT', "http://127.0.0.1:8200/v1/pipeline/lambda/data", body=payload, headers={'X-Vault-Request':'true'})
    f = open('/tmp/vault_secret.json',)
    dataChanged = json.load(f)
    f.close()

#re reade datetime kv val
    date_update = http.request('GET', "http://127.0.0.1:8200/v1/pipeline/lambda/data")
    f = open('/tmp/vault_secret.json',)
    dataNew = json.load(f)
    f.close()

    new_date = json.loads(date_update.data.decode('utf8'))

    return {
        'statusCode': 200,
        'message': message,
        'initialRequest_id': dataInitial['request_id'],
        'date1stFileRead': dataInitial['data']['date'],
        'date2ndFileRead': dataChanged['data']['date'],
        'date3rdFileRead': dataNew['data']['date'],
        'dateRequestResponse': new_date['data']['date']
    }
