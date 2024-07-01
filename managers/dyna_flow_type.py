# models/managers/dyna_flow_type.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeManager class, which is
responsible for managing
dyna_flow_types in the system.
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
from models.dyna_flow_type import DynaFlowType
from models.serialization_schema.dyna_flow_type import DynaFlowTypeSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DynaFlowTypeNotFoundError(Exception):
    """
    Exception raised when a specified
    dyna_flow_type is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DynaFlowType not found"):
        self.message = message
        super().__init__(self.message)


class DynaFlowTypeEnum(Enum):
    """
    Represents an enumeration of
    Dyna Flow Type options.
    """
    UNKNOWN = 'Unknown'
    PACPROCESSALLDYNAFLOWTYPESCHEDULEFLOW = 'PacProcessAllDynaFlowTypeScheduleFlow'
    PLANTSAMPLEWORKFLOW = 'PlantSampleWorkflow'


class DynaFlowTypeManager:
    """
    The DynaFlowTypeManager class
    is responsible for managing
    dyna_flow_types in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dyna_flow_types.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DynaFlowTypeManager class.

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
        Initializes the DynaFlowTypeManager.
        This method initializes the DynaFlowTypeManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("DynaFlowTypeManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
        if await self.from_enum(DynaFlowTypeEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.priority_level = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTypeEnum.PACPROCESSALLDYNAFLOWTYPESCHEDULEFLOW) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Pac Process All Dyna Flow Type Schedule Flow"
            item.lookup_enum_name = "PacProcessAllDynaFlowTypeScheduleFlow"
            item.description = "Pac Process All Dyna Flow Type Schedule Flow"
            item.display_order = await self.count()
            item.is_active = True
            # item.priority_level = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTypeEnum.PLANTSAMPLEWORKFLOW) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Plant Sample Workflow"
            item.lookup_enum_name = "PlantSampleWorkflow"
            item.description = "Plant Sample Workflow"
            item.display_order = await self.count()
            item.is_active = True
            # item.priority_level = 1
            await self.add(item)
        logging.info("DynaFlowTypeManager.Initialize end")

    async def from_enum(
        self,
        enum_val: DynaFlowTypeEnum
    ) -> DynaFlowType:
        """
        Returns a DynaFlowType object
        based on the provided enum value.
        Args:
            enum_val (DynaFlowTypeEnum):
                The enum value representing the filter.
        Returns:
            DynaFlowType:
                The DynaFlowType object
                matching the enum value.
        """
        query_filter = (
            DynaFlowType._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)


    async def build(self, **kwargs) -> DynaFlowType:
        """
        Builds a new DynaFlowType
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dyna_flow_type.

        Returns:
            DynaFlowType: The newly created
                DynaFlowType object.
        """
        logging.info(
            "DynaFlowTypeManager.build")
        return DynaFlowType(**kwargs)

    async def add(
        self,
        dyna_flow_type: DynaFlowType
    ) -> DynaFlowType:
        """
        Adds a new dyna_flow_type to the system.

        Args:
            dyna_flow_type (DynaFlowType): The
                dyna_flow_type to add.

        Returns:
            DynaFlowType: The added
                dyna_flow_type.
        """
        logging.info(
            "DynaFlowTypeManager.add")
        dyna_flow_type.insert_user_id = (
            self._session_context.customer_code)
        dyna_flow_type.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dyna_flow_type)
        await self._session_context.session.flush()
        return dyna_flow_type

    def _build_query(self):
        """
        Builds the base query for retrieving
        dyna_flow_types.

        Returns:
            The base query for retrieving
            dyna_flow_types.
        """
        logging.info(
            "DynaFlowTypeManager._build_query")

        query = select(
            DynaFlowType,
            Pac,  # pac_id
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DynaFlowType._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowType._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DynaFlowType]:
        """
        Runs the query to retrieve
        dyna_flow_types from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DynaFlowType]: The list of
                dyna_flow_types that match the query.
        """
        logging.info(
            "DynaFlowTypeManager._run_query")
        dyna_flow_type_query_all = self._build_query()

        if query_filter is not None:
            query = dyna_flow_type_query_all.filter(query_filter)
        else:
            query = dyna_flow_type_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            dyna_flow_type = query_result_row[i]
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            dyna_flow_type.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(dyna_flow_type)

        return result

    def _first_or_none(
        self,
        dyna_flow_type_list: List['DynaFlowType']
    ) -> Optional['DynaFlowType']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dyna_flow_type_list (List[DynaFlowType]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DynaFlowType]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dyna_flow_type_list[0]
            if dyna_flow_type_list
            else None
        )

    async def get_by_id(
        self, dyna_flow_type_id: int
    ) -> Optional[DynaFlowType]:
        """
        Retrieves a dyna_flow_type by its ID.

        Args:
            dyna_flow_type_id (int): The ID of the
                dyna_flow_type to retrieve.

        Returns:
            Optional[DynaFlowType]: The retrieved
                dyna_flow_type, or None if not found.
        """
        logging.info(
            "DynaFlowTypeManager.get_by_id start dyna_flow_type_id: %s",
            str(dyna_flow_type_id))
        if not isinstance(dyna_flow_type_id, int):
            raise TypeError(
                "The dyna_flow_type_id must be an integer, "
                f"got {type(dyna_flow_type_id)} instead.")

        query_filter = (
            DynaFlowType._dyna_flow_type_id == dyna_flow_type_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DynaFlowType]:
        """
        Retrieves a dyna_flow_type
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dyna_flow_type to retrieve.

        Returns:
            Optional[DynaFlowType]: The retrieved
                dyna_flow_type, or None if not found.
        """
        logging.info("DynaFlowTypeManager.get_by_code %s",
                     code)

        query_filter = DynaFlowType._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dyna_flow_type: DynaFlowType, **kwargs
    ) -> Optional[DynaFlowType]:
        """
        Updates a dyna_flow_type with
        the specified attributes.

        Args:
            dyna_flow_type (DynaFlowType): The
                dyna_flow_type to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DynaFlowType]: The updated
                dyna_flow_type, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DynaFlowTypeManager.update")
        property_list = DynaFlowType.property_list()
        if dyna_flow_type:
            dyna_flow_type.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dyna_flow_type, key, value)
            await self._session_context.session.flush()
        return dyna_flow_type

    async def delete(self, dyna_flow_type_id: int):
        """
        Deletes a dyna_flow_type by its ID.

        Args:
            dyna_flow_type_id (int): The ID of the
                dyna_flow_type to delete.

        Raises:
            TypeError: If the dyna_flow_type_id
                is not an integer.
            DynaFlowTypeNotFoundError: If the
                dyna_flow_type with the
                specified ID is not found.
        """
        logging.info(
            "DynaFlowTypeManager.delete %s",
            dyna_flow_type_id)
        if not isinstance(dyna_flow_type_id, int):
            raise TypeError(
                f"The dyna_flow_type_id must be an integer, "
                f"got {type(dyna_flow_type_id)} instead."
            )
        dyna_flow_type = await self.get_by_id(
            dyna_flow_type_id)
        if not dyna_flow_type:
            raise DynaFlowTypeNotFoundError(
                f"DynaFlowType with ID {dyna_flow_type_id} not found!")

        await self._session_context.session.delete(
            dyna_flow_type)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DynaFlowType]:
        """
        Retrieves a list of all dyna_flow_types.

        Returns:
            List[DynaFlowType]: The list of
                dyna_flow_types.
        """
        logging.info(
            "DynaFlowTypeManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dyna_flow_type: DynaFlowType) -> str:
        """
        Serializes a DynaFlowType object
        to a JSON string.

        Args:
            dyna_flow_type (DynaFlowType): The
                dyna_flow_type to serialize.

        Returns:
            str: The JSON string representation of the
                dyna_flow_type.
        """
        logging.info(
            "DynaFlowTypeManager.to_json")
        schema = DynaFlowTypeSchema()
        dyna_flow_type_data = schema.dump(dyna_flow_type)
        return json.dumps(dyna_flow_type_data)

    def to_dict(
        self,
        dyna_flow_type: DynaFlowType
    ) -> Dict[str, Any]:
        """
        Serializes a DynaFlowType
        object to a dictionary.

        Args:
            dyna_flow_type (DynaFlowType): The
                dyna_flow_type to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dyna_flow_type.
        """
        logging.info(
            "DynaFlowTypeManager.to_dict")
        schema = DynaFlowTypeSchema()
        dyna_flow_type_data = schema.dump(dyna_flow_type)

        assert isinstance(dyna_flow_type_data, dict)

        return dyna_flow_type_data

    async def from_json(self, json_str: str) -> DynaFlowType:
        """
        Deserializes a JSON string into a
        DynaFlowType object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DynaFlowType: The deserialized
                DynaFlowType object.
        """
        logging.info(
            "DynaFlowTypeManager.from_json")
        schema = DynaFlowTypeSchema()
        data = json.loads(json_str)
        dyna_flow_type_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_dyna_flow_type = DynaFlowType(**dyna_flow_type_dict)

        # load or create
        new_dyna_flow_type = await self.get_by_id(
            dyna_flow_type_dict["dyna_flow_type_id"])
        if new_dyna_flow_type is None:
            new_dyna_flow_type = DynaFlowType(**dyna_flow_type_dict)
            self._session_context.session.add(new_dyna_flow_type)
        else:
            for key, value in dyna_flow_type_dict.items():
                setattr(new_dyna_flow_type, key, value)

        return new_dyna_flow_type

    async def from_dict(
        self, dyna_flow_type_dict: Dict[str, Any]
    ) -> DynaFlowType:
        """
        Creates a DynaFlowType
        instance from a dictionary of attributes.

        Args:
            dyna_flow_type_dict (Dict[str, Any]): A dictionary
                containing dyna_flow_type
                attributes.

        Returns:
            DynaFlowType: A new
                DynaFlowType instance
                created from the given
                dictionary.
        """
        logging.info(
            "DynaFlowTypeManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DynaFlowTypeSchema()
        dyna_flow_type_dict_converted = schema.load(
            dyna_flow_type_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new DynaFlowType instance
        # using the validated data
        # new_dyna_flow_type = DynaFlowType(**dyna_flow_type_dict_converted)

        # load or create
        new_dyna_flow_type = await self.get_by_id(
            dyna_flow_type_dict_converted["dyna_flow_type_id"])
        if new_dyna_flow_type is None:
            new_dyna_flow_type = DynaFlowType(**dyna_flow_type_dict_converted)
            self._session_context.session.add(new_dyna_flow_type)
        else:
            for key, value in dyna_flow_type_dict_converted.items():
                setattr(new_dyna_flow_type, key, value)

        return new_dyna_flow_type

    async def add_bulk(
        self,
        dyna_flow_types: List[DynaFlowType]
    ) -> List[DynaFlowType]:
        """
        Adds multiple dyna_flow_types
        to the system.

        Args:
            dyna_flow_types (List[DynaFlowType]): The list of
                dyna_flow_types to add.

        Returns:
            List[DynaFlowType]: The added
                dyna_flow_types.
        """
        logging.info(
            "DynaFlowTypeManager.add_bulk")
        for list_item in dyna_flow_types:
            dyna_flow_type_id = \
                list_item.dyna_flow_type_id
            code = list_item.code
            if list_item.dyna_flow_type_id is not None and \
                    list_item.dyna_flow_type_id > 0:
                raise ValueError(
                    "DynaFlowType is already added"
                    f": {str(code)} {str(dyna_flow_type_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dyna_flow_types)
        await self._session_context.session.flush()
        return dyna_flow_types

    async def update_bulk(
        self,
        dyna_flow_type_updates: List[Dict[str, Any]]
    ) -> List[DynaFlowType]:
        """
        Update multiple dyna_flow_types
        with the provided updates.

        Args:
            dyna_flow_type_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dyna_flow_type.

        Returns:
            List[DynaFlowType]: A list of updated
                DynaFlowType objects.

        Raises:
            TypeError: If the dyna_flow_type_id is not an integer.
            DynaFlowTypeNotFoundError: If a
                dyna_flow_type with the
                provided dyna_flow_type_id is not found.
        """

        logging.info(
            "DynaFlowTypeManager.update_bulk start")
        updated_dyna_flow_types = []
        for update in dyna_flow_type_updates:
            dyna_flow_type_id = update.get("dyna_flow_type_id")
            if not isinstance(dyna_flow_type_id, int):
                raise TypeError(
                    f"The dyna_flow_type_id must be an integer, "
                    f"got {type(dyna_flow_type_id)} instead."
                )
            if not dyna_flow_type_id:
                continue

            logging.info(
                "DynaFlowTypeManager.update_bulk dyna_flow_type_id:%s",
                dyna_flow_type_id)

            dyna_flow_type = await self.get_by_id(
                dyna_flow_type_id)

            if not dyna_flow_type:
                raise DynaFlowTypeNotFoundError(
                    f"DynaFlowType with ID {dyna_flow_type_id} not found!")

            for key, value in update.items():
                if key != "dyna_flow_type_id":
                    setattr(dyna_flow_type, key, value)

            dyna_flow_type.last_update_user_id =\
                self._session_context.customer_code

            updated_dyna_flow_types.append(dyna_flow_type)

        await self._session_context.session.flush()

        logging.info(
            "DynaFlowTypeManager.update_bulk end")

        return updated_dyna_flow_types

    async def delete_bulk(self, dyna_flow_type_ids: List[int]) -> bool:
        """
        Delete multiple dyna_flow_types
        by their IDs.
        """
        logging.info(
            "DynaFlowTypeManager.delete_bulk")

        for dyna_flow_type_id in dyna_flow_type_ids:
            if not isinstance(dyna_flow_type_id, int):
                raise TypeError(
                    f"The dyna_flow_type_id must be an integer, "
                    f"got {type(dyna_flow_type_id)} instead."
                )

            dyna_flow_type = await self.get_by_id(
                dyna_flow_type_id)
            if not dyna_flow_type:
                raise DynaFlowTypeNotFoundError(
                    f"DynaFlowType with ID {dyna_flow_type_id} not found!"
                )

            if dyna_flow_type:
                await self._session_context.session.delete(
                    dyna_flow_type)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dyna_flow_types.
        """
        logging.info(
            "DynaFlowTypeManager.count")
        result = await self._session_context.session.execute(
            select(DynaFlowType))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dyna_flow_type: DynaFlowType
    ) -> DynaFlowType:
        """
        Refresh the state of a given
        dyna_flow_type instance
        from the database.
        """

        logging.info(
            "DynaFlowTypeManager.refresh")

        await self._session_context.session.refresh(dyna_flow_type)

        return dyna_flow_type

    async def exists(self, dyna_flow_type_id: int) -> bool:
        """
        Check if a dyna_flow_type
        with the given ID exists.
        """
        logging.info(
            "DynaFlowTypeManager.exists %s",
            dyna_flow_type_id)
        if not isinstance(dyna_flow_type_id, int):
            raise TypeError(
                f"The dyna_flow_type_id must be an integer, "
                f"got {type(dyna_flow_type_id)} instead."
            )
        dyna_flow_type = await self.get_by_id(
            dyna_flow_type_id)
        return bool(dyna_flow_type)

    def is_equal(
        self,
        dyna_flow_type1: DynaFlowType,
        dyna_flow_type2: DynaFlowType
    ) -> bool:
        """
        Check if two DynaFlowType
        objects are equal.

        Args:
            dyna_flow_type1 (DynaFlowType): The first
                DynaFlowType object.
            dyna_flow_type2 (DynaFlowType): The second
                DynaFlowType object.

        Returns:
            bool: True if the two DynaFlowType
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dyna_flow_type1
                or dyna_flow_type2
                is not provided or is not an instance of
                DynaFlowType.
        """
        if not dyna_flow_type1:
            raise TypeError("DynaFlowType1 required.")

        if not dyna_flow_type2:
            raise TypeError("DynaFlowType2 required.")

        if not isinstance(dyna_flow_type1,
                          DynaFlowType):
            raise TypeError("The dyna_flow_type1 must be an "
                            "DynaFlowType instance.")

        if not isinstance(dyna_flow_type2,
                          DynaFlowType):
            raise TypeError("The dyna_flow_type2 must be an "
                            "DynaFlowType instance.")

        dict1 = self.to_dict(dyna_flow_type1)
        dict2 = self.to_dict(dyna_flow_type2)

        return dict1 == dict2
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[DynaFlowType]:
        """
        Retrieve a list of dyna_flow_types by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[DynaFlowType]: A list of
                dyna_flow_types associated
                with the specified pac ID.
        """

        logging.info(
            "DynaFlowTypeManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The dyna_flow_type_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = DynaFlowType._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
