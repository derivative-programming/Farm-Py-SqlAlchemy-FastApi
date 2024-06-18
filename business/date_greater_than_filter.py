# business/date_greater_than_filter.py
# pylint: disable=unused-import

"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DateGreaterThanFilter object is not initialized")


class DateGreaterThanFilterInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass


class DateGreaterThanFilterBusObj(BaseBusObj):
    """
    This class represents the business object for a DateGreaterThanFilter.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.date_greater_than_filter = DateGreaterThanFilter()

    @property
    def date_greater_than_filter_id(self):
        """
        Get the date_greater_than_filter ID from the
        DateGreaterThanFilter object.
        :return: The date_greater_than_filter ID.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.date_greater_than_filter_id

    # @date_greater_than_filter_id.setter
    # def date_greater_than_filter_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("date_greater_than_filter_id must be a int.")
    #     self.date_greater_than_filter.date_greater_than_filter_id = value

    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.date_greater_than_filter.code = value

    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.date_greater_than_filter.last_change_code = value

    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.date_greater_than_filter.insert_user_id = value

    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.date_greater_than_filter:
    #         raise AttributeError(
    #             NOT_INITIALIZED_ERROR_MESSAGE
    #         )
    #     self.insert_user_id = value
    #     return self

    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.date_greater_than_filter.last_update_user_id = value

    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset

    # dayCount
    @property
    def day_count(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.day_count

    @day_count.setter
    def day_count(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "day_count must be an integer")
        self.date_greater_than_filter.day_count = value

    # def set_prop_day_count(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.day_count = value
    #     return self

    # description
    @property
    def description(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.description is None:
            return ""
        return self.date_greater_than_filter.description

    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.date_greater_than_filter.description = value

    # def set_prop_description(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.description = value
    #     return self

    # displayOrder
    @property
    def display_order(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.display_order

    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.date_greater_than_filter.display_order = value

    # def set_prop_display_order(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.display_order = value
    #     return self

    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.date_greater_than_filter.is_active = value

    # def set_prop_is_active(self, value: bool):
    #     """
    #     #TODO add comment
    #     """
    #     self.is_active = value
    #     return self

    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.lookup_enum_name is None:
            return ""
        return self.date_greater_than_filter.lookup_enum_name

    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.date_greater_than_filter.lookup_enum_name = value

    # def set_prop_lookup_enum_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.lookup_enum_name = value
    #     return self

    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.name is None:
            return ""
        return self.date_greater_than_filter.name

    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.date_greater_than_filter.name = value

    # def set_prop_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.name = value
    #     return self

    # PacID
# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    @property
    def pac_id(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.date_greater_than_filter.pac_id = value

    # def set_prop_pac_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.pac_id = value
    #     return self

    @property
    def pac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.pac_code_peek

    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.date_greater_than_filter.pac_code_peek = value

# endset
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.date_greater_than_filter.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.date_greater_than_filter.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load date_greater_than_filter data from JSON string.
        :param json_data: JSON string containing
            date_greater_than_filter data.
        :raises ValueError: If json_data is not a string
            or if no date_greater_than_filter data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        self.date_greater_than_filter = (
            date_greater_than_filter_manager.from_json(
                json_data
            )
        )
        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load date_greater_than_filter data from UUID code.
        :param code: UUID code for loading a specific
            date_greater_than_filter.
        :raises ValueError: If code is not a UUID or
            if no date_greater_than_filter data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        date_greater_than_filter_manager = (
            DateGreaterThanFilterManager(
                self._session_context
            )
        )
        date_greater_than_filter_obj = await (
            date_greater_than_filter_manager
            .get_by_code(code)
        )
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self

    async def load_from_id(
        self,
        date_greater_than_filter_id: int
    ):
        """
        Load date_greater_than_filter data from date_greater_than_filter ID.
        :param date_greater_than_filter_id: Integer ID
            for loading a specific date_greater_than_filter.
        :raises ValueError: If date_greater_than_filter_id
            is not an integer or if no date_greater_than_filter
            data is found.
        """
        if not isinstance(date_greater_than_filter_id, int):
            raise ValueError("date_greater_than_filter_id must be an integer")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        date_greater_than_filter_obj = await (
            date_greater_than_filter_manager
            .get_by_id(
                date_greater_than_filter_id
            )
        )
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self

    async def load_from_obj_instance(
        self,
        obj_instance: DateGreaterThanFilter
    ):
        """
        Use the provided DateGreaterThanFilter instance.
        :param obj_instance:Instance
            of the DateGreaterThanFilter class.
        :raises ValueError: If obj_instance
            is not an instance of DateGreaterThanFilter.
        """
        if not isinstance(
            obj_instance,
            DateGreaterThanFilter
        ):
            raise ValueError(
                "obj_instance must be "
                "an instance of DateGreaterThanFilter")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        obj_instance_date_greater_than_filter_id = (
            obj_instance.date_greater_than_filter_id
        )
        date_greater_than_filter_obj = await (
            date_greater_than_filter_manager
            .get_by_id(
                obj_instance_date_greater_than_filter_id
            )
        )
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self

    async def load_from_dict(
        self,
        date_greater_than_filter_dict: dict
    ):
        """
        Load date_greater_than_filter data from dictionary.
        :param date_greater_than_filter_dict: Dictionary
            containing date_greater_than_filter data.
        :raises ValueError: If date_greater_than_filter_dict is
            not a dictionary or if no date_greater_than_filter data is found.
        """
        if not isinstance(date_greater_than_filter_dict, dict):
            raise ValueError(
                "date_greater_than_filter_dict must be a dictionary"
            )
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        self.date_greater_than_filter = (
            date_greater_than_filter_manager
            .from_dict(
                date_greater_than_filter_dict
            )
        )
        return self

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start

    @property
    def lookup_enum(self) -> managers_and_enums.DateGreaterThanFilterEnum:
        """
        #TODO add comment
        """

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

        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        self.date_greater_than_filter = await (
            date_greater_than_filter_manager.
            from_enum(date_greater_than_filter_enum)
        )

##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End

    async def refresh(self):
        """
        #TODO add comment
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        self.date_greater_than_filter = await (
            date_greater_than_filter_manager.
            refresh(self.date_greater_than_filter)
        )
        return self

    def is_valid(self):
        """
        #TODO add comment
        """
        return self.date_greater_than_filter is not None

    def to_dict(self):
        """
        #TODO add comment
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        return date_greater_than_filter_manager.to_dict(
            self.date_greater_than_filter
        )

    def to_json(self):
        """
        #TODO add comment
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        return date_greater_than_filter_manager.to_json(
            self.date_greater_than_filter
        )

    async def save(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(
                self._session_context
            )
            self.date_greater_than_filter = await (
                date_greater_than_filter_manager.update(
                    self.date_greater_than_filter)
            )
        if self.date_greater_than_filter.date_greater_than_filter_id == 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(
                self._session_context
            )
            self.date_greater_than_filter = await (
                date_greater_than_filter_manager.add(
                    self.date_greater_than_filter
                )
            )
        return self

    async def delete(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(
                self._session_context
            )
            await date_greater_than_filter_manager.delete(
                self.date_greater_than_filter.date_greater_than_filter_id
            )
            self.date_greater_than_filter = None

    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.date_greater_than_filter.day_count = random.randint(0, 100)
        self.date_greater_than_filter.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.date_greater_than_filter.display_order = random.randint(0, 100)
        self.date_greater_than_filter.is_active = random.choice([True, False])
        self.date_greater_than_filter.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.date_greater_than_filter.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.date_greater_than_filter.pac_id = random.randint(0, 100)
# endset
        return self

    def get_date_greater_than_filter_obj(self) -> DateGreaterThanFilter:
        """
        #TODO add comment
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter

    def is_equal(
        self,
        date_greater_than_filter: DateGreaterThanFilter
    ) -> bool:
        """
        #TODO add comment
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        my_date_greater_than_filter = self.get_date_greater_than_filter_obj()
        return date_greater_than_filter_manager.is_equal(
            date_greater_than_filter,
            my_date_greater_than_filter
        )

# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj

# endset

    def get_obj(self) -> DateGreaterThanFilter:
        """
        #TODO add comment
        """
        return self.date_greater_than_filter

    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "date_greater_than_filter"

    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.date_greater_than_filter_id

    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        return self.get_pac_id_rel_obj()

# endset

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DateGreaterThanFilter]
    ):
        """
        #TODO add comment
        """
        result = list()
        for obj_instance in obj_list:

            date_greater_than_filter_bus_obj = DateGreaterThanFilterBusObj(
                session_context)

            await date_greater_than_filter_bus_obj.load_from_obj_instance(
                obj_instance)

            result.append(date_greater_than_filter_bus_obj)
        return result
