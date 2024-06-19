# flows/base/tests/base_flow_test.py
# pylint: disable=protected-access

"""
This module contains unit tests for the BaseFlow class.
"""

import logging
from unittest.mock import Mock

import pytest

from flows.base import BaseFlow, FlowValidationError
from helpers import SessionContext

TEST_ERROR_MESSAGE = "Test error message"


class TestBaseFlow():
    """
    This class contains unit tests for the BaseFlow class.
    """

    @pytest.fixture
    def base_flow(self):
        """
        Fixture that returns an instance of BaseFlow for testing.
        """

        session_context = SessionContext(dict())
        return BaseFlow("TestFlow", session_context=session_context)

    def test_init(self, base_flow):
        """
        Test case to verify the initialization of BaseFlow.
        """

        assert base_flow._BaseFlow__flow_name == "TestFlow"

    def test_add_validation_error(self, base_flow):
        """
        Test case to verify the addition of a
        validation error to the BaseFlow.
        """

        base_flow._add_validation_error(TEST_ERROR_MESSAGE)
        assert base_flow.queued_validation_errors == {"": TEST_ERROR_MESSAGE}

    def test_add_field_validation_error(self, base_flow):
        """
        Test case to verify the addition of a field
        validation error to the BaseFlow.
        """

        base_flow._add_field_validation_error(
            "field1", TEST_ERROR_MESSAGE)
        assert base_flow.queued_validation_errors == {
            "field1": TEST_ERROR_MESSAGE}

    def test_add_field_validation_error_existing_field(self, base_flow):
        """
        Test case to verify the addition of a field
        validation error to the BaseFlow
        when the field already has an existing error message.
        """

        base_flow.queued_validation_errors = {
            "field1": "Existing error message"}
        base_flow._add_field_validation_error(
            "field1", TEST_ERROR_MESSAGE)
        assert base_flow.queued_validation_errors == {
            "field1": "Existing error message,Test error message"}

    def test_throw_validation_error(self, base_flow):
        """
        Test case to verify the throwing of a validation
        error from the BaseFlow.
        """

        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_validation_error(TEST_ERROR_MESSAGE)
        assert exc_info.value.error_dict == {"": TEST_ERROR_MESSAGE}

    def test_throw_field_validation_error(self, base_flow):
        """
        Test case to verify the throwing of a field
        validation error from the BaseFlow.
        """

        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_field_validation_error(
                "field1",
                TEST_ERROR_MESSAGE
            )
        assert exc_info.value.error_dict == {
            "field1": TEST_ERROR_MESSAGE}

    def test_throw_queued_validation_errors(self, base_flow):
        """
        Test case to verify the throwing of all queued
        validation errors from the BaseFlow.
        """

        base_flow.queued_validation_errors = {
            "field1": TEST_ERROR_MESSAGE}
        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_queued_validation_errors()
        assert exc_info.value.error_dict == {
            "field1": TEST_ERROR_MESSAGE}

    def test_log_exception(self, monkeypatch, base_flow):
        """
        Test case to verify the logging of an exception in the BaseFlow.
        """

        logging_error_mock = Mock()
        monkeypatch.setattr(logging, "error", logging_error_mock)
        exception = Exception("Test exception")
        base_flow._log_exception(exception)
        logging_error_mock.assert_called_once_with("TestFlow Test exception")

    def test_log_message(self, monkeypatch, base_flow):
        """
        Test case to verify the logging of a message in the BaseFlow.
        """

        logging_debug_mock = Mock()
        monkeypatch.setattr(logging, "debug", logging_debug_mock)
        base_flow._log_message("Test message")
        logging_debug_mock.assert_called_once_with("TestFlow Test message")
