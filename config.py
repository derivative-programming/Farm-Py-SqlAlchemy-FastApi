# config.py

"""
This module provides configuration settings for the application.
"""
import os
import configparser

# Initialize the parser
config = configparser.ConfigParser()
config.read('config.ini')

# Access the DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL',
                         config['database']['DATABASE_URL']) 

API_KEY_SECRET = os.getenv('API_KEY_SECRET',
                           config['apis']['API_KEY_SECRET'])

ENCRYPTION_KEY_SECRET = os.getenv('ENCRYPTION_KEY_SECRET',
                                  config['services']['ENCRYPTION_KEY_SECRET'])
