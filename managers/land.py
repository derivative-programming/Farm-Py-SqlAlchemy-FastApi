# models/managers/land.py
# pylint: disable=unused-import
"""
This module contains the
LandManager class, which is
responsible for managing
lands in the system.
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
from models.land import Land
from models.serialization_schema.land import LandSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class LandNotFoundError(Exception):
    """
    Exception raised when a specified
    land is not found.
    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Land not found"):
        self.message = message
        super().__init__(self.message)

class LandEnum(Enum):
    """
    Represents an enumeration of
    Land options.
    """
    UNKNOWN = 'Unknown'
    FIELD_ONE = 'Field_One'

class LandManager:
    """
    The LandManager class
    is responsible for managing
    lands in the system.
    It provides methods for adding, updating, deleting,
    and retrieving lands.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        LandManager class.
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
        Initializes the LandManager.
        This method initializes the LandManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("LandManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(LandEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(LandEnum.FIELD_ONE) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Field One"
            item.lookup_enum_name = "Field_One"
            item.description = "Field One"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("LandManager.Initialize end")
    async def from_enum(
        self,
        enum_val: LandEnum
    ) -> Land:
        """
        Returns a Land object
        based on the provided enum value.
        Args:
            enum_val (LandEnum):
                The enum value representing the filter.
        Returns:
            Land:
                The Land object
                matching the enum value.
        """
        query_filter = (
            Land._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Land:
        """
        Builds a new Land
        object with the specified attributes.
        Args:
            **kwargs: The attributes of the
                land.
        Returns:
            Land: The newly created
                Land object.
        """
        logging.info("LandManager.build")
        return Land(**kwargs)
    async def add(
        self,
        land: Land
    ) -> Land:
        """
        Adds a new land to the system.
        Args:
            land (Land): The
                land to add.
        Returns:
            Land: The added
                land.
        """
        logging.info("LandManager.add")
        land.insert_user_id = self._session_context.customer_code
        land.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            land)
        await self._session_context.session.flush()
        return land
    def _build_query(self):
        """
        Builds the base query for retrieving
        lands.
        Returns:
            The base query for retrieving
            lands.
        """
        logging.info("LandManager._build_query")
        query = select(
            Land,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Land._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Land._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(
        self,
        query_filter
    ) -> List[Land]:
        """
        Runs the query to retrieve
        lands from the database.
        Args:
            query_filter: The filter to apply to the query.
        Returns:
            List[Land]: The list of
                lands that match the query.
        """
        logging.info("LandManager._run_query")
        land_query_all = self._build_query()
        if query_filter is not None:
            query = land_query_all.filter(query_filter)
        else:
            query = land_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            land = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            land.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(land)
        return result
    def _first_or_none(
        self,
        land_list: List['Land']
    ) -> Optional['Land']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.
        Args:
            land_list (List[Land]):
                The list to retrieve
                the first element from.
        Returns:
            Optional[Land]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            land_list[0]
            if land_list
            else None
        )
    async def get_by_id(self, land_id: int) -> Optional[Land]:
        """
        Retrieves a land by its ID.
        Args:
            land_id (int): The ID of the
                land to retrieve.
        Returns:
            Optional[Land]: The retrieved
                land, or None if not found.
        """
        logging.info(
            "LandManager.get_by_id start land_id: %s",
            str(land_id))
        if not isinstance(land_id, int):
            raise TypeError(
                "The land_id must be an integer, "
                f"got {type(land_id)} instead.")
        query_filter = (
            Land._land_id == land_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Land]:
        """
        Retrieves a land
        by its code.
        Args:
            code (uuid.UUID): The code of the
                land to retrieve.
        Returns:
            Optional[Land]: The retrieved
                land, or None if not found.
        """
        logging.info("LandManager.get_by_code %s", code)
        query_filter = Land._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(
        self,
        land: Land, **kwargs
    ) -> Optional[Land]:
        """
        Updates a land with
        the specified attributes.
        Args:
            land (Land): The
                land to update.
            **kwargs: The attributes to update.
        Returns:
            Optional[Land]: The updated
                land, or None if not found.
        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("LandManager.update")
        property_list = Land.property_list()
        if land:
            land.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(land, key, value)
            await self._session_context.session.flush()
        return land
    async def delete(self, land_id: int):
        """
        Deletes a land by its ID.
        Args:
            land_id (int): The ID of the
                land to delete.
        Raises:
            TypeError: If the land_id
                is not an integer.
            LandNotFoundError: If the
                land with the
                specified ID is not found.
        """
        logging.info("LandManager.delete %s", land_id)
        if not isinstance(land_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(land_id)} instead."
            )
        land = await self.get_by_id(
            land_id)
        if not land:
            raise LandNotFoundError(f"Land with ID {land_id} not found!")
        await self._session_context.session.delete(
            land)
        await self._session_context.session.flush()
    async def get_list(
        self
    ) -> List[Land]:
        """
        Retrieves a list of all lands.
        Returns:
            List[Land]: The list of
                lands.
        """
        logging.info("LandManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(
            self,
            land: Land) -> str:
        """
        Serializes a Land object
        to a JSON string.
        Args:
            land (Land): The
                land to serialize.
        Returns:
            str: The JSON string representation of the
                land.
        """
        logging.info("LandManager.to_json")
        schema = LandSchema()
        land_data = schema.dump(land)
        return json.dumps(land_data)
    def to_dict(
        self,
        land: Land
    ) -> Dict[str, Any]:
        """
        Serializes a Land
        object to a dictionary.
        Args:
            land (Land): The
                land to serialize.
        Returns:
            Dict[str, Any]: The dictionary representation of the
                land.
        """
        logging.info("LandManager.to_dict")
        schema = LandSchema()
        land_data = schema.dump(land)
        assert isinstance(land_data, dict)
        return land_data
    def from_json(self, json_str: str) -> Land:
        """
        Deserializes a JSON string into a
        Land object.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            Land: The deserialized
                Land object.
        """
        logging.info("LandManager.from_json")
        schema = LandSchema()
        data = json.loads(json_str)
        land_dict = schema.load(data)
        new_land = Land(**land_dict)
        return new_land
    def from_dict(self, land_dict: Dict[str, Any]) -> Land:
        """
        Creates a Land
        instance from a dictionary of attributes.
        Args:
            land_dict (Dict[str, Any]): A dictionary
                containing land
                attributes.
        Returns:
            Land: A new
                Land instance
                created from the given
                dictionary.
        """
        logging.info("LandManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = LandSchema()
        land_dict_converted = schema.load(
            land_dict)
        # Create a new Land instance
        # using the validated data
        new_land = Land(**land_dict_converted)
        return new_land
    async def add_bulk(
        self,
        lands: List[Land]
    ) -> List[Land]:
        """
        Adds multiple lands
        to the system.
        Args:
            lands (List[Land]): The list of
                lands to add.
        Returns:
            List[Land]: The added
                lands.
        """
        logging.info("LandManager.add_bulk")
        for land in lands:
            land_id = land.land_id
            code = land.code
            if land.land_id is not None and land.land_id > 0:
                raise ValueError(
                    "Land is already added"
                    f": {str(code)} {str(land_id)}"
                )
            land.insert_user_id = self._session_context.customer_code
            land.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(lands)
        await self._session_context.session.flush()
        return lands
    async def update_bulk(
        self,
        land_updates: List[Dict[str, Any]]
    ) -> List[Land]:
        """
        Update multiple lands
        with the provided updates.
        Args:
            land_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            land.
        Returns:
            List[Land]: A list of updated
                Land objects.
        Raises:
            TypeError: If the land_id is not an integer.
            LandNotFoundError: If a
                land with the
                provided land_id is not found.
        """
        logging.info("LandManager.update_bulk start")
        updated_lands = []
        for update in land_updates:
            land_id = update.get("land_id")
            if not isinstance(land_id, int):
                raise TypeError(
                    f"The land_id must be an integer, "
                    f"got {type(land_id)} instead."
                )
            if not land_id:
                continue
            logging.info("LandManager.update_bulk land_id:%s", land_id)
            land = await self.get_by_id(
                land_id)
            if not land:
                raise LandNotFoundError(
                    f"Land with ID {land_id} not found!")
            for key, value in update.items():
                if key != "land_id":
                    setattr(land, key, value)
            land.last_update_user_id = self._session_context.customer_code
            updated_lands.append(land)
        await self._session_context.session.flush()
        logging.info("LandManager.update_bulk end")
        return updated_lands
    async def delete_bulk(self, land_ids: List[int]) -> bool:
        """
        Delete multiple lands
        by their IDs.
        """
        logging.info("LandManager.delete_bulk")
        for land_id in land_ids:
            if not isinstance(land_id, int):
                raise TypeError(
                    f"The land_id must be an integer, "
                    f"got {type(land_id)} instead."
                )
            land = await self.get_by_id(
                land_id)
            if not land:
                raise LandNotFoundError(
                    f"Land with ID {land_id} not found!"
                )
            if land:
                await self._session_context.session.delete(
                    land)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of
        lands.
        """
        logging.info("LandManager.count")
        result = await self._session_context.session.execute(
            select(Land))
        return len(list(result.scalars().all()))
    async def refresh(
        self,
        land: Land
    ) -> Land:
        """
        Refresh the state of a given
        land instance
        from the database.
        """
        logging.info("LandManager.refresh")
        await self._session_context.session.refresh(land)
        return land
    async def exists(self, land_id: int) -> bool:
        """
        Check if a land
        with the given ID exists.
        """
        logging.info("LandManager.exists %s", land_id)
        if not isinstance(land_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(land_id)} instead."
            )
        land = await self.get_by_id(
            land_id)
        return bool(land)
    def is_equal(
        self,
        land1: Land,
        land2: Land
    ) -> bool:
        """
        Check if two Land
        objects are equal.
        Args:
            land1 (Land): The first
                Land object.
            land2 (Land): The second
                Land object.
        Returns:
            bool: True if the two Land
                objects are equal, False otherwise.
        Raises:
            TypeError: If either land1
                or land2
                is not provided or is not an instance of
                Land.
        """
        if not land1:
            raise TypeError("Land1 required.")
        if not land2:
            raise TypeError("Land2 required.")
        if not isinstance(land1, Land):
            raise TypeError("The land1 must be an "
                            "Land instance.")
        if not isinstance(land2, Land):
            raise TypeError("The land2 must be an "
                            "Land instance.")
        dict1 = self.to_dict(land1)
        dict2 = self.to_dict(land2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Land]:  # PacID
        """
        Retrieve a list of lands by
        pac ID.
        Args:
            pac_id (int): The ID of the pac.
        Returns:
            List[Land]: A list of
                lands associated
                with the specified pac ID.
        """
        logging.info("LandManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Land._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

