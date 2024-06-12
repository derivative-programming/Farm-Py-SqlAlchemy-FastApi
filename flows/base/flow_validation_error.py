# flows/base/flow_validation_error.py

"""
    #TODO add comment
"""

import uuid
from models import Tac


class FlowValidationError(Exception):
    """
    #TODO add comment
    """
    error_dict: dict

    def __init__(self, field_name: str = None, message: str = None, error_dict: dict = None, **kwargs):
        if error_dict is not None:
            self.error_dict = error_dict
            self.message = next(iter(error_dict.values()))
        elif field_name is not None and message is not None:
            self.error_dict = dict()
            self.error_dict[field_name] = message
        elif message is not None:
            self.error_dict = dict()
            self.error_dict[""] = message
