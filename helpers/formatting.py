# helpers/formatting.py

"""
    #TODO add comment
"""


def snake_to_camel(snake_str: str) -> str:
    """
        #TODO add comment
    """

    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one,
    # join them together, and prepend the first component.
    return components[0] + ''.join(x.capitalize() for x in components[1:])
