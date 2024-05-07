import io
import json
import logging
import os
import re
import requests
from fdk import response
from datetime import datetime
from newrelic_telemetry_sdk import GaugeMetric, CountMetric, SummaryMetric, MetricClient

# Use OCI Application or Function configurations to override these environment variable defaults.

nr_api_key = os.getenv('NEWRELIC_API_KEY', 'not-configured')

forward_to_nr = eval(os.getenv('FORWARD_TO_NR', "True"))
metric_tag_keys = os.getenv('METRICS_TAG_KEYS', 'name, namespace, displayName, resourceDisplayName, unit')
metric_tag_set = set()

# Exception stack trace logging

is_tracing = eval(os.getenv('ENABLE_TRACING', "False"))

# Set all registered loggers to the configured log_level

logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
loggers = [logging.getLogger()] + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
[logger.setLevel(logging.getLevelName(logging_level)) for logger in loggers]

# Constants

TEN_MINUTES_SEC = 10 * 60
ONE_HOUR_SEC = 60 * 60

# Functions

def handler(ctx, data: io.BytesIO = None):
    """
    OCI Function Entry Point
    :param ctx: InvokeContext
    :param data: data payload
    :return: plain text response indicating success or error
    """

    preamble = " {} / event count = {} / logging level = {} / forwarding to NR = {}"

    if nr_api_key == 'not-configured':
        logging.getLogger().error("No API Key Configured")
        return

    try:
        logging.getLogger().info('function payload: %s',data.getvalue())
        metrics_list = json.loads(data.getvalue())
        logging.getLogger().info(preamble.format(ctx.FnName(), len(metrics_list), logging_level, forward_to_nr))
        #logging.getLogger().debug(metrics_list)

        converted_event_list = handle_metric_events(event_list=metrics_list)
        send_to_nr(event_list=converted_event_list)

    except (Exception, ValueError) as ex:
        logging.getLogger().error('error handling logging payload: {}'.format(str(ex)))
        if is_tracing:
            logging.getLogger().error(ex)


def handle_metric_events(event_list):
    """
    :param event_list: the list of metric formatted log records.
    :return: the list of NR formatted log records
    """

    result_list = []
    for event in event_list:

        single_result = transform_metric_to_nr_format(log_record=event)
        result_list.append(single_result)
        logging.getLogger().debug(single_result)

    return result_list


def transform_metric_to_nr_format(log_record: dict):

    metric_list = []
    metricName = get_metric_name(log_record)
    type = get_metric_type(log_record)
    points = get_metric_points(log_record)
    metricTags = get_metric_tags_nr(log_record)

    for datapoints in points:

        #using gauge for all
        gaugeMetric = GaugeMetric(name=metricName,value=datapoints['value'], tags=metricTags, end_time_ms=datetime.now().timestamp())
        metric_list.append(gaugeMetric)

    return metric_list
  
  def get_metric_name(log_record: dict):
    """
    Assembles a metric name that appears to follow NR conventions.
    :param log_record:
    :return:
    """

    elements = get_dictionary_value(log_record, 'namespace').split('_')
    elements += camel_case_split(get_dictionary_value(log_record, 'name'))
    elements = [element.lower() for element in elements]
    return '.'.join(elements)


def camel_case_split(str):
    """
    :param str:
    :return: Splits camel case string to individual strings
    """

    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)


def get_metric_type(log_record: dict):
    """
    :param log_record:
    :return: The type of metric. The available types are 0 (unspecified), 1 (count), 2 (rate), and 3 (gauge).
    Allowed enum values: 0,1,2,3
    """

    return 0
  
  def get_now_timestamp():
    return datetime.now().timestamp()


def get_metric_points(log_record: dict):

    result = []

    datapoints = get_dictionary_value(dictionary=log_record, target_key='datapoints')
    for point in datapoints:
        nr_point = {'timestamp': point.get('timestamp'), 'value': point.get('value')}
        result.append(nr_point)

    return result

def get_metric_tags_nr(log_record: dict):

    result = {}

    for tag in get_metric_tag_set():
        value = get_dictionary_value(dictionary=log_record, target_key=tag)
        if value is None:
            continue

        if isinstance(value, str) and ':' in value:
            logging.getLogger().warning('tag contains a \':\' / ignoring {} ({})'.format(tag, value))
            continue

        result[tag] = value

    return result
def get_metric_tag_set():
    """
    :return: the set metric payload keys that we would like to have converted to tags.
    """

    global metric_tag_set

    if len(metric_tag_set) == 0 and metric_tag_keys:
        split_and_stripped_tags = [x.strip() for x in metric_tag_keys.split(',')]
        metric_tag_set.update(split_and_stripped_tags)
        logging.getLogger().debug("tag key set / {} ".format (metric_tag_set))

    return metric_tag_set

def get_dictionary_value(dictionary: dict, target_key: str):
    """
    Recursive method to find value within a dictionary which may also have nested lists / dictionaries.
    :param dictionary: the dictionary to scan
    :param target_key: the key we are looking for
    :return: If a target_key exists multiple times in the dictionary, the first one found will be returned.
    """

    if dictionary is None:
        raise Exception('dictionary None for key'.format(target_key))

    target_value = dictionary.get(target_key)
    if target_value:
        return target_value

    for key, value in dictionary.items():
        if isinstance(value, dict):
            target_value = get_dictionary_value(dictionary=value, target_key=target_key)
            if target_value:
                return target_value

        elif isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    target_value = get_dictionary_value(dictionary=entry, target_key=target_key)
                    if target_value:
                        return target_value


def send_to_nr (event_list):
    """
    Sends each transformed event to NR Endpoint.
    :param event_list: list of events in NR format
    :return: None
    """
    if send_to_nr is False:
        logging.getLogger().debug("Metric Reporting is disabled - nothing sent")
        return

    try:

        metric_client = MetricClient(nr_api_key)

        for metric in event_list:

            response = metric_client.send_batch(event_list[0])
            logging.getLogger().debug('payload: %s', event_list[0])

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
                    case 431:
                        logging.getLogger().error("431 - The request headers are too long.")
                    case _:
                        logging.getLogger().error('%s - Server Error, please retry.', response.status)
                raise Exception ('error {} sending to NR: {}'.format(response.status, response.reason))

        #response.raise_for_status()

    finally:
        metric_client.close()


def get_dictionary_value(dictionary: dict, target_key: str):
    """
    Recursive method to find value within a dictionary which may also have nested lists / dictionaries.
    :param dictionary: the dictionary to scan
    :param target_key: the key we are looking for
    :return: If a target_key exists multiple times in the dictionary, the first one found will be returned.
    """

    if dictionary is None:
        raise Exception('dictionary None for key'.format(target_key))

    target_value = dictionary.get(target_key)
 
    if target_value:
        return target_value

    for key, value in dictionary.items():
        if isinstance(value, dict):
            target_value = get_dictionary_value(dictionary=value, target_key=target_key)
            if target_value:
                return target_value

        elif isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    target_value = get_dictionary_value(dictionary=entry, target_key=target_key)
                    if target_value:
                        return target_value


def local_test_mode(filename):
    """
    This routine reads a local json metrics file, converting the contents to NR format.
    :param filename: cloud events json file exported from OCI Logging UI or CLI.
    :return: None
    """

    logging.getLogger().info("local testing started")

    with open(filename, 'r') as f:
        transformed_results = list()

        for line in f:
            event = json.loads(line)
            logging.getLogger().debug(json.dumps(event, indent=4))

            transformed_result = transform_metric_to_nr_format(event)

            transformed_results.append(transformed_result)

        logging.getLogger().debug(json.dumps(transformed_results, indent=4))

        send_to_nr(event_list=transformed_results)
    logging.getLogger().info("local testing completed")


"""
Local Debugging 
"""

if __name__ == "__main__":
    local_test_mode('oci-metrics.json')
