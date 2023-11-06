import unittest
import uuid
from flows.base import BaseFlowTacLogin
from helpers import SessionContext
from models.factories import TacFactory
from decimal import Decimal
from factory import Faker
from django.utils import timezone
from datetime import date, datetime

from models import CurrentRuntime
class BaseFlowTacLoginTestCase(unittest.TestCase):
    def setUp(self):
        CurrentRuntime.initialize()
        session_context = SessionContext(dict())
        self.flow = BaseFlowTacLogin(session_context)
    def test_process_validation_rules(self):
        tac = TacFactory.create()
        email:str = Faker('email')
        password:str = Faker('sentence', nb_words=4)
        # Call the method being tested
        self.flow._process_validation_rules(
            tac,
            email,
            password,
            )
        # Add assertions here to validate the expected behavior
        #TODO add validation checks - is required,
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
    def test_process_security_rules(self):
        tac = TacFactory.create()
        # Call the method being tested
        self.flow._process_security_rules(tac)
        # Add assertions here to validate the expected behavior
