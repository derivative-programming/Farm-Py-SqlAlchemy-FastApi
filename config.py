# config.py  # pylint: disable=duplicate-code

"""
This module provides configuration settings for the application.
"""
import os
import configparser


def str_to_bool(value) -> bool:
    """
    Convert a string to a boolean value.
    """
    return value.lower() in ('true', '1', 'yes')


# Initialize the parser
config = configparser.ConfigParser()
config.read('config.ini')

# Access the DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL',
                         config['database']['DATABASE_URL'])

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL',
                              config['database']['TEST_DATABASE_URL'])

API_KEY_SECRET = os.getenv('API_KEY_SECRET',
                           config['apis']['API_KEY_SECRET'])

ENCRYPTION_KEY_SECRET = os.getenv('ENCRYPTION_KEY_SECRET',
                                  config['services']['ENCRYPTION_KEY_SECRET'])


IS_DYNAFLOW_TASK_QUEUE_USED = \
    str_to_bool(os.getenv(
        'IS_DYNAFLOW_TASK_QUEUE_USED',
        config['dyna_flow_processor']['IS_DYNAFLOW_TASK_QUEUE_USED']
    ))

IS_DYNAFLOW_TASK_MASTER = \
    str_to_bool(os.getenv(
        'IS_DYNAFLOW_TASK_MASTER',
        config['dyna_flow_processor']['IS_DYNAFLOW_TASK_MASTER']
    ))

IS_DYNAFLOW_TASK_PROCESSOR = \
    str_to_bool(os.getenv(
        'IS_DYNAFLOW_TASK_PROCESSOR',
        config['dyna_flow_processor']['IS_DYNAFLOW_TASK_PROCESSOR']
    ))


DYNAFLOW_TASK_RESULT_QUEUE_NAME = \
    os.getenv(
        'DYNAFLOW_TASK_RESULT_QUEUE_NAME',
        config['dyna_flow_processor']['DYNAFLOW_TASK_RESULT_QUEUE_NAME']
    )


DYNAFLOW_TASK_DEAD_QUEUE_NAME = \
    os.getenv(
        'DYNAFLOW_TASK_DEAD_QUEUE_NAME',
        config['dyna_flow_processor']['DYNAFLOW_TASK_DEAD_QUEUE_NAME']
    )

DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME = \
    os.getenv(
        'DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME',
        config['dyna_flow_processor']['DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME']
    )

AZURE_SERVICE_BUS_CONNECTION_STRING = \
    os.getenv(
        'AZURE_SERVICE_BUS_CONNECTION_STRING',
        config['dyna_flow_processor']['AZURE_SERVICE_BUS_CONNECTION_STRING']
    )
