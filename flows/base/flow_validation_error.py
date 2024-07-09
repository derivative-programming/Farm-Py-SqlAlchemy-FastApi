# flows/base/flow_validation_error.py  # pylint: disable=duplicate-code # noqa: E501

"""
This module contains the definition of the
FlowValidationError class, which is a custom
exception class for flow validation errors.
"""

UNKNOWN_ERROR_OCCURRED_MESSAGE = "An unknown error occurred."


class FlowValidationError(Exception):
    """
    Custom exception class for flow validation errors.

    Attributes:
        error_dict (dict): Dictionary containing field names and
            their corresponding error messages.
    """
    error_dict: dict

    def __init__(self,
                 field_name: str = None,  # type: ignore
                 message: str = None,  # type: ignore
                 error_dict: dict = None):  # type: ignore
        """
        Initialize a FlowValidationError instance.

        Args:
            field_name (str, optional): Name of the field with the error.
            message (str, optional): Error message for the field.
            error_dict (dict, optional): Dictionary containing field names
                and their corresponding error messages.
            **kwargs: Additional keyword arguments.
        """

        if error_dict is not None:
            self.error_dict = error_dict
            self.message = next(iter(error_dict.values()))
        elif field_name is not None and message is not None:
            self.error_dict = {}
            self.error_dict[field_name] = message
        elif message is not None:
            self.error_dict = {}
            self.error_dict[""] = message
        else:
            self.error_dict = {}
            self.message = UNKNOWN_ERROR_OCCURRED_MESSAGE

        if not hasattr(self, 'message'):
            self.message = self._generate_message()

    def _generate_message(self) -> str:
        """
        Generate a default error message if none is provided.

        Returns:
            str: Generated error message.
        """
        if self.error_dict:
            return next(iter(self.error_dict.values()),
                        UNKNOWN_ERROR_OCCURRED_MESSAGE)
        return UNKNOWN_ERROR_OCCURRED_MESSAGE

    def __str__(self):
        """
        Return the string representation of the exception.

        Returns:
            str: String representation of the error message.
        """
        return self.message
