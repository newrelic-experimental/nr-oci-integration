import io
import os
import json
import requests
import logging
from fdk import response

def handler(ctx, data: io.BytesIO=None):

    # NR Logs endpoint URL and token to call the API endpoint. 
    # This is defined in the func.yaml file or on the OCI Function Environment Settings
    # EU: https://log-api.eu.newrelic.com/log/v1
    # US: https://log-api.newrelic.com/log/v1
    nr_log_endpoint = os.getenv('NR-LOG-ENDPOINT','not-configured')

    # NR API Key for authentication. 
    # This is defined in the func.yaml file or on the OCI Function Environment Settings
    nr_api_key = os.getenv('NEWRELIC_API_KEY','not-configured')

    # NR API Key for authentication. 
    # This is defined in the func.yaml file or on the OCI Function Environment Settings
    forward_to_nr = os.getenv('FORWARD_TO_NR', 'True')

    if forward_to_nr is False:
        logging.getLogger().debug("Log Reporting is disabled - nothing sent")
        return
    
    if nr_api_key == 'not-configured':
        logging.getLogger().error("No API Key Configured - nothing sent")
        return
    
    if nr_log_endpoint == 'not-configured':
        logging.getLogger().error("Log Endpoint Not Configured - nothing sent")
        return
    
    try:
        # parse payload from request
        logs = json.loads(data.getvalue())

        # Setting Request Header and API Key
        headers = {'Content-type': 'application/json', 'Api-Key': nr_api_key}

        #for each log line
        for item in logs:
            # Post Log
            response = requests.post(nr_log_endpoint, json.dumps(item["data"]), headers=headers)

            #Optional Log (response)
            logging.getLogger().info(response.text)

            # Possible New Relic API Error Response Codes
            if response.status != 202:
                match response.status:
                    case 400:
                        logging.getLogger().error("400 - Structure of the request is invalid.")
                    case 403:
                        logging.getLogger().error("403 - Authentication failure.")
                    case 408:
                        logging.getLogger().error("408 - The request took too long to reach the endpoint.")
                    case 411:
                        logging.getLogger().error("411 - The Content-Length header wasn’t included.")
                    case 413:
                        logging.getLogger().error("413 - The payload was too big. Payloads must be under 1MB (10^6 bytes).")
                    case 429:
                        logging.getLogger().error("429 - The request rate quota has been exceeded.")
                    case _:
                        logging.getLogger().error('%s - Server Error, please retry.', response.status)
                raise Exception ('error {} sending to NR: {}'.format(response.status, response.reason))

    except (Exception, ValueError) as ex:
        logging.getLogger().info(str(ex))
        return
