# flows/base/tests/flow_validation_error_test.py

"""
    #TODO add comment
"""

import pytest
from flows.base import FlowValidationError

class TestFlowValidationError():
    """
    #TODO add comment
    """

    def test_init_with_message(self):
        """
        #TODO add comment
        """

        exception = FlowValidationError(None, "Test error message", None)
        assert exception.error_dict == {"": "Test error message"}

    def test_init_with_field_name_and_message(self):
        """
        #TODO add comment
        """

        exception = FlowValidationError("field1", "Test error message", None)
        assert exception.error_dict == {"field1": "Test error message"}

    def test_init_with_error_dict(self):
        """
        #TODO add comment
        """

        error_dict = {"field1": "Test error message", "field2": "Another error message"}
        exception = FlowValidationError(None, None, error_dict)
        assert exception.error_dict == error_dict

    def test_raise_flow_validation_error(self):
        """
        #TODO add comment
        """

        with pytest.raises(FlowValidationError) as exc_info:
            raise FlowValidationError("field1", "Test error message", None)
        assert exc_info.value.error_dict == {"field1": "Test error message"}
