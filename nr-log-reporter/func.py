import io
import os
import json
import requests
import logging
from fdk import response

def handler(ctx, data: io.BytesIO=None):

    nr_log_endpoint = os.environ['NR-LOG-ENDPOINT']
    nr_api_key = os.environ['NEWRELIC_API_KEY']

    try:
        logs = json.loads(data.getvalue())

        for item in logs:

            headers = {'Content-type': 'application/json', 'Api-Key': nr_api_key}
            x = requests.post(nr_log_endpoint, json.dumps(item["data"]), headers=headers)
            logging.getLogger().info(x.text)

    except (Exception, ValueError) as ex:
        logging.getLogger().info(str(ex))
        return
