# report_request_validation_error.py

"""
    #TODO add comment
"""


class ReportRequestValidationError(Exception):
    """
    #TODO add comment
    """
    error_dict: dict

    def __init__(self, field_name: str, message: str):
        if field_name is not None and message is not None:
            self.error_dict = dict()
            self.error_dict[field_name] = message
            super().__init__(message)
        elif message is not None:
            self.error_dict = dict()
            self.error_dict[""] = message
            super().__init__(message)
