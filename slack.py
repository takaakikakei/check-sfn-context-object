import os
import boto3
import json
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

secret_name = os.environ['SECRET_NAME']
secretsmanager_client = boto3.client('secretsmanager',
                                     region_name='ap-northeast-1')
resp = secretsmanager_client.get_secret_value(SecretId=secret_name)
secret = json.loads(resp['SecretString'])
SLACK_WEBHOOK = secret['SLACK_WEBHOOK']


def alert_slack(event, context):
    message = "Error:{}\n\nCause:{}\n\nExecution:{}\n\nState{}\n\nStateMachine{}".format(
        event['param']['Error'], event['param']['Cause'], event['Execution'],
        event['State'], event['StateMachine'])
    payload = {
        "attachments": [{
            "color": "danger",
            "text": "{}".format(message)
        }]
    }
    data = json.dumps(payload)
    try:
        requests.post(SLACK_WEBHOOK, data=data)
    except Exception as e:
        logger.exception("alert_slack {}".format(e))
    else:
        return True
