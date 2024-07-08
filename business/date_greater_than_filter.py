# business/date_greater_than_filter.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the DateGreaterThanFilterBusObj class,
which represents the business object for a DateGreaterThanFilter.
"""

from typing import List
from helpers.session_context import SessionContext
import models
from models import DateGreaterThanFilter
import managers as managers_and_enums  # noqa: F401
from .date_greater_than_filter_fluent import DateGreaterThanFilterFluentBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DateGreaterThanFilter object is not initialized")


class DateGreaterThanFilterBusObj(DateGreaterThanFilterFluentBusObj):
    """
    This class represents the business object for a DateGreaterThanFilter.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DateGreaterThanFilter]
    ):
        """
        Convert a list of DateGreaterThanFilter
        objects to a list of
        DateGreaterThanFilterBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DateGreaterThanFilter]): The
                list of DateGreaterThanFilter objects to convert.

        Returns:
            List[DateGreaterThanFilterBusObj]: The
                list of converted DateGreaterThanFilterBusObj
                objects.
        """
        result = []

        for date_greater_than_filter in obj_list:
            date_greater_than_filter_bus_obj = DateGreaterThanFilterBusObj(
                session_context)

            date_greater_than_filter_bus_obj.load_from_obj_instance(
                date_greater_than_filter)

            result.append(date_greater_than_filter_bus_obj)

        return result
    # description
    # displayOrder
    # isActive
    # lookupEnumName
    # name
    # PacID

    async def get_pac_id_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based
        on the pac_id.

        Returns:
            An instance of the Pac model
            representing the related pac.

        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj

    async def get_pac_id_bus_obj(self):
        """
        Retrieves the related Pac
        business object based
        on the pac_id.

        Returns:
            An instance of the Pac
            business object
            representing the related pac.

        """
        from .pac import PacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = PacBusObj(self._session_context)
        await bus_obj.load_from_id(self.pac_id)
        return bus_obj

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start
    @property
    def lookup_enum(self) -> managers_and_enums.DateGreaterThanFilterEnum:
        """
        Returns the corresponding DateGreaterThanFilterEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the date_greater_than_filter
                attribute is not initialized.
        Returns:
            managers_and_enums.DateGreaterThanFilterEnum:
                The corresponding DateGreaterThanFilterEnum value.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.DateGreaterThanFilterEnum[
                self.date_greater_than_filter.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        date_greater_than_filter_enum:
            managers_and_enums.DateGreaterThanFilterEnum
    ):
        """
        Load date_greater_than_filter data from dictionary.
        :param date_greater_than_filter_dict: Dictionary
            containing date_greater_than_filter data.
        :raises ValueError: If date_greater_than_filter_dict
            is not a dictionary or if no
            date_greater_than_filter data is found.
        """
        if not isinstance(
            date_greater_than_filter_enum,
            managers_and_enums.DateGreaterThanFilterEnum
        ):
            raise ValueError("date_greater_than_filter_enum must be a enum")
        date_greater_than_filter_manager =  \
            managers_and_enums.DateGreaterThanFilterManager(
                self._session_context
            )
        self.date_greater_than_filter = await (
            date_greater_than_filter_manager.
            from_enum(date_greater_than_filter_enum)
        )

##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End
