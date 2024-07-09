# flows/base/tests/flow_validation_error_test.py  # pylint: disable=duplicate-code # noqa: E501

"""
This module contains unit tests for the FlowValidationError class.
"""

import pytest
from flows.base import FlowValidationError

TEST_ERROR_MESSAGE = "Test error message"


class TestFlowValidationError():
    """
    Unit tests for the FlowValidationError class.
    """

    def test_init_with_message(self):
        """
        Test the initialization of FlowValidationError with a message.
        """

        exception = FlowValidationError(message=TEST_ERROR_MESSAGE)
        assert exception.error_dict == {"": TEST_ERROR_MESSAGE}

    def test_init_with_field_name_and_message(self):
        """
        Test the initialization of FlowValidationError
        with a field name and message.
        """

        exception = FlowValidationError("field1", TEST_ERROR_MESSAGE)
        assert exception.error_dict == {"field1": TEST_ERROR_MESSAGE}

    def test_init_with_error_dict(self):
        """
        Test the initialization of FlowValidationError
        with an error dictionary.
        """

        error_dict = {
            "field1": TEST_ERROR_MESSAGE,
            "field2": "Another error message"}
        exception = FlowValidationError(error_dict=error_dict)
        assert exception.error_dict == error_dict

    def test_raise_flow_validation_error(self):
        """
        Test raising a FlowValidationError.
        """

        with pytest.raises(FlowValidationError) as exc_info:
            raise FlowValidationError("field1", TEST_ERROR_MESSAGE)
        assert exc_info.value.error_dict == {"field1": TEST_ERROR_MESSAGE}
