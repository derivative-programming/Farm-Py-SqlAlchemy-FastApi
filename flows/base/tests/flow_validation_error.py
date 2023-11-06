# your_app/tests.py
from django.test import TestCase
from flows.base import FlowValidationError

class TestFlowValidationError(TestCase):
    def test_init_with_message(self):
        exception = FlowValidationError(None, "Test error message", None)
        self.assertEqual(exception.error_dict, {"": "Test error message"})

    def test_init_with_field_name_and_message(self):
        exception = FlowValidationError("field1", "Test error message", None)
        self.assertEqual(exception.error_dict, {"field1": "Test error message"})

    def test_init_with_error_dict(self):
        error_dict = {"field1": "Test error message", "field2": "Another error message"}
        exception = FlowValidationError(None, None, error_dict)
        self.assertEqual(exception.error_dict, error_dict)

    def test_raise_flow_validation_error(self):
        with self.assertRaises(FlowValidationError) as context:
            raise FlowValidationError("field1", "Test error message", None)
        self.assertEqual(context.exception.error_dict, {"field1": "Test error message"})
