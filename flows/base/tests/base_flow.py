from django.test import TestCase
from unittest.mock import patch
from flows.base import BaseFlow
from flows.base import FlowValidationError
from helpers import SessionContext

class TestBaseFlow(TestCase):
    def setUp(self):
        session_context = SessionContext(dict())
        self.base_flow = BaseFlow("TestFlow",session_context=session_context)

    def test_init(self):
        self.assertEqual(self.base_flow._BaseFlow__flow_name, "TestFlow")

    def test_add_validation_error(self):
        self.base_flow._add_validation_error("Test error message")
        self.assertEqual(self.base_flow.queued_validation_errors, {"": "Test error message"})

    def test_add_field_validation_error(self):
        self.base_flow._add_field_validation_error("field1", "Test error message")
        self.assertEqual(self.base_flow.queued_validation_errors, {"field1": "Test error message"})

    def test_add_field_validation_error_existing_field(self):
        self.base_flow.queued_validation_errors = {"field1": "Existing error message"}
        self.base_flow._add_field_validation_error("field1", "Test error message")
        self.assertEqual(self.base_flow.queued_validation_errors, {"field1": "Existing error message,Test error message"})

    def test_throw_validation_error(self):
        with self.assertRaises(FlowValidationError) as context:
            self.base_flow._throw_validation_error("Test error message")
        self.assertEqual(context.exception.error_dict, {"": "Test error message"})

    def test_throw_field_validation_error(self):
        with self.assertRaises(FlowValidationError) as context:
            self.base_flow._throw_field_validation_error("field1", "Test error message")
        self.assertEqual(context.exception.error_dict, {"field1": "Test error message"})

    def test_throw_queued_validation_errors(self):
        self.base_flow.queued_validation_errors = {"field1": "Test error message"}
        with self.assertRaises(FlowValidationError) as context:
            self.base_flow._throw_queued_validation_errors()
        self.assertEqual(context.exception.error_dict, {"field1": "Test error message"})

    @patch("logging.error")
    def test_log_exception(self, logging_error_mock):
        exception = Exception("Test exception")
        self.base_flow._log_exception(exception)
        logging_error_mock.assert_called_once_with("TestFlow Test exception")

    @patch("logging.debug")
    def test_log_message(self, logging_debug_mock):
        self.base_flow._log_message("Test message")
        logging_debug_mock.assert_called_once_with("TestFlow Test message")
