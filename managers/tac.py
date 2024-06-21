# models/managers/tac.py
# pylint: disable=unused-import
"""
This module contains the
TacManager class, which is
responsible for managing
tacs in the system.
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
from models.tac import Tac
from models.serialization_schema.tac import TacSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class TacNotFoundError(Exception):
    """
    Exception raised when a specified
    tac is not found.
    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Tac not found"):
        self.message = message
        super().__init__(self.message)

class TacEnum(Enum):
    """
    Represents an enumeration of
    Tac options.
    """
    UNKNOWN = 'Unknown'
    PRIMARY = 'Primary'

class TacManager:
    """
    The TacManager class
    is responsible for managing
    tacs in the system.
    It provides methods for adding, updating, deleting,
    and retrieving tacs.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        TacManager class.
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
        Initializes the TacManager.
        This method initializes the TacManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("TacManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(TacEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(TacEnum.PRIMARY) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Primary"
            item.lookup_enum_name = "Primary"
            item.description = "Primary"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("TacManager.Initialize end")
    async def from_enum(
        self,
        enum_val: TacEnum
    ) -> Tac:
        """
        Returns a Tac object
        based on the provided enum value.
        Args:
            enum_val (TacEnum):
                The enum value representing the filter.
        Returns:
            Tac:
                The Tac object
                matching the enum value.
        """
        query_filter = (
            Tac._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Tac:
        """
        Builds a new Tac
        object with the specified attributes.
        Args:
            **kwargs: The attributes of the
                tac.
        Returns:
            Tac: The newly created
                Tac object.
        """
        logging.info("TacManager.build")
        return Tac(**kwargs)
    async def add(
        self,
        tac: Tac
    ) -> Tac:
        """
        Adds a new tac to the system.
        Args:
            tac (Tac): The
                tac to add.
        Returns:
            Tac: The added
                tac.
        """
        logging.info("TacManager.add")
        tac.insert_user_id = self._session_context.customer_code
        tac.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            tac)
        await self._session_context.session.flush()
        return tac
    def _build_query(self):
        """
        Builds the base query for retrieving
        tacs.
        Returns:
            The base query for retrieving
            tacs.
        """
        logging.info("TacManager._build_query")
        query = select(
            Tac,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Tac._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Tac._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(
        self,
        query_filter
    ) -> List[Tac]:
        """
        Runs the query to retrieve
        tacs from the database.
        Args:
            query_filter: The filter to apply to the query.
        Returns:
            List[Tac]: The list of
                tacs that match the query.
        """
        logging.info("TacManager._run_query")
        tac_query_all = self._build_query()
        if query_filter is not None:
            query = tac_query_all.filter(query_filter)
        else:
            query = tac_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            tac = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            tac.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(tac)
        return result
    def _first_or_none(
        self,
        tac_list: List['Tac']
    ) -> Optional['Tac']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.
        Args:
            tac_list (List[Tac]):
                The list to retrieve
                the first element from.
        Returns:
            Optional[Tac]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            tac_list[0]
            if tac_list
            else None
        )
    async def get_by_id(self, tac_id: int) -> Optional[Tac]:
        """
        Retrieves a tac by its ID.
        Args:
            tac_id (int): The ID of the
                tac to retrieve.
        Returns:
            Optional[Tac]: The retrieved
                tac, or None if not found.
        """
        logging.info(
            "TacManager.get_by_id start tac_id: %s",
            str(tac_id))
        if not isinstance(tac_id, int):
            raise TypeError(
                "The tac_id must be an integer, "
                f"got {type(tac_id)} instead.")
        query_filter = (
            Tac._tac_id == tac_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Tac]:
        """
        Retrieves a tac
        by its code.
        Args:
            code (uuid.UUID): The code of the
                tac to retrieve.
        Returns:
            Optional[Tac]: The retrieved
                tac, or None if not found.
        """
        logging.info("TacManager.get_by_code %s", code)
        query_filter = Tac._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(
        self,
        tac: Tac, **kwargs
    ) -> Optional[Tac]:
        """
        Updates a tac with
        the specified attributes.
        Args:
            tac (Tac): The
                tac to update.
            **kwargs: The attributes to update.
        Returns:
            Optional[Tac]: The updated
                tac, or None if not found.
        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("TacManager.update")
        property_list = Tac.property_list()
        if tac:
            tac.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(tac, key, value)
            await self._session_context.session.flush()
        return tac
    async def delete(self, tac_id: int):
        """
        Deletes a tac by its ID.
        Args:
            tac_id (int): The ID of the
                tac to delete.
        Raises:
            TypeError: If the tac_id
                is not an integer.
            TacNotFoundError: If the
                tac with the
                specified ID is not found.
        """
        logging.info("TacManager.delete %s", tac_id)
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, "
                f"got {type(tac_id)} instead."
            )
        tac = await self.get_by_id(
            tac_id)
        if not tac:
            raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
        await self._session_context.session.delete(
            tac)
        await self._session_context.session.flush()
    async def get_list(
        self
    ) -> List[Tac]:
        """
        Retrieves a list of all tacs.
        Returns:
            List[Tac]: The list of
                tacs.
        """
        logging.info("TacManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(
            self,
            tac: Tac) -> str:
        """
        Serializes a Tac object
        to a JSON string.
        Args:
            tac (Tac): The
                tac to serialize.
        Returns:
            str: The JSON string representation of the
                tac.
        """
        logging.info("TacManager.to_json")
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return json.dumps(tac_data)
    def to_dict(
        self,
        tac: Tac
    ) -> Dict[str, Any]:
        """
        Serializes a Tac
        object to a dictionary.
        Args:
            tac (Tac): The
                tac to serialize.
        Returns:
            Dict[str, Any]: The dictionary representation of the
                tac.
        """
        logging.info("TacManager.to_dict")
        schema = TacSchema()
        tac_data = schema.dump(tac)
        assert isinstance(tac_data, dict)
        return tac_data
    def from_json(self, json_str: str) -> Tac:
        """
        Deserializes a JSON string into a
        Tac object.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            Tac: The deserialized
                Tac object.
        """
        logging.info("TacManager.from_json")
        schema = TacSchema()
        data = json.loads(json_str)
        tac_dict = schema.load(data)
        new_tac = Tac(**tac_dict)
        return new_tac
    def from_dict(self, tac_dict: Dict[str, Any]) -> Tac:
        """
        Creates a Tac
        instance from a dictionary of attributes.
        Args:
            tac_dict (Dict[str, Any]): A dictionary
                containing tac
                attributes.
        Returns:
            Tac: A new
                Tac instance
                created from the given
                dictionary.
        """
        logging.info("TacManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = TacSchema()
        tac_dict_converted = schema.load(
            tac_dict)
        # Create a new Tac instance
        # using the validated data
        new_tac = Tac(**tac_dict_converted)
        return new_tac
    async def add_bulk(
        self,
        tacs: List[Tac]
    ) -> List[Tac]:
        """
        Adds multiple tacs
        to the system.
        Args:
            tacs (List[Tac]): The list of
                tacs to add.
        Returns:
            List[Tac]: The added
                tacs.
        """
        logging.info("TacManager.add_bulk")
        for tac in tacs:
            tac_id = tac.tac_id
            code = tac.code
            if tac.tac_id is not None and tac.tac_id > 0:
                raise ValueError(
                    "Tac is already added"
                    f": {str(code)} {str(tac_id)}"
                )
            tac.insert_user_id = self._session_context.customer_code
            tac.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(tacs)
        await self._session_context.session.flush()
        return tacs
    async def update_bulk(
        self,
        tac_updates: List[Dict[str, Any]]
    ) -> List[Tac]:
        """
        Update multiple tacs
        with the provided updates.
        Args:
            tac_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            tac.
        Returns:
            List[Tac]: A list of updated
                Tac objects.
        Raises:
            TypeError: If the tac_id is not an integer.
            TacNotFoundError: If a
                tac with the
                provided tac_id is not found.
        """
        logging.info("TacManager.update_bulk start")
        updated_tacs = []
        for update in tac_updates:
            tac_id = update.get("tac_id")
            if not isinstance(tac_id, int):
                raise TypeError(
                    f"The tac_id must be an integer, "
                    f"got {type(tac_id)} instead."
                )
            if not tac_id:
                continue
            logging.info("TacManager.update_bulk tac_id:%s", tac_id)
            tac = await self.get_by_id(
                tac_id)
            if not tac:
                raise TacNotFoundError(
                    f"Tac with ID {tac_id} not found!")
            for key, value in update.items():
                if key != "tac_id":
                    setattr(tac, key, value)
            tac.last_update_user_id = self._session_context.customer_code
            updated_tacs.append(tac)
        await self._session_context.session.flush()
        logging.info("TacManager.update_bulk end")
        return updated_tacs
    async def delete_bulk(self, tac_ids: List[int]) -> bool:
        """
        Delete multiple tacs
        by their IDs.
        """
        logging.info("TacManager.delete_bulk")
        for tac_id in tac_ids:
            if not isinstance(tac_id, int):
                raise TypeError(
                    f"The tac_id must be an integer, "
                    f"got {type(tac_id)} instead."
                )
            tac = await self.get_by_id(
                tac_id)
            if not tac:
                raise TacNotFoundError(
                    f"Tac with ID {tac_id} not found!"
                )
            if tac:
                await self._session_context.session.delete(
                    tac)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of
        tacs.
        """
        logging.info("TacManager.count")
        result = await self._session_context.session.execute(
            select(Tac))
        return len(list(result.scalars().all()))
    async def refresh(
        self,
        tac: Tac
    ) -> Tac:
        """
        Refresh the state of a given
        tac instance
        from the database.
        """
        logging.info("TacManager.refresh")
        await self._session_context.session.refresh(tac)
        return tac
    async def exists(self, tac_id: int) -> bool:
        """
        Check if a tac
        with the given ID exists.
        """
        logging.info("TacManager.exists %s", tac_id)
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, "
                f"got {type(tac_id)} instead."
            )
        tac = await self.get_by_id(
            tac_id)
        return bool(tac)
    def is_equal(
        self,
        tac1: Tac,
        tac2: Tac
    ) -> bool:
        """
        Check if two Tac
        objects are equal.
        Args:
            tac1 (Tac): The first
                Tac object.
            tac2 (Tac): The second
                Tac object.
        Returns:
            bool: True if the two Tac
                objects are equal, False otherwise.
        Raises:
            TypeError: If either tac1
                or tac2
                is not provided or is not an instance of
                Tac.
        """
        if not tac1:
            raise TypeError("Tac1 required.")
        if not tac2:
            raise TypeError("Tac2 required.")
        if not isinstance(tac1, Tac):
            raise TypeError("The tac1 must be an "
                            "Tac instance.")
        if not isinstance(tac2, Tac):
            raise TypeError("The tac2 must be an "
                            "Tac instance.")
        dict1 = self.to_dict(tac1)
        dict2 = self.to_dict(tac2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Tac]:  # PacID
        """
        Retrieve a list of tacs by
        pac ID.
        Args:
            pac_id (int): The ID of the pac.
        Returns:
            List[Tac]: A list of
                tacs associated
                with the specified pac ID.
        """
        logging.info("TacManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The tac_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Tac._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

