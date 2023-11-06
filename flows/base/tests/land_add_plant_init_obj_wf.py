import unittest 
from flows.base import BaseFlowLandAddPlantInitObjWF
from helpers import SessionContext
from models.factories import LandFactory
from decimal import Decimal
from models import CurrentRuntime
class BaseFlowLandAddPlantInitObjWFTestCase(unittest.TestCase):
    def setUp(self):
        CurrentRuntime.initialize()
        session_context = SessionContext(dict())
        self.flow = BaseFlowLandAddPlantInitObjWF(session_context)
    def test_process_validation_rules(self): 
        land = LandFactory.create() 

        # Call the method being tested
        self.flow._process_validation_rules(
            land,

            )
        # Add assertions here to validate the expected behavior
    def test_process_security_rules(self): 
        land = LandFactory.create() 
        # Call the method being tested
        self.flow._process_security_rules(land)
        # Add assertions here to validate the expected behavior
