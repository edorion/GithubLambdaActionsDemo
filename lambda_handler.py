import json

def lambda_handler(event, context):
    body = json.loads(event)

    f = open('/tmp/vault_secret.json',)
    data = json.load(f)

    return {
        'statusCode': 200,
        'body': json.dumps(body),
        'data': json.dumps(data)
    }
