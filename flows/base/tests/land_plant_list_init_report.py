import unittest
import uuid
from flows.base import BaseFlowLandPlantListInitReport
from helpers import SessionContext
from models.factories import LandFactory
from decimal import Decimal
from factory import Faker
from django.utils import timezone
from datetime import date, datetime

from models import CurrentRuntime
class BaseFlowLandPlantListInitReportTestCase(unittest.TestCase):
    def setUp(self):
        CurrentRuntime.initialize()
        session_context = SessionContext(dict())
        self.flow = BaseFlowLandPlantListInitReport(session_context)
    def test_process_validation_rules(self):
        land = LandFactory.create()

        # Call the method being tested
        self.flow._process_validation_rules(
            land,

            )
        # Add assertions here to validate the expected behavior
        #TODO add validation checks - is required,
        #TODO add validation checks - is email
        #TODO add validation checks - is phone,
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
    def test_process_security_rules(self):
        land = LandFactory.create()
        # Call the method being tested
        self.flow._process_security_rules(land)
        # Add assertions here to validate the expected behavior
