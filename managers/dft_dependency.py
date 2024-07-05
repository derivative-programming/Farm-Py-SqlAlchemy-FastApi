# models/managers/dft_dependency.py
# pylint: disable=unused-import

"""
This module contains the
DFTDependencyManager class, which is
responsible for managing
dft_dependencys in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.dyna_flow_task import DynaFlowTask  # DynaFlowTaskID
from models.dft_dependency import DFTDependency
from models.serialization_schema.dft_dependency import DFTDependencySchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DFTDependencyNotFoundError(Exception):
    """
    Exception raised when a specified
    dft_dependency is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DFTDependency not found"):
        self.message = message
        super().__init__(self.message)


class DFTDependencyManager:
    """
    The DFTDependencyManager class
    is responsible for managing
    dft_dependencys in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dft_dependencys.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DFTDependencyManager class.

        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.

        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context


    async def initialize(self):
        """
        Initializes the DFTDependencyManager.
        """
        logging.info(
            "DFTDependencyManager.Initialize")


    async def build(self, **kwargs) -> DFTDependency:
        """
        Builds a new DFTDependency
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dft_dependency.

        Returns:
            DFTDependency: The newly created
                DFTDependency object.
        """
        logging.info(
            "DFTDependencyManager.build")
        return DFTDependency(**kwargs)

    async def add(
        self,
        dft_dependency: DFTDependency
    ) -> DFTDependency:
        """
        Adds a new dft_dependency to the system.

        Args:
            dft_dependency (DFTDependency): The
                dft_dependency to add.

        Returns:
            DFTDependency: The added
                dft_dependency.
        """
        logging.info(
            "DFTDependencyManager.add")
        dft_dependency.insert_user_id = (
            self._session_context.customer_code)
        dft_dependency.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dft_dependency)
        await self._session_context.session.flush()
        return dft_dependency

    def _build_query(self):
        """
        Builds the base query for retrieving
        dft_dependencys.

        Returns:
            The base query for retrieving
            dft_dependencys.
        """
        logging.info(
            "DFTDependencyManager._build_query")

        query = select(
            DFTDependency,
            DynaFlowTask,  # dyna_flow_task_id
        )
        query = query.outerjoin(  # dyna_flow_task_id
            DynaFlowTask,
            and_(DFTDependency._dyna_flow_task_id == DynaFlowTask._dyna_flow_task_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DFTDependency._dyna_flow_task_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DFTDependency]:
        """
        Runs the query to retrieve
        dft_dependencys from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DFTDependency]: The list of
                dft_dependencys that match the query.
        """
        logging.info(
            "DFTDependencyManager._run_query")
        dft_dependency_query_all = self._build_query()

        if query_filter is not None:
            query = dft_dependency_query_all.filter(query_filter)
        else:
            query = dft_dependency_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            dft_dependency = query_result_row[i]
            i = i + 1
            dyna_flow_task = query_result_row[i]  # dyna_flow_task_id
            i = i + 1
            dft_dependency.dyna_flow_task_code_peek = (  # dyna_flow_task_id
                dyna_flow_task.code if dyna_flow_task else uuid.UUID(int=0))
            result.append(dft_dependency)

        return result

    def _first_or_none(
        self,
        dft_dependency_list: List['DFTDependency']
    ) -> Optional['DFTDependency']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dft_dependency_list (List[DFTDependency]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DFTDependency]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dft_dependency_list[0]
            if dft_dependency_list
            else None
        )

    async def get_by_id(
        self, dft_dependency_id: int
    ) -> Optional[DFTDependency]:
        """
        Retrieves a dft_dependency by its ID.

        Args:
            dft_dependency_id (int): The ID of the
                dft_dependency to retrieve.

        Returns:
            Optional[DFTDependency]: The retrieved
                dft_dependency, or None if not found.
        """
        logging.info(
            "DFTDependencyManager.get_by_id start dft_dependency_id: %s",
            str(dft_dependency_id))
        if not isinstance(dft_dependency_id, int):
            raise TypeError(
                "The dft_dependency_id must be an integer, "
                f"got {type(dft_dependency_id)} instead.")

        query_filter = (
            DFTDependency._dft_dependency_id == dft_dependency_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DFTDependency]:
        """
        Retrieves a dft_dependency
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dft_dependency to retrieve.

        Returns:
            Optional[DFTDependency]: The retrieved
                dft_dependency, or None if not found.
        """
        logging.info("DFTDependencyManager.get_by_code %s",
                     code)

        query_filter = DFTDependency._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dft_dependency: DFTDependency, **kwargs
    ) -> Optional[DFTDependency]:
        """
        Updates a dft_dependency with
        the specified attributes.

        Args:
            dft_dependency (DFTDependency): The
                dft_dependency to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DFTDependency]: The updated
                dft_dependency, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DFTDependencyManager.update")
        property_list = DFTDependency.property_list()
        if dft_dependency:
            dft_dependency.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dft_dependency, key, value)
            await self._session_context.session.flush()
        return dft_dependency

    async def delete(self, dft_dependency_id: int):
        """
        Deletes a dft_dependency by its ID.

        Args:
            dft_dependency_id (int): The ID of the
                dft_dependency to delete.

        Raises:
            TypeError: If the dft_dependency_id
                is not an integer.
            DFTDependencyNotFoundError: If the
                dft_dependency with the
                specified ID is not found.
        """
        logging.info(
            "DFTDependencyManager.delete %s",
            dft_dependency_id)
        if not isinstance(dft_dependency_id, int):
            raise TypeError(
                f"The dft_dependency_id must be an integer, "
                f"got {type(dft_dependency_id)} instead."
            )
        dft_dependency = await self.get_by_id(
            dft_dependency_id)
        if not dft_dependency:
            raise DFTDependencyNotFoundError(
                f"DFTDependency with ID {dft_dependency_id} not found!")

        await self._session_context.session.delete(
            dft_dependency)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DFTDependency]:
        """
        Retrieves a list of all dft_dependencys.

        Returns:
            List[DFTDependency]: The list of
                dft_dependencys.
        """
        logging.info(
            "DFTDependencyManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dft_dependency: DFTDependency) -> str:
        """
        Serializes a DFTDependency object
        to a JSON string.

        Args:
            dft_dependency (DFTDependency): The
                dft_dependency to serialize.

        Returns:
            str: The JSON string representation of the
                dft_dependency.
        """
        logging.info(
            "DFTDependencyManager.to_json")
        schema = DFTDependencySchema()
        dft_dependency_data = schema.dump(dft_dependency)
        return json.dumps(dft_dependency_data)

    def to_dict(
        self,
        dft_dependency: DFTDependency
    ) -> Dict[str, Any]:
        """
        Serializes a DFTDependency
        object to a dictionary.

        Args:
            dft_dependency (DFTDependency): The
                dft_dependency to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dft_dependency.
        """
        logging.info(
            "DFTDependencyManager.to_dict")
        schema = DFTDependencySchema()
        dft_dependency_data = schema.dump(dft_dependency)

        assert isinstance(dft_dependency_data, dict)

        return dft_dependency_data

    async def from_json(self, json_str: str) -> DFTDependency:
        """
        Deserializes a JSON string into a
        DFTDependency object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DFTDependency: The deserialized
                DFTDependency object.
        """
        logging.info(
            "DFTDependencyManager.from_json")
        schema = DFTDependencySchema()
        data = json.loads(json_str)
        dft_dependency_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_dft_dependency = DFTDependency(**dft_dependency_dict)

        # load or create
        new_dft_dependency = await self.get_by_id(
            dft_dependency_dict["dft_dependency_id"])
        if new_dft_dependency is None:
            new_dft_dependency = DFTDependency(**dft_dependency_dict)
            self._session_context.session.add(new_dft_dependency)
        else:
            for key, value in dft_dependency_dict.items():
                setattr(new_dft_dependency, key, value)

        return new_dft_dependency

    async def from_dict(
        self, dft_dependency_dict: Dict[str, Any]
    ) -> DFTDependency:
        """
        Creates a DFTDependency
        instance from a dictionary of attributes.

        Args:
            dft_dependency_dict (Dict[str, Any]): A dictionary
                containing dft_dependency
                attributes.

        Returns:
            DFTDependency: A new
                DFTDependency instance
                created from the given
                dictionary.
        """
        logging.info(
            "DFTDependencyManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DFTDependencySchema()
        dft_dependency_dict_converted = schema.load(
            dft_dependency_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new DFTDependency instance
        # using the validated data
        # new_dft_dependency = DFTDependency(**dft_dependency_dict_converted)

        # load or create
        new_dft_dependency = await self.get_by_id(
            dft_dependency_dict_converted["dft_dependency_id"])
        if new_dft_dependency is None:
            new_dft_dependency = DFTDependency(**dft_dependency_dict_converted)
            self._session_context.session.add(new_dft_dependency)
        else:
            for key, value in dft_dependency_dict_converted.items():
                setattr(new_dft_dependency, key, value)

        return new_dft_dependency

    async def add_bulk(
        self,
        dft_dependencys: List[DFTDependency]
    ) -> List[DFTDependency]:
        """
        Adds multiple dft_dependencys
        to the system.

        Args:
            dft_dependencys (List[DFTDependency]): The list of
                dft_dependencys to add.

        Returns:
            List[DFTDependency]: The added
                dft_dependencys.
        """
        logging.info(
            "DFTDependencyManager.add_bulk")
        for list_item in dft_dependencys:
            dft_dependency_id = \
                list_item.dft_dependency_id
            code = list_item.code
            if list_item.dft_dependency_id is not None and \
                    list_item.dft_dependency_id > 0:
                raise ValueError(
                    "DFTDependency is already added"
                    f": {str(code)} {str(dft_dependency_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dft_dependencys)
        await self._session_context.session.flush()
        return dft_dependencys

    async def update_bulk(
        self,
        dft_dependency_updates: List[Dict[str, Any]]
    ) -> List[DFTDependency]:
        """
        Update multiple dft_dependencys
        with the provided updates.

        Args:
            dft_dependency_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dft_dependency.

        Returns:
            List[DFTDependency]: A list of updated
                DFTDependency objects.

        Raises:
            TypeError: If the dft_dependency_id is not an integer.
            DFTDependencyNotFoundError: If a
                dft_dependency with the
                provided dft_dependency_id is not found.
        """

        logging.info(
            "DFTDependencyManager.update_bulk start")
        updated_dft_dependencys = []
        for update in dft_dependency_updates:
            dft_dependency_id = update.get("dft_dependency_id")
            if not isinstance(dft_dependency_id, int):
                raise TypeError(
                    f"The dft_dependency_id must be an integer, "
                    f"got {type(dft_dependency_id)} instead."
                )
            if not dft_dependency_id:
                continue

            logging.info(
                "DFTDependencyManager.update_bulk dft_dependency_id:%s",
                dft_dependency_id)

            dft_dependency = await self.get_by_id(
                dft_dependency_id)

            if not dft_dependency:
                raise DFTDependencyNotFoundError(
                    f"DFTDependency with ID {dft_dependency_id} not found!")

            for key, value in update.items():
                if key != "dft_dependency_id":
                    setattr(dft_dependency, key, value)

            dft_dependency.last_update_user_id =\
                self._session_context.customer_code

            updated_dft_dependencys.append(dft_dependency)

        await self._session_context.session.flush()

        logging.info(
            "DFTDependencyManager.update_bulk end")

        return updated_dft_dependencys

    async def delete_bulk(self, dft_dependency_ids: List[int]) -> bool:
        """
        Delete multiple dft_dependencys
        by their IDs.
        """
        logging.info(
            "DFTDependencyManager.delete_bulk")

        for dft_dependency_id in dft_dependency_ids:
            if not isinstance(dft_dependency_id, int):
                raise TypeError(
                    f"The dft_dependency_id must be an integer, "
                    f"got {type(dft_dependency_id)} instead."
                )

            dft_dependency = await self.get_by_id(
                dft_dependency_id)
            if not dft_dependency:
                raise DFTDependencyNotFoundError(
                    f"DFTDependency with ID {dft_dependency_id} not found!"
                )

            if dft_dependency:
                await self._session_context.session.delete(
                    dft_dependency)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dft_dependencys.
        """
        logging.info(
            "DFTDependencyManager.count")
        result = await self._session_context.session.execute(
            select(DFTDependency))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dft_dependency: DFTDependency
    ) -> DFTDependency:
        """
        Refresh the state of a given
        dft_dependency instance
        from the database.
        """

        logging.info(
            "DFTDependencyManager.refresh")

        await self._session_context.session.refresh(dft_dependency)

        return dft_dependency

    async def exists(self, dft_dependency_id: int) -> bool:
        """
        Check if a dft_dependency
        with the given ID exists.
        """
        logging.info(
            "DFTDependencyManager.exists %s",
            dft_dependency_id)
        if not isinstance(dft_dependency_id, int):
            raise TypeError(
                f"The dft_dependency_id must be an integer, "
                f"got {type(dft_dependency_id)} instead."
            )
        dft_dependency = await self.get_by_id(
            dft_dependency_id)
        return bool(dft_dependency)

    def is_equal(
        self,
        dft_dependency1: DFTDependency,
        dft_dependency2: DFTDependency
    ) -> bool:
        """
        Check if two DFTDependency
        objects are equal.

        Args:
            dft_dependency1 (DFTDependency): The first
                DFTDependency object.
            dft_dependency2 (DFTDependency): The second
                DFTDependency object.

        Returns:
            bool: True if the two DFTDependency
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dft_dependency1
                or dft_dependency2
                is not provided or is not an instance of
                DFTDependency.
        """
        if not dft_dependency1:
            raise TypeError("DFTDependency1 required.")

        if not dft_dependency2:
            raise TypeError("DFTDependency2 required.")

        if not isinstance(dft_dependency1,
                          DFTDependency):
            raise TypeError("The dft_dependency1 must be an "
                            "DFTDependency instance.")

        if not isinstance(dft_dependency2,
                          DFTDependency):
            raise TypeError("The dft_dependency2 must be an "
                            "DFTDependency instance.")

        dict1 = self.to_dict(dft_dependency1)
        dict2 = self.to_dict(dft_dependency2)

        return dict1 == dict2
    # DynaFlowTaskID
    async def get_by_dyna_flow_task_id(
            self,
            dyna_flow_task_id: int) -> List[DFTDependency]:
        """
        Retrieve a list of dft_dependencys by
        dyna_flow_task ID.

        Args:
            dyna_flow_task_id (int): The ID of the dyna_flow_task.

        Returns:
            List[DFTDependency]: A list of
                dft_dependencys associated
                with the specified dyna_flow_task ID.
        """

        logging.info(
            "DFTDependencyManager.get_by_dyna_flow_task_id")
        if not isinstance(dyna_flow_task_id, int):
            raise TypeError(
                f"The dft_dependency_id must be an integer, "
                f"got {type(dyna_flow_task_id)} instead."
            )

        query_filter = DFTDependency._dyna_flow_task_id == dyna_flow_task_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
