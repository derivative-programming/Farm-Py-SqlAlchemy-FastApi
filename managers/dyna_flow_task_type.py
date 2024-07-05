# models/managers/dyna_flow_task_type.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskTypeManager class, which is
responsible for managing
dyna_flow_task_types in the system.
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
from models.dyna_flow_task_type import DynaFlowTaskType
from models.serialization_schema.dyna_flow_task_type import DynaFlowTaskTypeSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DynaFlowTaskTypeNotFoundError(Exception):
    """
    Exception raised when a specified
    dyna_flow_task_type is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DynaFlowTaskType not found"):
        self.message = message
        super().__init__(self.message)


class DynaFlowTaskTypeEnum(Enum):
    """
    Represents an enumeration of
    Dyna Flow Task Type options.
    """
    UNKNOWN = 'Unknown'
    DYNAFLOWTASKDYNAFLOWCLEANUP = 'DynaFlowTaskDynaFlowCleanup'
    PROCESSALLDYNAFLOWTYPESCHEDULETASK = 'ProcessAllDynaFlowTypeScheduleTask'
    DYNAFLOWTASKPLANTTASKONE = 'DynaFlowTaskPlantTaskOne'
    DYNAFLOWTASKPLANTTASKTWO = 'DynaFlowTaskPlantTaskTwo'


class DynaFlowTaskTypeManager:
    """
    The DynaFlowTaskTypeManager class
    is responsible for managing
    dyna_flow_task_types in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dyna_flow_task_types.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DynaFlowTaskTypeManager class.

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
        Initializes the DynaFlowTaskTypeManager.
        This method initializes the DynaFlowTaskTypeManager
        by adding predefined filter items to the database.
        If the filter items do not already exist in the database,
        they are created and added.
        Returns:
            None
        Raises:
            None
        """
        logging.info("DynaFlowTaskTypeManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
        if await self.from_enum(DynaFlowTaskTypeEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.max_retry_count = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTaskTypeEnum.DYNAFLOWTASKDYNAFLOWCLEANUP) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Dyna Flow Task Dyna Flow Cleanup"
            item.lookup_enum_name = "DynaFlowTaskDynaFlowCleanup"
            item.description = "Dyna Flow Task Dyna Flow Cleanup"
            item.display_order = await self.count()
            item.is_active = True
            # item.max_retry_count = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTaskTypeEnum.PROCESSALLDYNAFLOWTYPESCHEDULETASK) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Process All Scheduled DynaFlowTypes"
            item.lookup_enum_name = "ProcessAllDynaFlowTypeScheduleTask"
            item.description = "Process All Scheduled DynaFlowTypes"
            item.display_order = await self.count()
            item.is_active = True
            # item.max_retry_count = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTaskTypeEnum.DYNAFLOWTASKPLANTTASKONE) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Dyna Flow Task Plant Task One"
            item.lookup_enum_name = "DynaFlowTaskPlantTaskOne"
            item.description = "Dyna Flow Task Plant Task One"
            item.display_order = await self.count()
            item.is_active = True
            # item.max_retry_count = 1
            await self.add(item)
        if await self.from_enum(DynaFlowTaskTypeEnum.DYNAFLOWTASKPLANTTASKTWO) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Dyna Flow Task Plant Task Two"
            item.lookup_enum_name = "DynaFlowTaskPlantTaskTwo"
            item.description = "Dyna Flow Task Plant Task Two"
            item.display_order = await self.count()
            item.is_active = True
            # item.max_retry_count = 1
            await self.add(item)
        logging.info("DynaFlowTaskTypeManager.Initialize end")

    async def from_enum(
        self,
        enum_val: DynaFlowTaskTypeEnum
    ) -> DynaFlowTaskType:
        """
        Returns a DynaFlowTaskType object
        based on the provided enum value.
        Args:
            enum_val (DynaFlowTaskTypeEnum):
                The enum value representing the filter.
        Returns:
            DynaFlowTaskType:
                The DynaFlowTaskType object
                matching the enum value.
        """
        query_filter = (
            DynaFlowTaskType._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)


    async def build(self, **kwargs) -> DynaFlowTaskType:
        """
        Builds a new DynaFlowTaskType
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dyna_flow_task_type.

        Returns:
            DynaFlowTaskType: The newly created
                DynaFlowTaskType object.
        """
        logging.info(
            "DynaFlowTaskTypeManager.build")
        return DynaFlowTaskType(**kwargs)

    async def add(
        self,
        dyna_flow_task_type: DynaFlowTaskType
    ) -> DynaFlowTaskType:
        """
        Adds a new dyna_flow_task_type to the system.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                dyna_flow_task_type to add.

        Returns:
            DynaFlowTaskType: The added
                dyna_flow_task_type.
        """
        logging.info(
            "DynaFlowTaskTypeManager.add")
        dyna_flow_task_type.insert_user_id = (
            self._session_context.customer_code)
        dyna_flow_task_type.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dyna_flow_task_type)
        await self._session_context.session.flush()
        return dyna_flow_task_type

    def _build_query(self):
        """
        Builds the base query for retrieving
        dyna_flow_task_types.

        Returns:
            The base query for retrieving
            dyna_flow_task_types.
        """
        logging.info(
            "DynaFlowTaskTypeManager._build_query")

        query = select(
            DynaFlowTaskType,
            Pac,  # pac_id
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DynaFlowTaskType._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowTaskType._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DynaFlowTaskType]:
        """
        Runs the query to retrieve
        dyna_flow_task_types from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DynaFlowTaskType]: The list of
                dyna_flow_task_types that match the query.
        """
        logging.info(
            "DynaFlowTaskTypeManager._run_query")
        dyna_flow_task_type_query_all = self._build_query()

        if query_filter is not None:
            query = dyna_flow_task_type_query_all.filter(query_filter)
        else:
            query = dyna_flow_task_type_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            dyna_flow_task_type = query_result_row[i]
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            dyna_flow_task_type.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(dyna_flow_task_type)

        return result

    def _first_or_none(
        self,
        dyna_flow_task_type_list: List['DynaFlowTaskType']
    ) -> Optional['DynaFlowTaskType']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dyna_flow_task_type_list (List[DynaFlowTaskType]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DynaFlowTaskType]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dyna_flow_task_type_list[0]
            if dyna_flow_task_type_list
            else None
        )

    async def get_by_id(
        self, dyna_flow_task_type_id: int
    ) -> Optional[DynaFlowTaskType]:
        """
        Retrieves a dyna_flow_task_type by its ID.

        Args:
            dyna_flow_task_type_id (int): The ID of the
                dyna_flow_task_type to retrieve.

        Returns:
            Optional[DynaFlowTaskType]: The retrieved
                dyna_flow_task_type, or None if not found.
        """
        logging.info(
            "DynaFlowTaskTypeManager.get_by_id start dyna_flow_task_type_id: %s",
            str(dyna_flow_task_type_id))
        if not isinstance(dyna_flow_task_type_id, int):
            raise TypeError(
                "The dyna_flow_task_type_id must be an integer, "
                f"got {type(dyna_flow_task_type_id)} instead.")

        query_filter = (
            DynaFlowTaskType._dyna_flow_task_type_id == dyna_flow_task_type_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DynaFlowTaskType]:
        """
        Retrieves a dyna_flow_task_type
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dyna_flow_task_type to retrieve.

        Returns:
            Optional[DynaFlowTaskType]: The retrieved
                dyna_flow_task_type, or None if not found.
        """
        logging.info("DynaFlowTaskTypeManager.get_by_code %s",
                     code)

        query_filter = DynaFlowTaskType._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dyna_flow_task_type: DynaFlowTaskType, **kwargs
    ) -> Optional[DynaFlowTaskType]:
        """
        Updates a dyna_flow_task_type with
        the specified attributes.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                dyna_flow_task_type to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DynaFlowTaskType]: The updated
                dyna_flow_task_type, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DynaFlowTaskTypeManager.update")
        property_list = DynaFlowTaskType.property_list()
        if dyna_flow_task_type:
            dyna_flow_task_type.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dyna_flow_task_type, key, value)
            await self._session_context.session.flush()
        return dyna_flow_task_type

    async def delete(self, dyna_flow_task_type_id: int):
        """
        Deletes a dyna_flow_task_type by its ID.

        Args:
            dyna_flow_task_type_id (int): The ID of the
                dyna_flow_task_type to delete.

        Raises:
            TypeError: If the dyna_flow_task_type_id
                is not an integer.
            DynaFlowTaskTypeNotFoundError: If the
                dyna_flow_task_type with the
                specified ID is not found.
        """
        logging.info(
            "DynaFlowTaskTypeManager.delete %s",
            dyna_flow_task_type_id)
        if not isinstance(dyna_flow_task_type_id, int):
            raise TypeError(
                f"The dyna_flow_task_type_id must be an integer, "
                f"got {type(dyna_flow_task_type_id)} instead."
            )
        dyna_flow_task_type = await self.get_by_id(
            dyna_flow_task_type_id)
        if not dyna_flow_task_type:
            raise DynaFlowTaskTypeNotFoundError(
                f"DynaFlowTaskType with ID {dyna_flow_task_type_id} not found!")

        await self._session_context.session.delete(
            dyna_flow_task_type)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DynaFlowTaskType]:
        """
        Retrieves a list of all dyna_flow_task_types.

        Returns:
            List[DynaFlowTaskType]: The list of
                dyna_flow_task_types.
        """
        logging.info(
            "DynaFlowTaskTypeManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dyna_flow_task_type: DynaFlowTaskType) -> str:
        """
        Serializes a DynaFlowTaskType object
        to a JSON string.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                dyna_flow_task_type to serialize.

        Returns:
            str: The JSON string representation of the
                dyna_flow_task_type.
        """
        logging.info(
            "DynaFlowTaskTypeManager.to_json")
        schema = DynaFlowTaskTypeSchema()
        dyna_flow_task_type_data = schema.dump(dyna_flow_task_type)
        return json.dumps(dyna_flow_task_type_data)

    def to_dict(
        self,
        dyna_flow_task_type: DynaFlowTaskType
    ) -> Dict[str, Any]:
        """
        Serializes a DynaFlowTaskType
        object to a dictionary.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                dyna_flow_task_type to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dyna_flow_task_type.
        """
        logging.info(
            "DynaFlowTaskTypeManager.to_dict")
        schema = DynaFlowTaskTypeSchema()
        dyna_flow_task_type_data = schema.dump(dyna_flow_task_type)

        assert isinstance(dyna_flow_task_type_data, dict)

        return dyna_flow_task_type_data

    async def from_json(self, json_str: str) -> DynaFlowTaskType:
        """
        Deserializes a JSON string into a
        DynaFlowTaskType object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DynaFlowTaskType: The deserialized
                DynaFlowTaskType object.
        """
        logging.info(
            "DynaFlowTaskTypeManager.from_json")
        schema = DynaFlowTaskTypeSchema()
        data = json.loads(json_str)
        dyna_flow_task_type_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_dyna_flow_task_type = DynaFlowTaskType(**dyna_flow_task_type_dict)

        # load or create
        new_dyna_flow_task_type = await self.get_by_id(
            dyna_flow_task_type_dict["dyna_flow_task_type_id"])
        if new_dyna_flow_task_type is None:
            new_dyna_flow_task_type = DynaFlowTaskType(**dyna_flow_task_type_dict)
            self._session_context.session.add(new_dyna_flow_task_type)
        else:
            for key, value in dyna_flow_task_type_dict.items():
                setattr(new_dyna_flow_task_type, key, value)

        return new_dyna_flow_task_type

    async def from_dict(
        self, dyna_flow_task_type_dict: Dict[str, Any]
    ) -> DynaFlowTaskType:
        """
        Creates a DynaFlowTaskType
        instance from a dictionary of attributes.

        Args:
            dyna_flow_task_type_dict (Dict[str, Any]): A dictionary
                containing dyna_flow_task_type
                attributes.

        Returns:
            DynaFlowTaskType: A new
                DynaFlowTaskType instance
                created from the given
                dictionary.
        """
        logging.info(
            "DynaFlowTaskTypeManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DynaFlowTaskTypeSchema()
        dyna_flow_task_type_dict_converted = schema.load(
            dyna_flow_task_type_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new DynaFlowTaskType instance
        # using the validated data
        # new_dyna_flow_task_type = DynaFlowTaskType(**dyna_flow_task_type_dict_converted)

        # load or create
        new_dyna_flow_task_type = await self.get_by_id(
            dyna_flow_task_type_dict_converted["dyna_flow_task_type_id"])
        if new_dyna_flow_task_type is None:
            new_dyna_flow_task_type = DynaFlowTaskType(**dyna_flow_task_type_dict_converted)
            self._session_context.session.add(new_dyna_flow_task_type)
        else:
            for key, value in dyna_flow_task_type_dict_converted.items():
                setattr(new_dyna_flow_task_type, key, value)

        return new_dyna_flow_task_type

    async def add_bulk(
        self,
        dyna_flow_task_types: List[DynaFlowTaskType]
    ) -> List[DynaFlowTaskType]:
        """
        Adds multiple dyna_flow_task_types
        to the system.

        Args:
            dyna_flow_task_types (List[DynaFlowTaskType]): The list of
                dyna_flow_task_types to add.

        Returns:
            List[DynaFlowTaskType]: The added
                dyna_flow_task_types.
        """
        logging.info(
            "DynaFlowTaskTypeManager.add_bulk")
        for list_item in dyna_flow_task_types:
            dyna_flow_task_type_id = \
                list_item.dyna_flow_task_type_id
            code = list_item.code
            if list_item.dyna_flow_task_type_id is not None and \
                    list_item.dyna_flow_task_type_id > 0:
                raise ValueError(
                    "DynaFlowTaskType is already added"
                    f": {str(code)} {str(dyna_flow_task_type_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dyna_flow_task_types)
        await self._session_context.session.flush()
        return dyna_flow_task_types

    async def update_bulk(
        self,
        dyna_flow_task_type_updates: List[Dict[str, Any]]
    ) -> List[DynaFlowTaskType]:
        """
        Update multiple dyna_flow_task_types
        with the provided updates.

        Args:
            dyna_flow_task_type_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dyna_flow_task_type.

        Returns:
            List[DynaFlowTaskType]: A list of updated
                DynaFlowTaskType objects.

        Raises:
            TypeError: If the dyna_flow_task_type_id is not an integer.
            DynaFlowTaskTypeNotFoundError: If a
                dyna_flow_task_type with the
                provided dyna_flow_task_type_id is not found.
        """

        logging.info(
            "DynaFlowTaskTypeManager.update_bulk start")
        updated_dyna_flow_task_types = []
        for update in dyna_flow_task_type_updates:
            dyna_flow_task_type_id = update.get("dyna_flow_task_type_id")
            if not isinstance(dyna_flow_task_type_id, int):
                raise TypeError(
                    f"The dyna_flow_task_type_id must be an integer, "
                    f"got {type(dyna_flow_task_type_id)} instead."
                )
            if not dyna_flow_task_type_id:
                continue

            logging.info(
                "DynaFlowTaskTypeManager.update_bulk dyna_flow_task_type_id:%s",
                dyna_flow_task_type_id)

            dyna_flow_task_type = await self.get_by_id(
                dyna_flow_task_type_id)

            if not dyna_flow_task_type:
                raise DynaFlowTaskTypeNotFoundError(
                    f"DynaFlowTaskType with ID {dyna_flow_task_type_id} not found!")

            for key, value in update.items():
                if key != "dyna_flow_task_type_id":
                    setattr(dyna_flow_task_type, key, value)

            dyna_flow_task_type.last_update_user_id =\
                self._session_context.customer_code

            updated_dyna_flow_task_types.append(dyna_flow_task_type)

        await self._session_context.session.flush()

        logging.info(
            "DynaFlowTaskTypeManager.update_bulk end")

        return updated_dyna_flow_task_types

    async def delete_bulk(self, dyna_flow_task_type_ids: List[int]) -> bool:
        """
        Delete multiple dyna_flow_task_types
        by their IDs.
        """
        logging.info(
            "DynaFlowTaskTypeManager.delete_bulk")

        for dyna_flow_task_type_id in dyna_flow_task_type_ids:
            if not isinstance(dyna_flow_task_type_id, int):
                raise TypeError(
                    f"The dyna_flow_task_type_id must be an integer, "
                    f"got {type(dyna_flow_task_type_id)} instead."
                )

            dyna_flow_task_type = await self.get_by_id(
                dyna_flow_task_type_id)
            if not dyna_flow_task_type:
                raise DynaFlowTaskTypeNotFoundError(
                    f"DynaFlowTaskType with ID {dyna_flow_task_type_id} not found!"
                )

            if dyna_flow_task_type:
                await self._session_context.session.delete(
                    dyna_flow_task_type)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dyna_flow_task_types.
        """
        logging.info(
            "DynaFlowTaskTypeManager.count")
        result = await self._session_context.session.execute(
            select(DynaFlowTaskType))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dyna_flow_task_type: DynaFlowTaskType
    ) -> DynaFlowTaskType:
        """
        Refresh the state of a given
        dyna_flow_task_type instance
        from the database.
        """

        logging.info(
            "DynaFlowTaskTypeManager.refresh")

        await self._session_context.session.refresh(dyna_flow_task_type)

        return dyna_flow_task_type

    async def exists(self, dyna_flow_task_type_id: int) -> bool:
        """
        Check if a dyna_flow_task_type
        with the given ID exists.
        """
        logging.info(
            "DynaFlowTaskTypeManager.exists %s",
            dyna_flow_task_type_id)
        if not isinstance(dyna_flow_task_type_id, int):
            raise TypeError(
                f"The dyna_flow_task_type_id must be an integer, "
                f"got {type(dyna_flow_task_type_id)} instead."
            )
        dyna_flow_task_type = await self.get_by_id(
            dyna_flow_task_type_id)
        return bool(dyna_flow_task_type)

    def is_equal(
        self,
        dyna_flow_task_type1: DynaFlowTaskType,
        dyna_flow_task_type2: DynaFlowTaskType
    ) -> bool:
        """
        Check if two DynaFlowTaskType
        objects are equal.

        Args:
            dyna_flow_task_type1 (DynaFlowTaskType): The first
                DynaFlowTaskType object.
            dyna_flow_task_type2 (DynaFlowTaskType): The second
                DynaFlowTaskType object.

        Returns:
            bool: True if the two DynaFlowTaskType
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dyna_flow_task_type1
                or dyna_flow_task_type2
                is not provided or is not an instance of
                DynaFlowTaskType.
        """
        if not dyna_flow_task_type1:
            raise TypeError("DynaFlowTaskType1 required.")

        if not dyna_flow_task_type2:
            raise TypeError("DynaFlowTaskType2 required.")

        if not isinstance(dyna_flow_task_type1,
                          DynaFlowTaskType):
            raise TypeError("The dyna_flow_task_type1 must be an "
                            "DynaFlowTaskType instance.")

        if not isinstance(dyna_flow_task_type2,
                          DynaFlowTaskType):
            raise TypeError("The dyna_flow_task_type2 must be an "
                            "DynaFlowTaskType instance.")

        dict1 = self.to_dict(dyna_flow_task_type1)
        dict2 = self.to_dict(dyna_flow_task_type2)

        return dict1 == dict2
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[DynaFlowTaskType]:
        """
        Retrieve a list of dyna_flow_task_types by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[DynaFlowTaskType]: A list of
                dyna_flow_task_types associated
                with the specified pac ID.
        """

        logging.info(
            "DynaFlowTaskTypeManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The dyna_flow_task_type_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = DynaFlowTaskType._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
