import json, urllib3
from datetime import datetime

def lambda_handler(event, context):
    vault_addr = "http://127.0.0.1"

    message = event['body']['message']

    f = open('/tmp/vault_secret.json',)
    dataOld = json.load(f)
    f.close()


#set current datetime as a kv val
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    payload = '{"date":' + date_time + '}"'
    date_update = http.request('PUT', "https://127.0.0.1:8200/v1/pipeline/lambda/data", data=json.dumps(payload))
    #date_update = requests.put("https://127.0.0.1:8200/v1/pipeline/lambda/data", data=json.dumps(payload))
    f = open('/tmp/vault_secret.json',)
    dataChange = json.load(f)
    f.close()

#re reade datetime kv val
    date_update = http.request('GET', "https://127.0.0.1:8200/v1/pipeline/lambda/data")
    #date_update = requests.get("https://127.0.0.1:8200/v1/pipeline/lambda/data")
    f = open('/tmp/vault_secret.json',)
    dataNew = json.load(f)
    f.close()

    return {
        'statusCode': 200,
        'message': message,
        'request_id': data[request_id],
        'dateOld': dataOld['data']['date'],
        'dataChange': dataChange.status_code,
        'dateNew': dataNew['data']['date']
    }
