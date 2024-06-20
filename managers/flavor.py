# models/managers/flavor.py
# pylint: disable=unused-import
"""
This module contains the FlavorManager class, which is
responsible for managing flavors in the system.
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
from models.flavor import Flavor
from models.serialization_schema.flavor import FlavorSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class FlavorNotFoundError(Exception):
    """
    Exception raised when a specified flavor is not found.
    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Flavor not found"):
        self.message = message
        super().__init__(self.message)

class FlavorEnum(Enum):
    """
    Represents an enumeration of
    Flavor options.
    """
    UNKNOWN = 'Unknown'
    SWEET = 'Sweet'
    SOUR = 'Sour'

class FlavorManager:
    """
    The FlavorManager class is responsible for managing flavors in the system.
    It provides methods for adding, updating, deleting, and retrieving flavors.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the FlavorManager class.
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

    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        """
        Initializes the FlavorManager.
        This method initializes the FlavorManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("FlavorManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(FlavorEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(FlavorEnum.SWEET) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sweet"
            item.lookup_enum_name = "Sweet"
            item.description = "Sweet"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(FlavorEnum.SOUR) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sour"
            item.lookup_enum_name = "Sour"
            item.description = "Sour"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("FlavorManager.Initialize end")
    async def from_enum(
        self,
        enum_val: FlavorEnum
    ) -> Flavor:
        """
        Returns a Flavor object
        based on the provided enum value.
        Args:
            enum_val (FlavorEnum):
                The enum value representing the filter.
        Returns:
            Flavor:
                The Flavor object
                matching the enum value.
        """
        query_filter = (
            Flavor._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Flavor:
        """
        Builds a new Flavor object with the specified attributes.
        Args:
            **kwargs: The attributes of the flavor.
        Returns:
            Flavor: The newly created Flavor object.
        """
        logging.info("FlavorManager.build")
        return Flavor(**kwargs)
    async def add(self, flavor: Flavor) -> Flavor:
        """
        Adds a new flavor to the system.
        Args:
            flavor (Flavor): The flavor to add.
        Returns:
            Flavor: The added flavor.
        """
        logging.info("FlavorManager.add")
        flavor.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(flavor)
        await self._session_context.session.flush()
        return flavor
    def _build_query(self):
        """
        Builds the base query for retrieving flavors.
        Returns:
            The base query for retrieving flavors.
        """
        logging.info("FlavorManager._build_query")
        query = select(
            Flavor,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Flavor._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Flavor._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Flavor]:
        """
        Runs the query to retrieve flavors from the database.
        Args:
            query_filter: The filter to apply to the query.
        Returns:
            List[Flavor]: The list of flavors that match the query.
        """
        logging.info("FlavorManager._run_query")
        flavor_query_all = self._build_query()
        if query_filter is not None:
            query = flavor_query_all.filter(query_filter)
        else:
            query = flavor_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            flavor = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            flavor.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(flavor)
        return result
    def _first_or_none(
        self,
        flavor_list: List['Flavor']
    ) -> Optional['Flavor']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.
        Args:
            flavor_list (List[Flavor]): The list to retrieve
                the first element from.
        Returns:
            Optional[Flavor]: The first element of the list
                if it exists, otherwise None.
        """
        return (
            flavor_list[0]
            if flavor_list
            else None
        )
    async def get_by_id(self, flavor_id: int) -> Optional[Flavor]:
        """
        Retrieves a flavor by its ID.
        Args:
            flavor_id (int): The ID of the flavor to retrieve.
        Returns:
            Optional[Flavor]: The retrieved flavor, or None if not found.
        """
        logging.info(
            "FlavorManager.get_by_id start flavor_id: %s",
            str(flavor_id))
        if not isinstance(flavor_id, int):
            raise TypeError(
                "The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead.")
        query_filter = (
            Flavor._flavor_id == flavor_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Flavor]:
        """
        Retrieves a flavor by its code.
        Args:
            code (uuid.UUID): The code of the flavor to retrieve.
        Returns:
            Optional[Flavor]: The retrieved flavor, or None if not found.
        """
        logging.info("FlavorManager.get_by_code %s", code)
        query_filter = Flavor._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, flavor: Flavor, **kwargs) -> Optional[Flavor]:
        """
        Updates a flavor with the specified attributes.
        Args:
            flavor (Flavor): The flavor to update.
            **kwargs: The attributes to update.
        Returns:
            Optional[Flavor]: The updated flavor, or None if not found.
        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("FlavorManager.update")
        property_list = Flavor.property_list()
        if flavor:
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(flavor, key, value)
            await self._session_context.session.flush()
        return flavor
    async def delete(self, flavor_id: int):
        """
        Deletes a flavor by its ID.
        Args:
            flavor_id (int): The ID of the flavor to delete.
        Raises:
            TypeError: If the flavor_id is not an integer.
            FlavorNotFoundError: If the flavor with the
                specified ID is not found.
        """
        logging.info("FlavorManager.delete %s", flavor_id)
        if not isinstance(flavor_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead."
            )
        flavor = await self.get_by_id(flavor_id)
        if not flavor:
            raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
        await self._session_context.session.delete(flavor)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Flavor]:
        """
        Retrieves a list of all flavors.
        Returns:
            List[Flavor]: The list of flavors.
        """
        logging.info("FlavorManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, flavor: Flavor) -> str:
        """
        Serializes a Flavor object to a JSON string.
        Args:
            flavor (Flavor): The flavor to serialize.
        Returns:
            str: The JSON string representation of the flavor.
        """
        logging.info("FlavorManager.to_json")
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return json.dumps(flavor_data)
    def to_dict(self, flavor: Flavor) -> Dict[str, Any]:
        """
        Serializes a Flavor object to a dictionary.
        Args:
            flavor (Flavor): The flavor to serialize.
        Returns:
            Dict[str, Any]: The dictionary representation of the flavor.
        """
        logging.info("FlavorManager.to_dict")
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        assert isinstance(flavor_data, dict)
        return flavor_data
    def from_json(self, json_str: str) -> Flavor:
        """
        Deserializes a JSON string into a Flavor object.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            Flavor: The deserialized Flavor object.
        """
        logging.info("FlavorManager.from_json")
        schema = FlavorSchema()
        data = json.loads(json_str)
        flavor_dict = schema.load(data)
        new_flavor = Flavor(**flavor_dict)
        return new_flavor
    def from_dict(self, flavor_dict: Dict[str, Any]) -> Flavor:
        """
        Creates a Flavor instance from a dictionary of attributes.
        Args:
            flavor_dict (Dict[str, Any]): A dictionary
                containing flavor attributes.
        Returns:
            Flavor: A new Flavor instance created from the given dictionary.
        """
        logging.info("FlavorManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = FlavorSchema()
        flavor_dict_converted = schema.load(flavor_dict)
        # Create a new Flavor instance using the validated data
        new_flavor = Flavor(**flavor_dict_converted)
        return new_flavor
    async def add_bulk(self, flavors: List[Flavor]) -> List[Flavor]:
        """
        Adds multiple flavors to the system.
        Args:
            flavors (List[Flavor]): The list of flavors to add.
        Returns:
            List[Flavor]: The added flavors.
        """
        logging.info("FlavorManager.add_bulk")
        for flavor in flavors:
            flavor_id = flavor.flavor_id
            code = flavor.code
            if flavor.flavor_id is not None and flavor.flavor_id > 0:
                raise ValueError(
                    f"Flavor is already added: {str(code)} {str(flavor_id)}"
                )
            flavor.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(flavors)
        await self._session_context.session.flush()
        return flavors
    async def update_bulk(
        self,
        flavor_updates: List[Dict[str, Any]]
    ) -> List[Flavor]:
        """
        Update multiple flavors with the provided updates.
        Args:
            flavor_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each flavor.
        Returns:
            List[Flavor]: A list of updated Flavor objects.
        Raises:
            TypeError: If the flavor_id is not an integer.
            FlavorNotFoundError: If a flavor with the
                provided flavor_id is not found.
        """
        logging.info("FlavorManager.update_bulk start")
        updated_flavors = []
        for update in flavor_updates:
            flavor_id = update.get("flavor_id")
            if not isinstance(flavor_id, int):
                raise TypeError(
                    f"The flavor_id must be an integer, "
                    f"got {type(flavor_id)} instead."
                )
            if not flavor_id:
                continue
            logging.info("FlavorManager.update_bulk flavor_id:%s", flavor_id)
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(
                    f"Flavor with ID {flavor_id} not found!")
            for key, value in update.items():
                if key != "flavor_id":
                    setattr(flavor, key, value)
            flavor.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_flavors.append(flavor)
        await self._session_context.session.flush()
        logging.info("FlavorManager.update_bulk end")
        return updated_flavors
    async def delete_bulk(self, flavor_ids: List[int]) -> bool:
        """
        Delete multiple flavors by their IDs.
        """
        logging.info("FlavorManager.delete_bulk")
        for flavor_id in flavor_ids:
            if not isinstance(flavor_id, int):
                raise TypeError(
                    f"The flavor_id must be an integer, "
                    f"got {type(flavor_id)} instead."
                )
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(
                    f"Flavor with ID {flavor_id} not found!"
                )
            if flavor:
                await self._session_context.session.delete(flavor)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of flavors.
        """
        logging.info("FlavorManager.count")
        result = await self._session_context.session.execute(select(Flavor))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Flavor]:
        """
        Retrieve flavors sorted by a particular attribute.
        """
        if sort_by == "flavor_id":
            sort_by = "_flavor_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Flavor).order_by(getattr(Flavor, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Flavor).order_by(getattr(Flavor, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, flavor: Flavor) -> Flavor:
        """
        Refresh the state of a given flavor instance from the database.
        """
        logging.info("FlavorManager.refresh")
        await self._session_context.session.refresh(flavor)
        return flavor
    async def exists(self, flavor_id: int) -> bool:
        """
        Check if a flavor with the given ID exists.
        """
        logging.info("FlavorManager.exists %s", flavor_id)
        if not isinstance(flavor_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(flavor_id)} instead."
            )
        flavor = await self.get_by_id(flavor_id)
        return bool(flavor)
    def is_equal(self, flavor1: Flavor, flavor2: Flavor) -> bool:
        """
        Check if two Flavor objects are equal.
        Args:
            flavor1 (Flavor): The first Flavor object.
            flavor2 (Flavor): The second Flavor object.
        Returns:
            bool: True if the two Flavor objects are equal, False otherwise.
        Raises:
            TypeError: If either flavor1 or flavor2
                is not provided or is not an instance of Flavor.
        """
        if not flavor1:
            raise TypeError("Flavor1 required.")
        if not flavor2:
            raise TypeError("Flavor2 required.")
        if not isinstance(flavor1, Flavor):
            raise TypeError("The flavor1 must be an Flavor instance.")
        if not isinstance(flavor2, Flavor):
            raise TypeError("The flavor2 must be an Flavor instance.")
        dict1 = self.to_dict(flavor1)
        dict2 = self.to_dict(flavor2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Flavor]:  # PacID
        """
        Retrieve a list of flavors by pac ID.
        Args:
            pac_id (int): The ID of the pac.
        Returns:
            List[Flavor]: A list of flavors associated
            with the specified pac ID.
        """
        logging.info("FlavorManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The flavor_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Flavor._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

