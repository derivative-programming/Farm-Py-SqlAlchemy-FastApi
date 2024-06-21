# business/plant.py

"""
This module contains the PlantBusObj class,
which represents the business object for a Plant.
"""

from .plant_fluent import PlantFluentBusObj


class PlantBusObj(PlantFluentBusObj):
    """
    This class represents the business object for a Plant.
    It requires a valid session context for initialization.
    """
