# models/managers/dyna_flow_task.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskManager class, which is
responsible for managing
dyna_flow_tasks in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.dyna_flow import DynaFlow  # DynaFlowID
from models.dyna_flow_task_type import DynaFlowTaskType  # DynaFlowTaskTypeID
from models.dyna_flow_task import DynaFlowTask
from models.serialization_schema.dyna_flow_task import DynaFlowTaskSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DynaFlowTaskNotFoundError(Exception):
    """
    Exception raised when a specified
    dyna_flow_task is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DynaFlowTask not found"):
        self.message = message
        super().__init__(self.message)


class DynaFlowTaskManager:
    """
    The DynaFlowTaskManager class
    is responsible for managing
    dyna_flow_tasks in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dyna_flow_tasks.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DynaFlowTaskManager class.

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
        Initializes the DynaFlowTaskManager.
        """
        logging.info(
            "DynaFlowTaskManager.Initialize")


    async def build(self, **kwargs) -> DynaFlowTask:
        """
        Builds a new DynaFlowTask
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dyna_flow_task.

        Returns:
            DynaFlowTask: The newly created
                DynaFlowTask object.
        """
        logging.info(
            "DynaFlowTaskManager.build")
        return DynaFlowTask(**kwargs)

    async def add(
        self,
        dyna_flow_task: DynaFlowTask
    ) -> DynaFlowTask:
        """
        Adds a new dyna_flow_task to the system.

        Args:
            dyna_flow_task (DynaFlowTask): The
                dyna_flow_task to add.

        Returns:
            DynaFlowTask: The added
                dyna_flow_task.
        """
        logging.info(
            "DynaFlowTaskManager.add")
        dyna_flow_task.insert_user_id = (
            self._session_context.customer_code)
        dyna_flow_task.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dyna_flow_task)
        await self._session_context.session.flush()
        return dyna_flow_task

    def _build_query(self):
        """
        Builds the base query for retrieving
        dyna_flow_tasks.

        Returns:
            The base query for retrieving
            dyna_flow_tasks.
        """
        logging.info(
            "DynaFlowTaskManager._build_query")

        query = select(
            DynaFlowTask,
            DynaFlow,  # dyna_flow_id
            DynaFlowTaskType,  # dyna_flow_task_type_id
        )
        query = query.outerjoin(  # dyna_flow_id
            DynaFlow,
            and_(DynaFlowTask._dyna_flow_id == DynaFlow._dyna_flow_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowTask._dyna_flow_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # dyna_flow_task_type_id
            DynaFlowTaskType,
            and_(DynaFlowTask._dyna_flow_task_type_id == DynaFlowTaskType._dyna_flow_task_type_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowTask._dyna_flow_task_type_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DynaFlowTask]:
        """
        Runs the query to retrieve
        dyna_flow_tasks from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DynaFlowTask]: The list of
                dyna_flow_tasks that match the query.
        """
        logging.info(
            "DynaFlowTaskManager._run_query")
        dyna_flow_task_query_all = self._build_query()

        if query_filter is not None:
            query = dyna_flow_task_query_all.filter(query_filter)
        else:
            query = dyna_flow_task_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            dyna_flow_task = query_result_row[i]
            i = i + 1
            dyna_flow = query_result_row[i]  # dyna_flow_id
            i = i + 1
            dyna_flow_task_type = query_result_row[i]  # dyna_flow_task_type_id
            i = i + 1
            dyna_flow_task.dyna_flow_code_peek = (  # dyna_flow_id
                dyna_flow.code if dyna_flow else uuid.UUID(int=0))
            dyna_flow_task.dyna_flow_task_type_code_peek = (  # dyna_flow_task_type_id
                dyna_flow_task_type.code if dyna_flow_task_type else uuid.UUID(int=0))
            result.append(dyna_flow_task)

        return result

    def _first_or_none(
        self,
        dyna_flow_task_list: List['DynaFlowTask']
    ) -> Optional['DynaFlowTask']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dyna_flow_task_list (List[DynaFlowTask]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DynaFlowTask]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dyna_flow_task_list[0]
            if dyna_flow_task_list
            else None
        )

    async def get_by_id(
        self, dyna_flow_task_id: int
    ) -> Optional[DynaFlowTask]:
        """
        Retrieves a dyna_flow_task by its ID.

        Args:
            dyna_flow_task_id (int): The ID of the
                dyna_flow_task to retrieve.

        Returns:
            Optional[DynaFlowTask]: The retrieved
                dyna_flow_task, or None if not found.
        """
        logging.info(
            "DynaFlowTaskManager.get_by_id start dyna_flow_task_id: %s",
            str(dyna_flow_task_id))
        if not isinstance(dyna_flow_task_id, int):
            raise TypeError(
                "The dyna_flow_task_id must be an integer, "
                f"got {type(dyna_flow_task_id)} instead.")

        query_filter = (
            DynaFlowTask._dyna_flow_task_id == dyna_flow_task_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DynaFlowTask]:
        """
        Retrieves a dyna_flow_task
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dyna_flow_task to retrieve.

        Returns:
            Optional[DynaFlowTask]: The retrieved
                dyna_flow_task, or None if not found.
        """
        logging.info("DynaFlowTaskManager.get_by_code %s",
                     code)

        query_filter = DynaFlowTask._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dyna_flow_task: DynaFlowTask, **kwargs
    ) -> Optional[DynaFlowTask]:
        """
        Updates a dyna_flow_task with
        the specified attributes.

        Args:
            dyna_flow_task (DynaFlowTask): The
                dyna_flow_task to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DynaFlowTask]: The updated
                dyna_flow_task, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DynaFlowTaskManager.update")
        property_list = DynaFlowTask.property_list()
        if dyna_flow_task:
            dyna_flow_task.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dyna_flow_task, key, value)
            await self._session_context.session.flush()
        return dyna_flow_task

    async def delete(self, dyna_flow_task_id: int):
        """
        Deletes a dyna_flow_task by its ID.

        Args:
            dyna_flow_task_id (int): The ID of the
                dyna_flow_task to delete.

        Raises:
            TypeError: If the dyna_flow_task_id
                is not an integer.
            DynaFlowTaskNotFoundError: If the
                dyna_flow_task with the
                specified ID is not found.
        """
        logging.info(
            "DynaFlowTaskManager.delete %s",
            dyna_flow_task_id)
        if not isinstance(dyna_flow_task_id, int):
            raise TypeError(
                f"The dyna_flow_task_id must be an integer, "
                f"got {type(dyna_flow_task_id)} instead."
            )
        dyna_flow_task = await self.get_by_id(
            dyna_flow_task_id)
        if not dyna_flow_task:
            raise DynaFlowTaskNotFoundError(
                f"DynaFlowTask with ID {dyna_flow_task_id} not found!")

        await self._session_context.session.delete(
            dyna_flow_task)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DynaFlowTask]:
        """
        Retrieves a list of all dyna_flow_tasks.

        Returns:
            List[DynaFlowTask]: The list of
                dyna_flow_tasks.
        """
        logging.info(
            "DynaFlowTaskManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dyna_flow_task: DynaFlowTask) -> str:
        """
        Serializes a DynaFlowTask object
        to a JSON string.

        Args:
            dyna_flow_task (DynaFlowTask): The
                dyna_flow_task to serialize.

        Returns:
            str: The JSON string representation of the
                dyna_flow_task.
        """
        logging.info(
            "DynaFlowTaskManager.to_json")
        schema = DynaFlowTaskSchema()
        dyna_flow_task_data = schema.dump(dyna_flow_task)
        return json.dumps(dyna_flow_task_data)

    def to_dict(
        self,
        dyna_flow_task: DynaFlowTask
    ) -> Dict[str, Any]:
        """
        Serializes a DynaFlowTask
        object to a dictionary.

        Args:
            dyna_flow_task (DynaFlowTask): The
                dyna_flow_task to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dyna_flow_task.
        """
        logging.info(
            "DynaFlowTaskManager.to_dict")
        schema = DynaFlowTaskSchema()
        dyna_flow_task_data = schema.dump(dyna_flow_task)

        assert isinstance(dyna_flow_task_data, dict)

        return dyna_flow_task_data

    async def from_json(self, json_str: str) -> DynaFlowTask:
        """
        Deserializes a JSON string into a
        DynaFlowTask object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DynaFlowTask: The deserialized
                DynaFlowTask object.
        """
        logging.info(
            "DynaFlowTaskManager.from_json")
        schema = DynaFlowTaskSchema()
        data = json.loads(json_str)
        dyna_flow_task_dict = schema.load(data)

        # we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # load or create
        new_dyna_flow_task = await self.get_by_id(
            dyna_flow_task_dict["dyna_flow_task_id"])
        if new_dyna_flow_task is None:
            new_dyna_flow_task = DynaFlowTask(**dyna_flow_task_dict)
            self._session_context.session.add(new_dyna_flow_task)
        else:
            for key, value in dyna_flow_task_dict.items():
                setattr(new_dyna_flow_task, key, value)

        return new_dyna_flow_task

    async def from_dict(
        self, dyna_flow_task_dict: Dict[str, Any]
    ) -> DynaFlowTask:
        """
        Creates a DynaFlowTask
        instance from a dictionary of attributes.

        Args:
            dyna_flow_task_dict (Dict[str, Any]): A dictionary
                containing dyna_flow_task
                attributes.

        Returns:
            DynaFlowTask: A new
                DynaFlowTask instance
                created from the given
                dictionary.
        """
        logging.info(
            "DynaFlowTaskManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DynaFlowTaskSchema()
        dyna_flow_task_dict_converted = schema.load(
            dyna_flow_task_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new DynaFlowTask instance
        # using the validated data
        # new_dyna_flow_task = DynaFlowTask(**dyna_flow_task_dict_converted)

        # load or create
        new_dyna_flow_task = await self.get_by_id(
            dyna_flow_task_dict_converted["dyna_flow_task_id"])
        if new_dyna_flow_task is None:
            new_dyna_flow_task = DynaFlowTask(**dyna_flow_task_dict_converted)
            self._session_context.session.add(new_dyna_flow_task)
        else:
            for key, value in dyna_flow_task_dict_converted.items():
                setattr(new_dyna_flow_task, key, value)

        return new_dyna_flow_task

    async def add_bulk(
        self,
        dyna_flow_tasks: List[DynaFlowTask]
    ) -> List[DynaFlowTask]:
        """
        Adds multiple dyna_flow_tasks
        to the system.

        Args:
            dyna_flow_tasks (List[DynaFlowTask]): The list of
                dyna_flow_tasks to add.

        Returns:
            List[DynaFlowTask]: The added
                dyna_flow_tasks.
        """
        logging.info(
            "DynaFlowTaskManager.add_bulk")
        for list_item in dyna_flow_tasks:
            dyna_flow_task_id = \
                list_item.dyna_flow_task_id
            code = list_item.code
            if list_item.dyna_flow_task_id is not None and \
                    list_item.dyna_flow_task_id > 0:
                raise ValueError(
                    "DynaFlowTask is already added"
                    f": {str(code)} {str(dyna_flow_task_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dyna_flow_tasks)
        await self._session_context.session.flush()
        return dyna_flow_tasks

    async def update_bulk(
        self,
        dyna_flow_task_updates: List[Dict[str, Any]]
    ) -> List[DynaFlowTask]:
        """
        Update multiple dyna_flow_tasks
        with the provided updates.

        Args:
            dyna_flow_task_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dyna_flow_task.

        Returns:
            List[DynaFlowTask]: A list of updated
                DynaFlowTask objects.

        Raises:
            TypeError: If the dyna_flow_task_id is not an integer.
            DynaFlowTaskNotFoundError: If a
                dyna_flow_task with the
                provided dyna_flow_task_id is not found.
        """

        logging.info(
            "DynaFlowTaskManager.update_bulk start")
        updated_dyna_flow_tasks = []
        for update in dyna_flow_task_updates:
            dyna_flow_task_id = update.get("dyna_flow_task_id")
            if not isinstance(dyna_flow_task_id, int):
                raise TypeError(
                    f"The dyna_flow_task_id must be an integer, "
                    f"got {type(dyna_flow_task_id)} instead."
                )
            if not dyna_flow_task_id:
                continue

            logging.info(
                "DynaFlowTaskManager.update_bulk dyna_flow_task_id:%s",
                dyna_flow_task_id)

            dyna_flow_task = await self.get_by_id(
                dyna_flow_task_id)

            if not dyna_flow_task:
                raise DynaFlowTaskNotFoundError(
                    f"DynaFlowTask with ID {dyna_flow_task_id} not found!")

            for key, value in update.items():
                if key != "dyna_flow_task_id":
                    setattr(dyna_flow_task, key, value)

            dyna_flow_task.last_update_user_id =\
                self._session_context.customer_code

            updated_dyna_flow_tasks.append(dyna_flow_task)

        await self._session_context.session.flush()

        logging.info(
            "DynaFlowTaskManager.update_bulk end")

        return updated_dyna_flow_tasks

    async def delete_bulk(self, dyna_flow_task_ids: List[int]) -> bool:
        """
        Delete multiple dyna_flow_tasks
        by their IDs.
        """
        logging.info(
            "DynaFlowTaskManager.delete_bulk")

        for dyna_flow_task_id in dyna_flow_task_ids:
            if not isinstance(dyna_flow_task_id, int):
                raise TypeError(
                    f"The dyna_flow_task_id must be an integer, "
                    f"got {type(dyna_flow_task_id)} instead."
                )

            dyna_flow_task = await self.get_by_id(
                dyna_flow_task_id)
            if not dyna_flow_task:
                raise DynaFlowTaskNotFoundError(
                    f"DynaFlowTask with ID {dyna_flow_task_id} not found!"
                )

            if dyna_flow_task:
                await self._session_context.session.delete(
                    dyna_flow_task)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dyna_flow_tasks.
        """
        logging.info(
            "DynaFlowTaskManager.count")
        result = await self._session_context.session.execute(
            select(DynaFlowTask))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dyna_flow_task: DynaFlowTask
    ) -> DynaFlowTask:
        """
        Refresh the state of a given
        dyna_flow_task instance
        from the database.
        """

        logging.info(
            "DynaFlowTaskManager.refresh")

        await self._session_context.session.refresh(dyna_flow_task)

        return dyna_flow_task

    async def exists(self, dyna_flow_task_id: int) -> bool:
        """
        Check if a dyna_flow_task
        with the given ID exists.
        """
        logging.info(
            "DynaFlowTaskManager.exists %s",
            dyna_flow_task_id)
        if not isinstance(dyna_flow_task_id, int):
            raise TypeError(
                f"The dyna_flow_task_id must be an integer, "
                f"got {type(dyna_flow_task_id)} instead."
            )
        dyna_flow_task = await self.get_by_id(
            dyna_flow_task_id)
        return bool(dyna_flow_task)

    def is_equal(
        self,
        dyna_flow_task1: DynaFlowTask,
        dyna_flow_task2: DynaFlowTask
    ) -> bool:
        """
        Check if two DynaFlowTask
        objects are equal.

        Args:
            dyna_flow_task1 (DynaFlowTask): The first
                DynaFlowTask object.
            dyna_flow_task2 (DynaFlowTask): The second
                DynaFlowTask object.

        Returns:
            bool: True if the two DynaFlowTask
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dyna_flow_task1
                or dyna_flow_task2
                is not provided or is not an instance of
                DynaFlowTask.
        """
        if not dyna_flow_task1:
            raise TypeError("DynaFlowTask1 required.")

        if not dyna_flow_task2:
            raise TypeError("DynaFlowTask2 required.")

        if not isinstance(dyna_flow_task1,
                          DynaFlowTask):
            raise TypeError("The dyna_flow_task1 must be an "
                            "DynaFlowTask instance.")

        if not isinstance(dyna_flow_task2,
                          DynaFlowTask):
            raise TypeError("The dyna_flow_task2 must be an "
                            "DynaFlowTask instance.")

        dict1 = self.to_dict(dyna_flow_task1)
        dict2 = self.to_dict(dyna_flow_task2)

        return dict1 == dict2
    # DynaFlowID
    # DynaFlowTaskTypeID

    async def get_by_dyna_flow_task_type_id(
            self,
            dyna_flow_task_type_id: int) -> List[DynaFlowTask]:
        """
        Retrieve a list of dyna_flow_tasks
            based on the
            given dyna_flow_task_type_id.

        Args:
            dyna_flow_task_type_id (int): The
                dyna_flow_task_type_id
                to filter the
                dyna_flow_tasks.

        Returns:
            List[DynaFlowTask]: A list of DynaFlowTask
                objects
                matching the given
                dyna_flow_task_type_id.
        """

        logging.info(
            "DynaFlowTaskManager.get_by_dyna_flow_task_type_id")
        if not isinstance(dyna_flow_task_type_id, int):
            raise TypeError(
                f"The dyna_flow_task_id must be an integer, "
                f"got {type(dyna_flow_task_type_id)} instead."
            )

        query_filter = DynaFlowTask._dyna_flow_task_type_id == dyna_flow_task_type_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    async def get_by_dyna_flow_id(
            self,
            dyna_flow_id: int) -> List[DynaFlowTask]:
        """
        Retrieve a list of dyna_flow_tasks by
        dyna_flow ID.

        Args:
            dyna_flow_id (int): The ID of the dyna_flow.

        Returns:
            List[DynaFlowTask]: A list of
                dyna_flow_tasks associated
                with the specified dyna_flow ID.
        """

        logging.info(
            "DynaFlowTaskManager.get_by_dyna_flow_id")
        if not isinstance(dyna_flow_id, int):
            raise TypeError(
                f"The dyna_flow_task_id must be an integer, "
                f"got {type(dyna_flow_id)} instead."
            )

        query_filter = DynaFlowTask._dyna_flow_id == dyna_flow_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
