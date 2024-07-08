# flows/flow_factory.py  # pylint: disable=duplicate-code
"""
This module contains the FlowFactory class, which
is responsible for dynamically creating instances
of flow classes based on the provided class name.
"""

import importlib
from helpers.formatting import pascal_to_snake_case
from helpers.session_context import SessionContext


class FlowFactory:  # pylint: disable=too-few-public-methods
    @staticmethod
    def create_instance(class_name: str, session_context: SessionContext):
        """
        Create an instance of the specified flow class.

        Args:
            class_name (str): The name of the flow
                class to create an instance of.
            session_context (SessionContext): The session
                to pass to the flow class constructor.

        Returns:
            object: An instance of the specified flow class.

        Raises:
            ValueError: If the specified flow class is not found.
        """
        try:
            working_class_name = class_name

            working_file_name = class_name

            if class_name.startswith("Flow"):
                working_file_name = class_name[4:]
                working_file_name = \
                    pascal_to_snake_case(working_file_name)
            else:
                working_file_name = \
                    pascal_to_snake_case(class_name)
                working_class_name = f"Flow{class_name}"

            # Dynamically import the module
            module = importlib.import_module(
                f'flows.{working_file_name}')
            # Dynamically get the class from the module
            class_ = getattr(module, working_class_name)
            # Create an instance of the class
            return class_(session_context)
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(
                f"Flow Class {class_name} not found: {e}")
