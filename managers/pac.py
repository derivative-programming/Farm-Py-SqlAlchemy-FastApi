# models/managers/pac.py
# pylint: disable=unused-import

"""
This module contains the
PacManager class, which is
responsible for managing
pacs in the system.
"""

import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext

from models.pac import Pac
from models.serialization_schema.pac import PacSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class PacNotFoundError(Exception):
    """
    Exception raised when a specified
    pac is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Pac not found"):
        self.message = message
        super().__init__(self.message)


class PacEnum(Enum):
    """
    Represents an enumeration of
    Pac options.
    """
    UNKNOWN = 'Unknown'


class PacManager:
    """
    The PacManager class
    is responsible for managing
    pacs in the system.
    It provides methods for adding, updating, deleting,
    and retrieving pacs.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        PacManager class.

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

        return item

    async def initialize(self):
        """
        Initializes the PacManager.
        This method initializes the PacManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("PacManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
        if await self.from_enum(PacEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        logging.info("PacManager.Initialize end")

    async def from_enum(
        self,
        enum_val: PacEnum
    ) -> Pac:
        """
        Returns a Pac object
        based on the provided enum value.
        Args:
            enum_val (PacEnum):
                The enum value representing the filter.
        Returns:
            Pac:
                The Pac object
                matching the enum value.
        """
        query_filter = (
            Pac._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)


    async def build(self, **kwargs) -> Pac:
        """
        Builds a new Pac
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                pac.

        Returns:
            Pac: The newly created
                Pac object.
        """
        logging.info(
            "PacManager.build")
        return Pac(**kwargs)

    async def add(
        self,
        pac: Pac
    ) -> Pac:
        """
        Adds a new pac to the system.

        Args:
            pac (Pac): The
                pac to add.

        Returns:
            Pac: The added
                pac.
        """
        logging.info(
            "PacManager.add")
        pac.insert_user_id = (
            self._session_context.customer_code)
        pac.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            pac)
        await self._session_context.session.flush()
        return pac

    def _build_query(self):
        """
        Builds the base query for retrieving
        pacs.

        Returns:
            The base query for retrieving
            pacs.
        """
        logging.info(
            "PacManager._build_query")

        query = select(
            Pac,

        )


        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[Pac]:
        """
        Runs the query to retrieve
        pacs from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[Pac]: The list of
                pacs that match the query.
        """
        logging.info(
            "PacManager._run_query")
        pac_query_all = self._build_query()

        if query_filter is not None:
            query = pac_query_all.filter(query_filter)
        else:
            query = pac_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            pac = query_result_row[i]
            i = i + 1


            result.append(pac)

        return result

    def _first_or_none(
        self,
        pac_list: List['Pac']
    ) -> Optional['Pac']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            pac_list (List[Pac]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[Pac]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            pac_list[0]
            if pac_list
            else None
        )

    async def get_by_id(
        self, pac_id: int
    ) -> Optional[Pac]:
        """
        Retrieves a pac by its ID.

        Args:
            pac_id (int): The ID of the
                pac to retrieve.

        Returns:
            Optional[Pac]: The retrieved
                pac, or None if not found.
        """
        logging.info(
            "PacManager.get_by_id start pac_id: %s",
            str(pac_id))
        if not isinstance(pac_id, int):
            raise TypeError(
                "The pac_id must be an integer, "
                f"got {type(pac_id)} instead.")

        query_filter = (
            Pac._pac_id == pac_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[Pac]:
        """
        Retrieves a pac
        by its code.

        Args:
            code (uuid.UUID): The code of the
                pac to retrieve.

        Returns:
            Optional[Pac]: The retrieved
                pac, or None if not found.
        """
        logging.info("PacManager.get_by_code %s",
                     code)

        query_filter = Pac._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        pac: Pac, **kwargs
    ) -> Optional[Pac]:
        """
        Updates a pac with
        the specified attributes.

        Args:
            pac (Pac): The
                pac to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[Pac]: The updated
                pac, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("PacManager.update")
        property_list = Pac.property_list()
        if pac:
            pac.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(pac, key, value)
            await self._session_context.session.flush()
        return pac

    async def delete(self, pac_id: int):
        """
        Deletes a pac by its ID.

        Args:
            pac_id (int): The ID of the
                pac to delete.

        Raises:
            TypeError: If the pac_id
                is not an integer.
            PacNotFoundError: If the
                pac with the
                specified ID is not found.
        """
        logging.info(
            "PacManager.delete %s",
            pac_id)
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The pac_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        pac = await self.get_by_id(
            pac_id)
        if not pac:
            raise PacNotFoundError(
                f"Pac with ID {pac_id} not found!")

        await self._session_context.session.delete(
            pac)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[Pac]:
        """
        Retrieves a list of all pacs.

        Returns:
            List[Pac]: The list of
                pacs.
        """
        logging.info(
            "PacManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            pac: Pac) -> str:
        """
        Serializes a Pac object
        to a JSON string.

        Args:
            pac (Pac): The
                pac to serialize.

        Returns:
            str: The JSON string representation of the
                pac.
        """
        logging.info(
            "PacManager.to_json")
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return json.dumps(pac_data)

    def to_dict(
        self,
        pac: Pac
    ) -> Dict[str, Any]:
        """
        Serializes a Pac
        object to a dictionary.

        Args:
            pac (Pac): The
                pac to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                pac.
        """
        logging.info(
            "PacManager.to_dict")
        schema = PacSchema()
        pac_data = schema.dump(pac)

        assert isinstance(pac_data, dict)

        return pac_data

    async def from_json(self, json_str: str) -> Pac:
        """
        Deserializes a JSON string into a
        Pac object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            Pac: The deserialized
                Pac object.
        """
        logging.info(
            "PacManager.from_json")
        schema = PacSchema()
        data = json.loads(json_str)
        pac_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_pac = Pac(**pac_dict)

        # load or create
        new_pac = await self.get_by_id(
            pac_dict["pac_id"])
        if new_pac is None:
            new_pac = Pac(**pac_dict)
            self._session_context.session.add(new_pac)
        else:
            for key, value in pac_dict.items():
                setattr(new_pac, key, value)

        return new_pac

    async def from_dict(
        self, pac_dict: Dict[str, Any]
    ) -> Pac:
        """
        Creates a Pac
        instance from a dictionary of attributes.

        Args:
            pac_dict (Dict[str, Any]): A dictionary
                containing pac
                attributes.

        Returns:
            Pac: A new
                Pac instance
                created from the given
                dictionary.
        """
        logging.info(
            "PacManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = PacSchema()
        pac_dict_converted = schema.load(
            pac_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new Pac instance
        # using the validated data
        # new_pac = Pac(**pac_dict_converted)

        # load or create
        new_pac = await self.get_by_id(
            pac_dict_converted["pac_id"])
        if new_pac is None:
            new_pac = Pac(**pac_dict_converted)
            self._session_context.session.add(new_pac)
        else:
            for key, value in pac_dict_converted.items():
                setattr(new_pac, key, value)

        return new_pac

    async def add_bulk(
        self,
        pacs: List[Pac]
    ) -> List[Pac]:
        """
        Adds multiple pacs
        to the system.

        Args:
            pacs (List[Pac]): The list of
                pacs to add.

        Returns:
            List[Pac]: The added
                pacs.
        """
        logging.info(
            "PacManager.add_bulk")
        for pac in pacs:
            pac_id = pac.pac_id
            code = pac.code
            if pac.pac_id is not None and pac.pac_id > 0:
                raise ValueError(
                    "Pac is already added"
                    f": {str(code)} {str(pac_id)}"
                )
            pac.insert_user_id = (
                self._session_context.customer_code)
            pac.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(pacs)
        await self._session_context.session.flush()
        return pacs

    async def update_bulk(
        self,
        pac_updates: List[Dict[str, Any]]
    ) -> List[Pac]:
        """
        Update multiple pacs
        with the provided updates.

        Args:
            pac_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            pac.

        Returns:
            List[Pac]: A list of updated
                Pac objects.

        Raises:
            TypeError: If the pac_id is not an integer.
            PacNotFoundError: If a
                pac with the
                provided pac_id is not found.
        """

        logging.info(
            "PacManager.update_bulk start")
        updated_pacs = []
        for update in pac_updates:
            pac_id = update.get("pac_id")
            if not isinstance(pac_id, int):
                raise TypeError(
                    f"The pac_id must be an integer, "
                    f"got {type(pac_id)} instead."
                )
            if not pac_id:
                continue

            logging.info(
                "PacManager.update_bulk pac_id:%s",
                pac_id)

            pac = await self.get_by_id(
                pac_id)

            if not pac:
                raise PacNotFoundError(
                    f"Pac with ID {pac_id} not found!")

            for key, value in update.items():
                if key != "pac_id":
                    setattr(pac, key, value)

            pac.last_update_user_id = self._session_context.customer_code

            updated_pacs.append(pac)

        await self._session_context.session.flush()

        logging.info(
            "PacManager.update_bulk end")

        return updated_pacs

    async def delete_bulk(self, pac_ids: List[int]) -> bool:
        """
        Delete multiple pacs
        by their IDs.
        """
        logging.info(
            "PacManager.delete_bulk")

        for pac_id in pac_ids:
            if not isinstance(pac_id, int):
                raise TypeError(
                    f"The pac_id must be an integer, "
                    f"got {type(pac_id)} instead."
                )

            pac = await self.get_by_id(
                pac_id)
            if not pac:
                raise PacNotFoundError(
                    f"Pac with ID {pac_id} not found!"
                )

            if pac:
                await self._session_context.session.delete(
                    pac)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        pacs.
        """
        logging.info(
            "PacManager.count")
        result = await self._session_context.session.execute(
            select(Pac))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        pac: Pac
    ) -> Pac:
        """
        Refresh the state of a given
        pac instance
        from the database.
        """

        logging.info(
            "PacManager.refresh")

        await self._session_context.session.refresh(pac)

        return pac

    async def exists(self, pac_id: int) -> bool:
        """
        Check if a pac
        with the given ID exists.
        """
        logging.info(
            "PacManager.exists %s",
            pac_id)
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The pac_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        pac = await self.get_by_id(
            pac_id)
        return bool(pac)

    def is_equal(
        self,
        pac1: Pac,
        pac2: Pac
    ) -> bool:
        """
        Check if two Pac
        objects are equal.

        Args:
            pac1 (Pac): The first
                Pac object.
            pac2 (Pac): The second
                Pac object.

        Returns:
            bool: True if the two Pac
                objects are equal, False otherwise.

        Raises:
            TypeError: If either pac1
                or pac2
                is not provided or is not an instance of
                Pac.
        """
        if not pac1:
            raise TypeError("Pac1 required.")

        if not pac2:
            raise TypeError("Pac2 required.")

        if not isinstance(pac1, Pac):
            raise TypeError("The pac1 must be an "
                            "Pac instance.")

        if not isinstance(pac2, Pac):
            raise TypeError("The pac2 must be an "
                            "Pac instance.")

        dict1 = self.to_dict(pac1)
        dict2 = self.to_dict(pac2)

        return dict1 == dict2

