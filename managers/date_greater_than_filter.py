# models/managers/date_greater_than_filter.py
# pylint: disable=unused-import
"""
This module contains the DateGreaterThanFilterManager class, which is
responsible for managing date_greater_than_filters in the system.
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.date_greater_than_filter import DateGreaterThanFilter
from models.serialization_schema.date_greater_than_filter import DateGreaterThanFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class DateGreaterThanFilterNotFoundError(Exception):
    """
    Exception raised when a specified date_greater_than_filter is not found.
    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DateGreaterThanFilter not found"):
        self.message = message
        super().__init__(self.message)


##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start


class DateGreaterThanFilterEnum(Enum):
    """
    Represents an enumeration of
    Date Greater Than Filter options.
    """
    UNKNOWN = 'Unknown'
    LAST_24_HOURS = 'Last_24_Hours'
    LAST_7_DAYS = 'Last_7_Days'
    LAST_30_DAYS = 'Last_30_Days'
    LAST_90_DAYS = 'Last_90_Days'
    LAST_365_DAYS = 'Last_365_Days'

##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End
class DateGreaterThanFilterManager:
    """
    The DateGreaterThanFilterManager class is responsible for managing date_greater_than_filters in the system.
    It provides methods for adding, updating, deleting, and retrieving date_greater_than_filters.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the DateGreaterThanFilterManager class.
        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.
        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self, value: uuid.UUID):
        """
        Converts a UUID value to a model UUID.
        Args:
            value (uuid.UUID): The UUID value to convert.
        Returns:
            The converted UUID value.
        """
        # Conditionally set the UUID column type
        return value


##GENTrainingBlock[caseIsLookupObject]Start
##GENLearn[isLookup=true]Start

    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item

    async def initialize(self):
        """
        Initializes the DateGreaterThanFilterManager.
        This method initializes the DateGreaterThanFilterManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("DateGreaterThanFilterManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(DateGreaterThanFilterEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.LAST_24_HOURS) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 24 Hours"
            item.lookup_enum_name = "Last_24_Hours"
            item.description = "Last 24 Hours"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.LAST_7_DAYS) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 7 Days"
            item.lookup_enum_name = "Last_7_Days"
            item.description = "Last 7 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.LAST_30_DAYS) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 30 Days"
            item.lookup_enum_name = "Last_30_Days"
            item.description = "Last 30 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.LAST_90_DAYS) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 90 Days"
            item.lookup_enum_name = "Last_90_Days"
            item.description = "Last 90 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.LAST_365_DAYS) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 365 Days"
            item.lookup_enum_name = "Last_365_Days"
            item.description = "Last 365 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
# endset
        logging.info("DateGreaterThanFilterManager.Initialize end")

    async def from_enum(
        self,
        enum_val: DateGreaterThanFilterEnum
    ) -> DateGreaterThanFilter:
        """
        Returns a DateGreaterThanFilter object
        based on the provided enum value.
        Args:
            enum_val (DateGreaterThanFilterEnum):
                The enum value representing the filter.
        Returns:
            DateGreaterThanFilter:
                The DateGreaterThanFilter object
                matching the enum value.
        """
        query_filter = (
            DateGreaterThanFilter._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
##GENLearn[isLookup=true]End
##GENTrainingBlock[caseIsLookupObject]End

    async def build(self, **kwargs) -> DateGreaterThanFilter:
        """
        Builds a new DateGreaterThanFilter object with the specified attributes.
        Args:
            **kwargs: The attributes of the date_greater_than_filter.
        Returns:
            DateGreaterThanFilter: The newly created DateGreaterThanFilter object.
        """
        logging.info("DateGreaterThanFilterManager.build")
        return DateGreaterThanFilter(**kwargs)
    async def add(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        """
        Adds a new date_greater_than_filter to the system.
        Args:
            date_greater_than_filter (DateGreaterThanFilter): The date_greater_than_filter to add.
        Returns:
            DateGreaterThanFilter: The added date_greater_than_filter.
        """
        logging.info("DateGreaterThanFilterManager.add")
        date_greater_than_filter.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        date_greater_than_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(date_greater_than_filter)
        await self._session_context.session.flush()
        return date_greater_than_filter
    def _build_query(self):
        """
        Builds the base query for retrieving date_greater_than_filters.
        Returns:
            The base query for retrieving date_greater_than_filters.
        """
        logging.info("DateGreaterThanFilterManager._build_query")
        query = select(
            DateGreaterThanFilter,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DateGreaterThanFilter._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DateGreaterThanFilter._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[DateGreaterThanFilter]:
        """
        Runs the query to retrieve date_greater_than_filters from the database.
        Args:
            query_filter: The filter to apply to the query.
        Returns:
            List[DateGreaterThanFilter]: The list of date_greater_than_filters that match the query.
        """
        logging.info("DateGreaterThanFilterManager._run_query")
        date_greater_than_filter_query_all = self._build_query()
        if query_filter is not None:
            query = date_greater_than_filter_query_all.filter(query_filter)
        else:
            query = date_greater_than_filter_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            date_greater_than_filter = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            date_greater_than_filter.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(date_greater_than_filter)
        return result
    def _first_or_none(
        self,
        date_greater_than_filter_list: List['DateGreaterThanFilter']
    ) -> Optional['DateGreaterThanFilter']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.
        Args:
            date_greater_than_filter_list (List[DateGreaterThanFilter]): The list to retrieve
                the first element from.
        Returns:
            Optional[DateGreaterThanFilter]: The first element of the list
                if it exists, otherwise None.
        """
        return (
            date_greater_than_filter_list[0]
            if date_greater_than_filter_list
            else None
        )
    async def get_by_id(self, date_greater_than_filter_id: int) -> Optional[DateGreaterThanFilter]:
        """
        Retrieves a date_greater_than_filter by its ID.
        Args:
            date_greater_than_filter_id (int): The ID of the date_greater_than_filter to retrieve.
        Returns:
            Optional[DateGreaterThanFilter]: The retrieved date_greater_than_filter, or None if not found.
        """
        logging.info(
            "DateGreaterThanFilterManager.get_by_id start date_greater_than_filter_id: %s",
            str(date_greater_than_filter_id))
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(
                "The date_greater_than_filter_id must be an integer, "
                f"got {type(date_greater_than_filter_id)} instead.")
        query_filter = (
            DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[DateGreaterThanFilter]:
        """
        Retrieves a date_greater_than_filter by its code.
        Args:
            code (uuid.UUID): The code of the date_greater_than_filter to retrieve.
        Returns:
            Optional[DateGreaterThanFilter]: The retrieved date_greater_than_filter, or None if not found.
        """
        logging.info("DateGreaterThanFilterManager.get_by_code %s", code)
        query_filter = DateGreaterThanFilter._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, date_greater_than_filter: DateGreaterThanFilter, **kwargs) -> Optional[DateGreaterThanFilter]:
        """
        Updates a date_greater_than_filter with the specified attributes.
        Args:
            date_greater_than_filter (DateGreaterThanFilter): The date_greater_than_filter to update.
            **kwargs: The attributes to update.
        Returns:
            Optional[DateGreaterThanFilter]: The updated date_greater_than_filter, or None if not found.
        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DateGreaterThanFilterManager.update")
        property_list = DateGreaterThanFilter.property_list()
        if date_greater_than_filter:
            date_greater_than_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(date_greater_than_filter, key, value)
            await self._session_context.session.flush()
        return date_greater_than_filter
    async def delete(self, date_greater_than_filter_id: int):
        """
        Deletes a date_greater_than_filter by its ID.
        Args:
            date_greater_than_filter_id (int): The ID of the date_greater_than_filter to delete.
        Raises:
            TypeError: If the date_greater_than_filter_id is not an integer.
            DateGreaterThanFilterNotFoundError: If the date_greater_than_filter with the
                specified ID is not found.
        """
        logging.info("DateGreaterThanFilterManager.delete %s", date_greater_than_filter_id)
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(
                f"The date_greater_than_filter_id must be an integer, "
                f"got {type(date_greater_than_filter_id)} instead."
            )
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        if not date_greater_than_filter:
            raise DateGreaterThanFilterNotFoundError(f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
        await self._session_context.session.delete(date_greater_than_filter)
        await self._session_context.session.flush()
    async def get_list(self) -> List[DateGreaterThanFilter]:
        """
        Retrieves a list of all date_greater_than_filters.
        Returns:
            List[DateGreaterThanFilter]: The list of date_greater_than_filters.
        """
        logging.info("DateGreaterThanFilterManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, date_greater_than_filter: DateGreaterThanFilter) -> str:
        """
        Serializes a DateGreaterThanFilter object to a JSON string.
        Args:
            date_greater_than_filter (DateGreaterThanFilter): The date_greater_than_filter to serialize.
        Returns:
            str: The JSON string representation of the date_greater_than_filter.
        """
        logging.info("DateGreaterThanFilterManager.to_json")
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        return json.dumps(date_greater_than_filter_data)
    def to_dict(self, date_greater_than_filter: DateGreaterThanFilter) -> Dict[str, Any]:
        """
        Serializes a DateGreaterThanFilter object to a dictionary.
        Args:
            date_greater_than_filter (DateGreaterThanFilter): The date_greater_than_filter to serialize.
        Returns:
            Dict[str, Any]: The dictionary representation of the date_greater_than_filter.
        """
        logging.info("DateGreaterThanFilterManager.to_dict")
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        assert isinstance(date_greater_than_filter_data, dict)
        return date_greater_than_filter_data
    async def from_json(self, json_str: str) -> DateGreaterThanFilter:
        """
        Deserializes a JSON string into a DateGreaterThanFilter object.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            DateGreaterThanFilter: The deserialized DateGreaterThanFilter object.
        """
        logging.info("DateGreaterThanFilterManager.from_json")
        schema = DateGreaterThanFilterSchema()
        data = json.loads(json_str)
        date_greater_than_filter_dict = schema.load(data)
        # new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict)

        # load or create
        new_date_greater_than_filter = await self.get_by_id(date_greater_than_filter_dict["date_greater_than_filter_id"])
        if new_date_greater_than_filter is None:
            new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict)
            self._session_context.session.add(new_date_greater_than_filter)
        else:
            for key, value in date_greater_than_filter_dict.items():
                setattr(new_date_greater_than_filter, key, value)

        return new_date_greater_than_filter
    async def from_dict(self, date_greater_than_filter_dict: Dict[str, Any]) -> DateGreaterThanFilter:
        """
        Creates a DateGreaterThanFilter instance from a dictionary of attributes.
        Args:
            date_greater_than_filter_dict (Dict[str, Any]): A dictionary
                containing date_greater_than_filter attributes.
        Returns:
            DateGreaterThanFilter: A new DateGreaterThanFilter instance created from the given dictionary.
        """
        logging.info("DateGreaterThanFilterManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_dict_converted = schema.load(date_greater_than_filter_dict)
        # Create a new DateGreaterThanFilter instance using the validated data
        # new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict_converted)

        # load or create
        new_date_greater_than_filter = await self.get_by_id(date_greater_than_filter_dict_converted["date_greater_than_filter_id"])
        if new_date_greater_than_filter is None:
            new_date_greater_than_filter = DateGreaterThanFilter(**date_greater_than_filter_dict_converted)
            self._session_context.session.add(new_date_greater_than_filter)
        else:
            for key, value in date_greater_than_filter_dict_converted.items():
                setattr(new_date_greater_than_filter, key, value)

        return new_date_greater_than_filter
    async def add_bulk(self, date_greater_than_filters: List[DateGreaterThanFilter]) -> List[DateGreaterThanFilter]:
        """
        Adds multiple date_greater_than_filters to the system.
        Args:
            date_greater_than_filters (List[DateGreaterThanFilter]): The list of date_greater_than_filters to add.
        Returns:
            List[DateGreaterThanFilter]: The added date_greater_than_filters.
        """
        logging.info("DateGreaterThanFilterManager.add_bulk")
        for date_greater_than_filter in date_greater_than_filters:
            date_greater_than_filter_id = date_greater_than_filter.date_greater_than_filter_id
            code = date_greater_than_filter.code
            if date_greater_than_filter.date_greater_than_filter_id is not None and date_greater_than_filter.date_greater_than_filter_id > 0:
                raise ValueError(
                    f"DateGreaterThanFilter is already added: {str(code)} {str(date_greater_than_filter_id)}"
                )
            date_greater_than_filter.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            date_greater_than_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(date_greater_than_filters)
        await self._session_context.session.flush()
        return date_greater_than_filters
    async def update_bulk(
        self,
        date_greater_than_filter_updates: List[Dict[str, Any]]
    ) -> List[DateGreaterThanFilter]:
        """
        Update multiple date_greater_than_filters with the provided updates.
        Args:
            date_greater_than_filter_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each date_greater_than_filter.
        Returns:
            List[DateGreaterThanFilter]: A list of updated DateGreaterThanFilter objects.
        Raises:
            TypeError: If the date_greater_than_filter_id is not an integer.
            DateGreaterThanFilterNotFoundError: If a date_greater_than_filter with the
                provided date_greater_than_filter_id is not found.
        """
        logging.info("DateGreaterThanFilterManager.update_bulk start")
        updated_date_greater_than_filters = []
        for update in date_greater_than_filter_updates:
            date_greater_than_filter_id = update.get("date_greater_than_filter_id")
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError(
                    f"The date_greater_than_filter_id must be an integer, "
                    f"got {type(date_greater_than_filter_id)} instead."
                )
            if not date_greater_than_filter_id:
                continue
            logging.info("DateGreaterThanFilterManager.update_bulk date_greater_than_filter_id:%s", date_greater_than_filter_id)
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(
                    f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
            for key, value in update.items():
                if key != "date_greater_than_filter_id":
                    setattr(date_greater_than_filter, key, value)
            date_greater_than_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_date_greater_than_filters.append(date_greater_than_filter)
        await self._session_context.session.flush()
        logging.info("DateGreaterThanFilterManager.update_bulk end")
        return updated_date_greater_than_filters
    async def delete_bulk(self, date_greater_than_filter_ids: List[int]) -> bool:
        """
        Delete multiple date_greater_than_filters by their IDs.
        """
        logging.info("DateGreaterThanFilterManager.delete_bulk")
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError(
                    f"The date_greater_than_filter_id must be an integer, "
                    f"got {type(date_greater_than_filter_id)} instead."
                )
            date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(
                    f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!"
                )
            if date_greater_than_filter:
                await self._session_context.session.delete(date_greater_than_filter)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of date_greater_than_filters.
        """
        logging.info("DateGreaterThanFilterManager.count")
        result = await self._session_context.session.execute(select(DateGreaterThanFilter))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[DateGreaterThanFilter]:
        """
        Retrieve date_greater_than_filters sorted by a particular attribute.
        """
        if sort_by == "date_greater_than_filter_id":
            sort_by = "_date_greater_than_filter_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(DateGreaterThanFilter).order_by(getattr(DateGreaterThanFilter, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(DateGreaterThanFilter).order_by(getattr(DateGreaterThanFilter, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, date_greater_than_filter: DateGreaterThanFilter) -> DateGreaterThanFilter:
        """
        Refresh the state of a given date_greater_than_filter instance from the database.
        """
        logging.info("DateGreaterThanFilterManager.refresh")
        await self._session_context.session.refresh(date_greater_than_filter)
        return date_greater_than_filter
    async def exists(self, date_greater_than_filter_id: int) -> bool:
        """
        Check if a date_greater_than_filter with the given ID exists.
        """
        logging.info("DateGreaterThanFilterManager.exists %s", date_greater_than_filter_id)
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(
                f"The date_greater_than_filter_id must be an integer, "
                f"got {type(date_greater_than_filter_id)} instead."
            )
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        return bool(date_greater_than_filter)
    def is_equal(self, date_greater_than_filter1: DateGreaterThanFilter, date_greater_than_filter2: DateGreaterThanFilter) -> bool:
        """
        Check if two DateGreaterThanFilter objects are equal.
        Args:
            date_greater_than_filter1 (DateGreaterThanFilter): The first DateGreaterThanFilter object.
            date_greater_than_filter2 (DateGreaterThanFilter): The second DateGreaterThanFilter object.
        Returns:
            bool: True if the two DateGreaterThanFilter objects are equal, False otherwise.
        Raises:
            TypeError: If either date_greater_than_filter1 or date_greater_than_filter2
                is not provided or is not an instance of DateGreaterThanFilter.
        """
        if not date_greater_than_filter1:
            raise TypeError("DateGreaterThanFilter1 required.")
        if not date_greater_than_filter2:
            raise TypeError("DateGreaterThanFilter2 required.")
        if not isinstance(date_greater_than_filter1, DateGreaterThanFilter):
            raise TypeError("The date_greater_than_filter1 must be an DateGreaterThanFilter instance.")
        if not isinstance(date_greater_than_filter2, DateGreaterThanFilter):
            raise TypeError("The date_greater_than_filter2 must be an DateGreaterThanFilter instance.")
        dict1 = self.to_dict(date_greater_than_filter1)
        dict2 = self.to_dict(date_greater_than_filter2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[DateGreaterThanFilter]:  # PacID
        """
        Retrieve a list of date_greater_than_filters by pac ID.
        Args:
            pac_id (int): The ID of the pac.
        Returns:
            List[DateGreaterThanFilter]: A list of date_greater_than_filters associated
            with the specified pac ID.
        """
        logging.info("DateGreaterThanFilterManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The date_greater_than_filter_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = DateGreaterThanFilter._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset
