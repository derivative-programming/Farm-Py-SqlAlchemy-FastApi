import importlib
from helpers.formatting import pascal_to_snake_case


class FlowFactory:
    @staticmethod
    def create_instance(class_name: str):
        try:
            working_class_name = class_name

            working_file_name = class_name

            if class_name.startswith("Flow"):
                working_file_name = class_name[4:]
                working_file_name = \
                    pascal_to_snake_case(working_file_name)
            else:
                working_class_name = f"Flow{class_name}"

            # Dynamically import the module
            module = importlib.import_module(
                f'flows.{working_file_name}')
            # Dynamically get the class from the module
            class_ = getattr(module, working_class_name)
            # Create an instance of the class
            return class_()
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(
                f"Flow Class {class_name} not found: {e}")
