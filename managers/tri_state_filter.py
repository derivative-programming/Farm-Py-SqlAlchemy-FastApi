# models/managers/tri_state_filter.py
# pylint: disable=unused-import

"""
This module contains the
TriStateFilterManager class, which is
responsible for managing
tri_state_filters in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class TriStateFilterNotFoundError(Exception):
    """
    Exception raised when a specified
    tri_state_filter is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="TriStateFilter not found"):
        self.message = message
        super().__init__(self.message)


class TriStateFilterEnum(Enum):
    """
    Represents an enumeration of
    Tri State Filter options.
    """
    UNKNOWN = 'Unknown'
    YES = 'Yes'
    NO = 'No'


class TriStateFilterManager:
    """
    The TriStateFilterManager class
    is responsible for managing
    tri_state_filters in the system.
    It provides methods for adding, updating, deleting,
    and retrieving tri_state_filters.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        TriStateFilterManager class.

        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.

        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context


    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item

    async def initialize(self):
        """
        Initializes the TriStateFilterManager.
        This method initializes the TriStateFilterManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("TriStateFilterManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
        if await self.from_enum(TriStateFilterEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.YES) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Yes"
            item.lookup_enum_name = "Yes"
            item.description = "Yes"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.NO) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "No"
            item.lookup_enum_name = "No"
            item.description = "No"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        logging.info("TriStateFilterManager.Initialize end")

    async def from_enum(
        self,
        enum_val: TriStateFilterEnum
    ) -> TriStateFilter:
        """
        Returns a TriStateFilter object
        based on the provided enum value.
        Args:
            enum_val (TriStateFilterEnum):
                The enum value representing the filter.
        Returns:
            TriStateFilter:
                The TriStateFilter object
                matching the enum value.
        """
        query_filter = (
            TriStateFilter._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)


    async def build(self, **kwargs) -> TriStateFilter:
        """
        Builds a new TriStateFilter
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                tri_state_filter.

        Returns:
            TriStateFilter: The newly created
                TriStateFilter object.
        """
        logging.info(
            "TriStateFilterManager.build")
        return TriStateFilter(**kwargs)

    async def add(
        self,
        tri_state_filter: TriStateFilter
    ) -> TriStateFilter:
        """
        Adds a new tri_state_filter to the system.

        Args:
            tri_state_filter (TriStateFilter): The
                tri_state_filter to add.

        Returns:
            TriStateFilter: The added
                tri_state_filter.
        """
        logging.info(
            "TriStateFilterManager.add")
        tri_state_filter.insert_user_id = (
            self._session_context.customer_code)
        tri_state_filter.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            tri_state_filter)
        await self._session_context.session.flush()
        return tri_state_filter

    def _build_query(self):
        """
        Builds the base query for retrieving
        tri_state_filters.

        Returns:
            The base query for retrieving
            tri_state_filters.
        """
        logging.info(
            "TriStateFilterManager._build_query")

        query = select(
            TriStateFilter,
            Pac,  # pac_id
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(TriStateFilter._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 TriStateFilter._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[TriStateFilter]:
        """
        Runs the query to retrieve
        tri_state_filters from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[TriStateFilter]: The list of
                tri_state_filters that match the query.
        """
        logging.info(
            "TriStateFilterManager._run_query")
        tri_state_filter_query_all = self._build_query()

        if query_filter is not None:
            query = tri_state_filter_query_all.filter(query_filter)
        else:
            query = tri_state_filter_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            tri_state_filter = query_result_row[i]
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            tri_state_filter.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(tri_state_filter)

        return result

    def _first_or_none(
        self,
        tri_state_filter_list: List['TriStateFilter']
    ) -> Optional['TriStateFilter']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            tri_state_filter_list (List[TriStateFilter]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[TriStateFilter]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            tri_state_filter_list[0]
            if tri_state_filter_list
            else None
        )

    async def get_by_id(
        self, tri_state_filter_id: int
    ) -> Optional[TriStateFilter]:
        """
        Retrieves a tri_state_filter by its ID.

        Args:
            tri_state_filter_id (int): The ID of the
                tri_state_filter to retrieve.

        Returns:
            Optional[TriStateFilter]: The retrieved
                tri_state_filter, or None if not found.
        """
        logging.info(
            "TriStateFilterManager.get_by_id start tri_state_filter_id: %s",
            str(tri_state_filter_id))
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                "The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead.")

        query_filter = (
            TriStateFilter._tri_state_filter_id == tri_state_filter_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[TriStateFilter]:
        """
        Retrieves a tri_state_filter
        by its code.

        Args:
            code (uuid.UUID): The code of the
                tri_state_filter to retrieve.

        Returns:
            Optional[TriStateFilter]: The retrieved
                tri_state_filter, or None if not found.
        """
        logging.info("TriStateFilterManager.get_by_code %s",
                     code)

        query_filter = TriStateFilter._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        tri_state_filter: TriStateFilter, **kwargs
    ) -> Optional[TriStateFilter]:
        """
        Updates a tri_state_filter with
        the specified attributes.

        Args:
            tri_state_filter (TriStateFilter): The
                tri_state_filter to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[TriStateFilter]: The updated
                tri_state_filter, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("TriStateFilterManager.update")
        property_list = TriStateFilter.property_list()
        if tri_state_filter:
            tri_state_filter.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(tri_state_filter, key, value)
            await self._session_context.session.flush()
        return tri_state_filter

    async def delete(self, tri_state_filter_id: int):
        """
        Deletes a tri_state_filter by its ID.

        Args:
            tri_state_filter_id (int): The ID of the
                tri_state_filter to delete.

        Raises:
            TypeError: If the tri_state_filter_id
                is not an integer.
            TriStateFilterNotFoundError: If the
                tri_state_filter with the
                specified ID is not found.
        """
        logging.info(
            "TriStateFilterManager.delete %s",
            tri_state_filter_id)
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead."
            )
        tri_state_filter = await self.get_by_id(
            tri_state_filter_id)
        if not tri_state_filter:
            raise TriStateFilterNotFoundError(
                f"TriStateFilter with ID {tri_state_filter_id} not found!")

        await self._session_context.session.delete(
            tri_state_filter)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[TriStateFilter]:
        """
        Retrieves a list of all tri_state_filters.

        Returns:
            List[TriStateFilter]: The list of
                tri_state_filters.
        """
        logging.info(
            "TriStateFilterManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            tri_state_filter: TriStateFilter) -> str:
        """
        Serializes a TriStateFilter object
        to a JSON string.

        Args:
            tri_state_filter (TriStateFilter): The
                tri_state_filter to serialize.

        Returns:
            str: The JSON string representation of the
                tri_state_filter.
        """
        logging.info(
            "TriStateFilterManager.to_json")
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        return json.dumps(tri_state_filter_data)

    def to_dict(
        self,
        tri_state_filter: TriStateFilter
    ) -> Dict[str, Any]:
        """
        Serializes a TriStateFilter
        object to a dictionary.

        Args:
            tri_state_filter (TriStateFilter): The
                tri_state_filter to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                tri_state_filter.
        """
        logging.info(
            "TriStateFilterManager.to_dict")
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)

        assert isinstance(tri_state_filter_data, dict)

        return tri_state_filter_data

    async def from_json(self, json_str: str) -> TriStateFilter:
        """
        Deserializes a JSON string into a
        TriStateFilter object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            TriStateFilter: The deserialized
                TriStateFilter object.
        """
        logging.info(
            "TriStateFilterManager.from_json")
        schema = TriStateFilterSchema()
        data = json.loads(json_str)
        tri_state_filter_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)

        # load or create
        new_tri_state_filter = await self.get_by_id(
            tri_state_filter_dict["tri_state_filter_id"])
        if new_tri_state_filter is None:
            new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)
            self._session_context.session.add(new_tri_state_filter)
        else:
            for key, value in tri_state_filter_dict.items():
                setattr(new_tri_state_filter, key, value)

        return new_tri_state_filter

    async def from_dict(
        self, tri_state_filter_dict: Dict[str, Any]
    ) -> TriStateFilter:
        """
        Creates a TriStateFilter
        instance from a dictionary of attributes.

        Args:
            tri_state_filter_dict (Dict[str, Any]): A dictionary
                containing tri_state_filter
                attributes.

        Returns:
            TriStateFilter: A new
                TriStateFilter instance
                created from the given
                dictionary.
        """
        logging.info(
            "TriStateFilterManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = TriStateFilterSchema()
        tri_state_filter_dict_converted = schema.load(
            tri_state_filter_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new TriStateFilter instance
        # using the validated data
        # new_tri_state_filter = TriStateFilter(**tri_state_filter_dict_converted)

        # load or create
        new_tri_state_filter = await self.get_by_id(
            tri_state_filter_dict_converted["tri_state_filter_id"])
        if new_tri_state_filter is None:
            new_tri_state_filter = TriStateFilter(**tri_state_filter_dict_converted)
            self._session_context.session.add(new_tri_state_filter)
        else:
            for key, value in tri_state_filter_dict_converted.items():
                setattr(new_tri_state_filter, key, value)

        return new_tri_state_filter

    async def add_bulk(
        self,
        tri_state_filters: List[TriStateFilter]
    ) -> List[TriStateFilter]:
        """
        Adds multiple tri_state_filters
        to the system.

        Args:
            tri_state_filters (List[TriStateFilter]): The list of
                tri_state_filters to add.

        Returns:
            List[TriStateFilter]: The added
                tri_state_filters.
        """
        logging.info(
            "TriStateFilterManager.add_bulk")
        for list_item in tri_state_filters:
            tri_state_filter_id = \
                list_item.tri_state_filter_id
            code = list_item.code
            if list_item.tri_state_filter_id is not None and \
                    list_item.tri_state_filter_id > 0:
                raise ValueError(
                    "TriStateFilter is already added"
                    f": {str(code)} {str(tri_state_filter_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(tri_state_filters)
        await self._session_context.session.flush()
        return tri_state_filters

    async def update_bulk(
        self,
        tri_state_filter_updates: List[Dict[str, Any]]
    ) -> List[TriStateFilter]:
        """
        Update multiple tri_state_filters
        with the provided updates.

        Args:
            tri_state_filter_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            tri_state_filter.

        Returns:
            List[TriStateFilter]: A list of updated
                TriStateFilter objects.

        Raises:
            TypeError: If the tri_state_filter_id is not an integer.
            TriStateFilterNotFoundError: If a
                tri_state_filter with the
                provided tri_state_filter_id is not found.
        """

        logging.info(
            "TriStateFilterManager.update_bulk start")
        updated_tri_state_filters = []
        for update in tri_state_filter_updates:
            tri_state_filter_id = update.get("tri_state_filter_id")
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(
                    f"The tri_state_filter_id must be an integer, "
                    f"got {type(tri_state_filter_id)} instead."
                )
            if not tri_state_filter_id:
                continue

            logging.info(
                "TriStateFilterManager.update_bulk tri_state_filter_id:%s",
                tri_state_filter_id)

            tri_state_filter = await self.get_by_id(
                tri_state_filter_id)

            if not tri_state_filter:
                raise TriStateFilterNotFoundError(
                    f"TriStateFilter with ID {tri_state_filter_id} not found!")

            for key, value in update.items():
                if key != "tri_state_filter_id":
                    setattr(tri_state_filter, key, value)

            tri_state_filter.last_update_user_id =\
                self._session_context.customer_code

            updated_tri_state_filters.append(tri_state_filter)

        await self._session_context.session.flush()

        logging.info(
            "TriStateFilterManager.update_bulk end")

        return updated_tri_state_filters

    async def delete_bulk(self, tri_state_filter_ids: List[int]) -> bool:
        """
        Delete multiple tri_state_filters
        by their IDs.
        """
        logging.info(
            "TriStateFilterManager.delete_bulk")

        for tri_state_filter_id in tri_state_filter_ids:
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(
                    f"The tri_state_filter_id must be an integer, "
                    f"got {type(tri_state_filter_id)} instead."
                )

            tri_state_filter = await self.get_by_id(
                tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(
                    f"TriStateFilter with ID {tri_state_filter_id} not found!"
                )

            if tri_state_filter:
                await self._session_context.session.delete(
                    tri_state_filter)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        tri_state_filters.
        """
        logging.info(
            "TriStateFilterManager.count")
        result = await self._session_context.session.execute(
            select(TriStateFilter))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        tri_state_filter: TriStateFilter
    ) -> TriStateFilter:
        """
        Refresh the state of a given
        tri_state_filter instance
        from the database.
        """

        logging.info(
            "TriStateFilterManager.refresh")

        await self._session_context.session.refresh(tri_state_filter)

        return tri_state_filter

    async def exists(self, tri_state_filter_id: int) -> bool:
        """
        Check if a tri_state_filter
        with the given ID exists.
        """
        logging.info(
            "TriStateFilterManager.exists %s",
            tri_state_filter_id)
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead."
            )
        tri_state_filter = await self.get_by_id(
            tri_state_filter_id)
        return bool(tri_state_filter)

    def is_equal(
        self,
        tri_state_filter1: TriStateFilter,
        tri_state_filter2: TriStateFilter
    ) -> bool:
        """
        Check if two TriStateFilter
        objects are equal.

        Args:
            tri_state_filter1 (TriStateFilter): The first
                TriStateFilter object.
            tri_state_filter2 (TriStateFilter): The second
                TriStateFilter object.

        Returns:
            bool: True if the two TriStateFilter
                objects are equal, False otherwise.

        Raises:
            TypeError: If either tri_state_filter1
                or tri_state_filter2
                is not provided or is not an instance of
                TriStateFilter.
        """
        if not tri_state_filter1:
            raise TypeError("TriStateFilter1 required.")

        if not tri_state_filter2:
            raise TypeError("TriStateFilter2 required.")

        if not isinstance(tri_state_filter1,
                          TriStateFilter):
            raise TypeError("The tri_state_filter1 must be an "
                            "TriStateFilter instance.")

        if not isinstance(tri_state_filter2,
                          TriStateFilter):
            raise TypeError("The tri_state_filter2 must be an "
                            "TriStateFilter instance.")

        dict1 = self.to_dict(tri_state_filter1)
        dict2 = self.to_dict(tri_state_filter2)

        return dict1 == dict2
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[TriStateFilter]:
        """
        Retrieve a list of tri_state_filters by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[TriStateFilter]: A list of
                tri_state_filters associated
                with the specified pac ID.
        """

        logging.info(
            "TriStateFilterManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = TriStateFilter._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
