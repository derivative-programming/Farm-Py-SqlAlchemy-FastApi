# flows/base/base_flow.py

"""
This module contains the BaseFlow class which serves
as the base class for all flows.
"""

import logging

from helpers import SessionContext

from .flow_validation_error import FlowValidationError
from .log_severity import LogSeverity


class BaseFlow():
    """
    BaseFlow is the base class for all flows in the application.
    It provides common functionality and methods
    that can be used by derived flow classes.
    """

    __flow_name = ""
    queued_validation_errors: dict
    _session_context: SessionContext

    def __init__(self, flow_name: str, session_context: SessionContext):
        self._session_context = session_context
        self.__flow_name = flow_name
        self.queued_validation_errors = {}

    def _add_validation_error(self, message: str):
        """
        Adds a validation error to the queued validation errors.
        """
        self._add_field_validation_error("", message)

    def _add_field_validation_error(
            self,
            field_name: str = "",
            message: str = ""):
        """
        Adds a field-specific validation error to the queued validation errors.
        """
        if field_name in self.queued_validation_errors:
            current_val = self.queued_validation_errors[field_name]
            self.queued_validation_errors[field_name] = (
                current_val + ',' + message)
        else:
            self.queued_validation_errors[field_name] = message

    def _throw_validation_error(self, message: str):
        """
        Throws a validation error with the specified message.
        """
        self._throw_field_validation_error("", message)

    def _throw_field_validation_error(self, field_name: str, message: str):
        """
        Throws a field-specific validation error
        with the specified field name and message.
        """
        raise FlowValidationError(field_name, message)

    def _throw_queued_validation_errors(self):
        """
        Throws all the queued validation errors
        as a single FlowValidationError.
        """
        if len(self.queued_validation_errors) > 0:
            raise FlowValidationError(error_dict=self.queued_validation_errors)

    def _log_exception(self, ex: Exception):
        """
        Logs an exception with the specified severity level.
        """
        self._log_message_and_severity(
            LogSeverity.ERROR_OCCURRED,
            str(ex))

    def _log_message_and_severity(
        self,
        log_severity: LogSeverity,
        message: str
    ):
        """
        Logs a message with the specified severity level.
        """
        log_message = self.__flow_name + " " + message

        match log_severity:
            case LogSeverity.ERROR_OCCURRED:
                logging.error(log_message)
            case LogSeverity.WARNING:
                logging.critical(log_message)
            case LogSeverity.INFORMATION_LOW_DETAIL:
                logging.info(log_message)
            case LogSeverity.INFORMATION_MID_DETAIL:
                logging.info(log_message)
            case LogSeverity.INFORMATION_HIGH_DETAIL:
                logging.debug(log_message)

    def _log_message(self, message: str):
        """
        Logs a message with high detail information level.
        """
        self._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            message
        )
