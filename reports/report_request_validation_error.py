# reports/report_request_validation_error.py

"""
This module contains the definition of the ReportRequestValidationError class.
"""


class ReportRequestValidationError(Exception):
    """
    Exception raised for validation errors in report requests.

    Attributes:
        error_dict (dict): A dictionary containing the
            field name and corresponding error message.
    """

    error_dict: dict

    def __init__(self, field_name: str, message: str):
        """
        Initializes a new instance of the ReportRequestValidationError class.

        Args:
            field_name (str): The name of the field that
                caused the validation error.
            message (str): The error message associated
                with the validation error.
        """

        if field_name is not None and message is not None:
            self.error_dict = {}
            self.error_dict[field_name] = message
            super().__init__(message)
        elif message is not None:
            self.error_dict = {}
            self.error_dict[""] = message
            super().__init__(message)
