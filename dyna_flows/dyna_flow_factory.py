# dyna_flows/dyna_flow_factory.py  # pylint: disable=duplicate-code
"""
This module provides a factory class for creating instances of
DynaFlow classes dynamically.
"""
import importlib
from helpers.formatting import pascal_to_snake_case


class DynaFlowFactory:  # pylint: disable=too-few-public-methods
    """
    This class provides a factory for creating instances of
    DynaFlow classes dynamically.
    """
    @staticmethod
    def create_instance(class_name: str):
        """
        Create an instance of a DynaFlow class dynamically
        based on the specified class name.
        """
        try:
            working_class_name = class_name

            working_file_name = class_name

            if class_name.startswith("DynaFlow"):
                working_file_name = class_name[8:]
                working_file_name = \
                    pascal_to_snake_case(working_file_name)
            else:
                working_file_name = \
                    pascal_to_snake_case(working_class_name)
                working_class_name = f"DynaFlow{class_name}"

            # Dynamically import the module
            module = importlib.import_module(
                f'dyna_flows.{working_file_name}')
            # Dynamically get the class from the module
            class_ = getattr(module, working_class_name)
            # Create an instance of the class
            return class_()
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(
                f"Dyna Flow Class {class_name} not found: {e}")
