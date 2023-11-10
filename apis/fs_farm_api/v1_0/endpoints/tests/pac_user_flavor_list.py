import json
from django.test import TestCase
from rest_framework.test import APIClient
import logging
from models.factory import PacFactory
from apis.factories import RequestFactory
from helpers import ApiToken
from models import CurrentRuntime
import logging

class PacUserFlavorListViewSetTestCase(TestCase):

    def setUp(self):
        CurrentRuntime.initialize()
        self.client = APIClient()
        self.pac = PacFactory.create()
        logging.info('call RequestFactory.create()')
        self.request = RequestFactory.create()
        self.valid_request_data =  asdict(self.request)
        self.invalid_request_data = {
            "xxxxxx": "yyyyy"
        }
        api_dict = {'PacCode': str(self.pac.code), 'role_name_csv':'User'}
        self.test_api_key = ApiToken.create_token(api_dict,1)
        self.valid_header = {'HTTP_API_KEY' : self.test_api_key}

    ## TODO add test - zeroed context code replaced by true code in api token
    ## TODO add test - invalid api key
    ## TODO add test - no api key on public endpoint
    ## TODO add test - no api key on private endpoint
    ## TODO add test - correct role required in api key

    def test_post_not_implemented(self):
        # Assuming you have a FlowPacUserFlavorList.process method that handles valid data
        logging.info('/api/v1_0/pac-user-flavor-list/')
        logging.info(self.valid_request_data)
        response = self.client.post('/api/v1_0/pac-user-flavor-list/', self.valid_request_data, content_type='application/json')
        self.assertEqual(response.status_code, 501)

    def test_submit_success(self):
        # Assuming you have a FlowPacUserFlavorList.process method that handles valid data
        logging.info(f'/api/v1_0/pac-user-flavor-list/{self.pac.code}/')
        logging.info(self.valid_request_data)
        response = self.client.post(f'/api/v1_0/pac-user-flavor-list/{self.pac.code}/submit/', data=self.valid_request_data, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode()
        responseDict = json.loads(json_string)
        self.assertTrue(response.data['success'])

    def test_submit_failure(self):
        logging.info(self.invalid_request_data)
        response = self.client.post(f'/api/v1_0/pac-user-flavor-list/{self.pac.code}/submit/', data=self.invalid_request_data, **self.valid_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode()
        responseDict = json.loads(json_string)
        self.assertFalse(response.data['success'])

    def test_submit_failure2(self):
        response = self.client.get('/api/v1_0/pac-user-flavor-list/xxx/', **self.valid_header)
        self.assertEqual(response.status_code, 404)

    def test_submit_failure3(self):
        response = self.client.get('/api/v1_0/pac-user-flavor-list/', **self.valid_header)
        self.assertEqual(response.status_code, 501)

    def test_init_success(self):
        response = self.client.get(f'/api/v1_0/pac-user-flavor-list/{self.pac.code}/init/', **self.valid_header)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode()
        responseDict = json.loads(json_string)
        self.assertTrue(response.data['success'])

    def test_init_failure(self):
        response = self.client.get('/api/v1_0/pac-user-flavor-list/xxx/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)

    def test_init_failure2(self):
        response = self.client.get('/api/v1_0/pac-user-flavor-list/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)

    # Add any additional test cases for different scenarios and edge cases
