from django.test import TestCase
from rest_framework.test import APIClient 
from apis.fs_farm_api.v1_0.view_sets import TacFarmDashboardViewSet
from uuid import uuid4
import logging
import json
from models.factory import TacFactory
from helpers import ApiToken 
from models import CurrentRuntime

class TacFarmDashboardViewSetTestCase(TestCase):

    def setUp(self):
        CurrentRuntime.initialize()
        self.client = APIClient() 
        self.tac = TacFactory.create()
        self.valid_request_data = {
            "pageNumber": "1",
            "itemCountPerPage": "1",
            "orderByColumnName": "",
            "orderByDescending": "false" 
        }
        self.invalid_request_data = {
            "xxxxxx": "invalid@example.com",
            "yyyyyy": "wrong_password"
        }

        self.invalid_request_data2 = {
            "pageNumber": "1",
            "itemCountPerPage": "0",
            "orderByColumnName": "",
            "orderByDescending": "false" 
        }

        self.invalid_request_data3 = {
            "pageNumber": "0",
            "itemCountPerPage": "2",
            "orderByColumnName": "",
            "orderByDescending": "false" 
        }
        api_dict = {'TacCode': str(self.tac.code), 'role_name_csv':'User'}
        self.test_api_key = ApiToken.create_token(api_dict,1)
        self.valid_header = {'HTTP_API_KEY' : self.test_api_key}
    def test_submit_success(self):
        logging.debug('TacFarmDashboardViewSetTestCase test_submit_success')
        # Assuming you have a FlowTacFarmDashboard.process method that handles valid data 
        response = self.client.get(f'/api/v1_0/tac-farm-dashboard/{self.tac.code}/', data=self.valid_request_data,**self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertTrue(responseDict['success'])

    def test_submit_failure(self):
        logging.debug('TacFarmDashboardViewSetTestCase test_submit_failure')
        response = self.client.get(f'/api/v1_0/tac-farm-dashboard/{self.tac.code}/', data=self.invalid_request_data, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertFalse(response.data['success'])
        
    
    def test_submit_failure2(self):
        response = self.client.get('/api/v1_0/tac-farm-dashboard/xxx/', **self.valid_header)
        self.assertEqual(response.status_code, 404) 

    def test_submit_failure3(self):
        response = self.client.get('/api/v1_0/tac-farm-dashboard/', **self.valid_header)
        self.assertEqual(response.status_code, 404)
        

    def test_submit_failure4(self):
        response = self.client.get(f'/api/v1_0/tac-farm-dashboard/{self.tac.code}/', data=self.invalid_request_data2, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertFalse(response.data['success'])
        

    def test_submit_failure5(self):
        response = self.client.get(f'/api/v1_0/tac-farm-dashboard/{self.tac.code}/', data=self.invalid_request_data3, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertFalse(response.data['success'])

    def test_init_success(self):
        response = self.client.get(f'/api/v1_0/tac-farm-dashboard/{self.tac.code}/init/', **self.valid_header)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertTrue(response.data['success'])

    
    def test_init_failure(self):
        response = self.client.get('/api/v1_0/tac-farm-dashboard/xxx/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)
        
    def test_init_failure2(self):
        response = self.client.get('/api/v1_0/tac-farm-dashboard/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)

    # Add any additional test cases for different scenarios and edge cases
