import json
from django.test import TestCase
from rest_framework.test import APIClient 
from apis.fs_farm_api.v1_0.view_sets import TacRegisterViewSet
from uuid import uuid4
import logging
from models.factory import TacFactory
from helpers import ApiToken 
from models import CurrentRuntime

class TacRegisterViewSetTestCase(TestCase):

    def setUp(self):
        CurrentRuntime.initialize()
        self.client = APIClient() 
        self.tac = TacFactory.create()
        self.valid_request_data = {
            "email": "test@example.com",
            "password": "test_password",
            "confirmPassword": "test_password",
            "firstName": "test_first_name",
            "lastName": "test_last_name",
        }
        self.invalid_request_data = {
            "emailxxx": "invalid@example.com",
            "password": "wrong_password"
        }
        api_dict = {'TacCode': str(self.tac.code), 'role_name_csv':''}
        self.test_api_key = ApiToken.create_token(api_dict,1)
        self.valid_header = {'HTTP_API_KEY' : self.test_api_key}

    def test_submit_success(self):
        # Assuming you have a FlowTacRegister.process method that handles valid data
        logging.debug(f'/api/v1_0/tac-register/{self.tac.code}/')
        response = self.client.post(f'/api/v1_0/tac-register/{self.tac.code}/submit/', data=self.valid_request_data, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertTrue(response.data['success'])

    def test_submit_failure(self):
        response = self.client.post(f'/api/v1_0/tac-register/{self.tac.code}/submit/', data=self.invalid_request_data, **self.valid_header, format='json')
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertFalse(response.data['success'])
        
    def test_submit_failure2(self):
        response = self.client.get('/api/v1_0/tac-register/xxx/', **self.valid_header)
        self.assertEqual(response.status_code, 404)
        
    def test_submit_failure3(self):
        response = self.client.get('/api/v1_0/tac-register/', **self.valid_header)
        self.assertEqual(response.status_code, 501)

    def test_init_success(self):
        response = self.client.get(f'/api/v1_0/tac-register/{self.tac.code}/init/', **self.valid_header)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode() 
        responseDict = json.loads(json_string) 
        self.assertTrue(response.data['success'])

    def test_init_failure(self):
        response = self.client.get('/api/v1_0/tac-register/xxx/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)
        
    def test_init_failure2(self):
        response = self.client.get('/api/v1_0/tac-register/init/', **self.valid_header)
        self.assertEqual(response.status_code, 404)

    # Add any additional test cases for different scenarios and edge cases
