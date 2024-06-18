# flows/base/tests/flow_validation_error_test.py

"""
    #TODO add comment
"""

import pytest
from flows.base import FlowValidationError

TEST_ERROR_MESSAGE = "Test error message"


class TestFlowValidationError():
    """
    #TODO add comment
    """

    def test_init_with_message(self):
        """
        #TODO add comment
        """

        exception = FlowValidationError(message=TEST_ERROR_MESSAGE)
        assert exception.error_dict == {"": TEST_ERROR_MESSAGE}

    def test_init_with_field_name_and_message(self):
        """
        #TODO add comment
        """

        exception = FlowValidationError("field1", TEST_ERROR_MESSAGE)
        assert exception.error_dict == {"field1": TEST_ERROR_MESSAGE}

    def test_init_with_error_dict(self):
        """
        #TODO add comment
        """

        error_dict = {
            "field1": TEST_ERROR_MESSAGE,
            "field2": "Another error message"}
        exception = FlowValidationError(error_dict=error_dict)
        assert exception.error_dict == error_dict

    def test_raise_flow_validation_error(self):
        """
        #TODO add comment
        """

        with pytest.raises(FlowValidationError) as exc_info:
            raise FlowValidationError("field1", TEST_ERROR_MESSAGE)
        assert exc_info.value.error_dict == {"field1": TEST_ERROR_MESSAGE}
