import pytest
from unittest.mock import patch
from flows.base import BaseFlow
from flows.base import FlowValidationError
from helpers import SessionContext
from unittest.mock import Mock
import logging

class TestBaseFlow():
    @pytest.fixture
    def base_flow(self):
        session_context = SessionContext(dict())
        return BaseFlow("TestFlow", session_context=session_context)

    def test_init(self,base_flow):
        assert base_flow._BaseFlow__flow_name == "TestFlow"

    def test_add_validation_error(self,base_flow):
        base_flow._add_validation_error("Test error message")
        assert base_flow.queued_validation_errors == {"": "Test error message"}

    def test_add_field_validation_error(self,base_flow):
        base_flow._add_field_validation_error("field1", "Test error message")
        assert base_flow.queued_validation_errors == {"field1": "Test error message"}

    def test_add_field_validation_error_existing_field(self,base_flow):
        base_flow.queued_validation_errors = {"field1": "Existing error message"}
        base_flow._add_field_validation_error("field1", "Test error message")
        assert base_flow.queued_validation_errors == {"field1": "Existing error message,Test error message"}

    def test_throw_validation_error(self,base_flow):
        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_validation_error("Test error message")
        assert exc_info.value.error_dict == {"": "Test error message"}

    def test_throw_field_validation_error(self,base_flow):
        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_field_validation_error("field1", "Test error message")
        assert exc_info.value.error_dict == {"field1": "Test error message"}

    def test_throw_queued_validation_errors(self,base_flow):
        base_flow.queued_validation_errors = {"field1": "Test error message"}
        with pytest.raises(FlowValidationError) as exc_info:
            base_flow._throw_queued_validation_errors()
        assert exc_info.value.error_dict == {"field1": "Test error message"}

    def test_log_exception(self,monkeypatch, base_flow):
        logging_error_mock = Mock()
        monkeypatch.setattr(logging, "error", logging_error_mock)
        exception = Exception("Test exception")
        base_flow._log_exception(exception)
        logging_error_mock.assert_called_once_with("TestFlow Test exception")

    def test_log_message(self,monkeypatch, base_flow):
        logging_debug_mock = Mock()
        monkeypatch.setattr(logging, "debug", logging_debug_mock)
        base_flow._log_message("Test message")
        logging_debug_mock.assert_called_once_with("TestFlow Test message")