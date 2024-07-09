# models/managers/dyna_flow_type_schedule.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeScheduleManager class, which is
responsible for managing
dyna_flow_type_schedules in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.dyna_flow_type import DynaFlowType  # DynaFlowTypeID
from models.pac import Pac  # PacID
from models.dyna_flow_type_schedule import DynaFlowTypeSchedule
from models.serialization_schema.dyna_flow_type_schedule import \
    DynaFlowTypeScheduleSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DynaFlowTypeScheduleNotFoundError(Exception):
    """
    Exception raised when a specified
    dyna_flow_type_schedule is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DynaFlowTypeSchedule not found"):
        self.message = message
        super().__init__(self.message)


class DynaFlowTypeScheduleManager:
    """
    The DynaFlowTypeScheduleManager class
    is responsible for managing
    dyna_flow_type_schedules in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dyna_flow_type_schedules.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DynaFlowTypeScheduleManager class.

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
        Initializes the DynaFlowTypeScheduleManager.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.Initialize")


    async def build(self, **kwargs) -> DynaFlowTypeSchedule:
        """
        Builds a new DynaFlowTypeSchedule
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dyna_flow_type_schedule.

        Returns:
            DynaFlowTypeSchedule: The newly created
                DynaFlowTypeSchedule object.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.build")
        return DynaFlowTypeSchedule(**kwargs)

    async def add(
        self,
        dyna_flow_type_schedule: DynaFlowTypeSchedule
    ) -> DynaFlowTypeSchedule:
        """
        Adds a new dyna_flow_type_schedule to the system.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                dyna_flow_type_schedule to add.

        Returns:
            DynaFlowTypeSchedule: The added
                dyna_flow_type_schedule.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.add")
        dyna_flow_type_schedule.insert_user_id = (
            self._session_context.customer_code)
        dyna_flow_type_schedule.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dyna_flow_type_schedule)
        await self._session_context.session.flush()
        return dyna_flow_type_schedule

    def _build_query(self):
        """
        Builds the base query for retrieving
        dyna_flow_type_schedules.

        Returns:
            The base query for retrieving
            dyna_flow_type_schedules.
        """
        logging.info(
            "DynaFlowTypeScheduleManager._build_query")

        query = select(
            DynaFlowTypeSchedule,
            DynaFlowType,  # dyna_flow_type_id
            Pac,  # pac_id
        )
        query = query.outerjoin(  # dyna_flow_type_id
            DynaFlowType,
            and_(DynaFlowTypeSchedule._dyna_flow_type_id == DynaFlowType._dyna_flow_type_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowTypeSchedule._dyna_flow_type_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DynaFlowTypeSchedule._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 DynaFlowTypeSchedule._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DynaFlowTypeSchedule]:
        """
        Runs the query to retrieve
        dyna_flow_type_schedules from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DynaFlowTypeSchedule]: The list of
                dyna_flow_type_schedules that match the query.
        """
        logging.info(
            "DynaFlowTypeScheduleManager._run_query")
        dyna_flow_type_schedule_query_all = self._build_query()

        if query_filter is not None:
            query = dyna_flow_type_schedule_query_all.filter(query_filter)
        else:
            query = dyna_flow_type_schedule_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            dyna_flow_type_schedule = query_result_row[i]
            i = i + 1
            dyna_flow_type = query_result_row[i]  # dyna_flow_type_id
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            dyna_flow_type_schedule.dyna_flow_type_code_peek = (  # dyna_flow_type_id
                dyna_flow_type.code if dyna_flow_type else uuid.UUID(int=0))
            dyna_flow_type_schedule.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(dyna_flow_type_schedule)

        return result

    def _first_or_none(
        self,
        dyna_flow_type_schedule_list: List['DynaFlowTypeSchedule']
    ) -> Optional['DynaFlowTypeSchedule']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dyna_flow_type_schedule_list (List[DynaFlowTypeSchedule]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DynaFlowTypeSchedule]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dyna_flow_type_schedule_list[0]
            if dyna_flow_type_schedule_list
            else None
        )

    async def get_by_id(
        self, dyna_flow_type_schedule_id: int
    ) -> Optional[DynaFlowTypeSchedule]:
        """
        Retrieves a dyna_flow_type_schedule by its ID.

        Args:
            dyna_flow_type_schedule_id (int): The ID of the
                dyna_flow_type_schedule to retrieve.

        Returns:
            Optional[DynaFlowTypeSchedule]: The retrieved
                dyna_flow_type_schedule, or None if not found.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.get_by_id "
            "start dyna_flow_type_schedule_id: %s",
            str(dyna_flow_type_schedule_id))
        if not isinstance(dyna_flow_type_schedule_id, int):
            raise TypeError(
                "The dyna_flow_type_schedule_id must be an integer, "
                f"got {type(dyna_flow_type_schedule_id)} instead.")

        query_filter = (
            DynaFlowTypeSchedule._dyna_flow_type_schedule_id == dyna_flow_type_schedule_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DynaFlowTypeSchedule]:
        """
        Retrieves a dyna_flow_type_schedule
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dyna_flow_type_schedule to retrieve.

        Returns:
            Optional[DynaFlowTypeSchedule]: The retrieved
                dyna_flow_type_schedule, or None if not found.
        """
        logging.info("DynaFlowTypeScheduleManager.get_by_code %s",
                     code)

        query_filter = DynaFlowTypeSchedule._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dyna_flow_type_schedule: DynaFlowTypeSchedule, **kwargs
    ) -> Optional[DynaFlowTypeSchedule]:
        """
        Updates a dyna_flow_type_schedule with
        the specified attributes.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                dyna_flow_type_schedule to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DynaFlowTypeSchedule]: The updated
                dyna_flow_type_schedule, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DynaFlowTypeScheduleManager.update")
        property_list = DynaFlowTypeSchedule.property_list()
        if dyna_flow_type_schedule:
            dyna_flow_type_schedule.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dyna_flow_type_schedule, key, value)
            await self._session_context.session.flush()
        return dyna_flow_type_schedule

    async def delete(self, dyna_flow_type_schedule_id: int):
        """
        Deletes a dyna_flow_type_schedule by its ID.

        Args:
            dyna_flow_type_schedule_id (int): The ID of the
                dyna_flow_type_schedule to delete.

        Raises:
            TypeError: If the dyna_flow_type_schedule_id
                is not an integer.
            DynaFlowTypeScheduleNotFoundError: If the
                dyna_flow_type_schedule with the
                specified ID is not found.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.delete %s",
            dyna_flow_type_schedule_id)
        if not isinstance(dyna_flow_type_schedule_id, int):
            raise TypeError(
                f"The dyna_flow_type_schedule_id must be an integer, "
                f"got {type(dyna_flow_type_schedule_id)} instead."
            )
        dyna_flow_type_schedule = await self.get_by_id(
            dyna_flow_type_schedule_id)
        if not dyna_flow_type_schedule:
            raise DynaFlowTypeScheduleNotFoundError(
                f"DynaFlowTypeSchedule with ID "
                f"{dyna_flow_type_schedule_id} not found!")

        await self._session_context.session.delete(
            dyna_flow_type_schedule)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DynaFlowTypeSchedule]:
        """
        Retrieves a list of all dyna_flow_type_schedules.

        Returns:
            List[DynaFlowTypeSchedule]: The list of
                dyna_flow_type_schedules.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dyna_flow_type_schedule: DynaFlowTypeSchedule) -> str:
        """
        Serializes a DynaFlowTypeSchedule object
        to a JSON string.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                dyna_flow_type_schedule to serialize.

        Returns:
            str: The JSON string representation of the
                dyna_flow_type_schedule.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.to_json")
        schema = DynaFlowTypeScheduleSchema()
        dyna_flow_type_schedule_data = schema.dump(dyna_flow_type_schedule)
        return json.dumps(dyna_flow_type_schedule_data)

    def to_dict(
        self,
        dyna_flow_type_schedule: DynaFlowTypeSchedule
    ) -> Dict[str, Any]:
        """
        Serializes a DynaFlowTypeSchedule
        object to a dictionary.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                dyna_flow_type_schedule to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dyna_flow_type_schedule.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.to_dict")
        schema = DynaFlowTypeScheduleSchema()
        dyna_flow_type_schedule_data = schema.dump(dyna_flow_type_schedule)

        assert isinstance(dyna_flow_type_schedule_data, dict)

        return dyna_flow_type_schedule_data

    async def from_json(self, json_str: str) -> DynaFlowTypeSchedule:
        """
        Deserializes a JSON string into a
        DynaFlowTypeSchedule object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DynaFlowTypeSchedule: The deserialized
                DynaFlowTypeSchedule object.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.from_json")
        schema = DynaFlowTypeScheduleSchema()
        data = json.loads(json_str)
        dyna_flow_type_schedule_dict = schema.load(data)

        # we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # load or create
        new_dyna_flow_type_schedule = await self.get_by_id(
            dyna_flow_type_schedule_dict["dyna_flow_type_schedule_id"])
        if new_dyna_flow_type_schedule is None:
            new_dyna_flow_type_schedule = DynaFlowTypeSchedule(
                **dyna_flow_type_schedule_dict)
            self._session_context.session.add(new_dyna_flow_type_schedule)
        else:
            for key, value in dyna_flow_type_schedule_dict.items():
                setattr(new_dyna_flow_type_schedule, key, value)

        return new_dyna_flow_type_schedule

    async def from_dict(
        self, dyna_flow_type_schedule_dict: Dict[str, Any]
    ) -> DynaFlowTypeSchedule:
        """
        Creates a DynaFlowTypeSchedule
        instance from a dictionary of attributes.

        Args:
            dyna_flow_type_schedule_dict (Dict[str, Any]): A dictionary
                containing dyna_flow_type_schedule
                attributes.

        Returns:
            DynaFlowTypeSchedule: A new
                DynaFlowTypeSchedule instance
                created from the given
                dictionary.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DynaFlowTypeScheduleSchema()
        dyna_flow_type_schedule_dict_converted = schema.load(
            dyna_flow_type_schedule_dict)

        # load or create
        new_dyna_flow_type_schedule = await self.get_by_id(
            dyna_flow_type_schedule_dict_converted["dyna_flow_type_schedule_id"])
        if new_dyna_flow_type_schedule is None:
            new_dyna_flow_type_schedule = DynaFlowTypeSchedule(
                **dyna_flow_type_schedule_dict_converted)
            self._session_context.session.add(new_dyna_flow_type_schedule)
        else:
            for key, value in dyna_flow_type_schedule_dict_converted.items():
                setattr(new_dyna_flow_type_schedule, key, value)

        return new_dyna_flow_type_schedule

    async def add_bulk(
        self,
        dyna_flow_type_schedules: List[DynaFlowTypeSchedule]
    ) -> List[DynaFlowTypeSchedule]:
        """
        Adds multiple dyna_flow_type_schedules
        to the system.

        Args:
            dyna_flow_type_schedules (List[DynaFlowTypeSchedule]): The list of
                dyna_flow_type_schedules to add.

        Returns:
            List[DynaFlowTypeSchedule]: The added
                dyna_flow_type_schedules.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.add_bulk")
        for list_item in dyna_flow_type_schedules:
            dyna_flow_type_schedule_id = \
                list_item.dyna_flow_type_schedule_id
            code = list_item.code
            if list_item.dyna_flow_type_schedule_id is not None and \
                    list_item.dyna_flow_type_schedule_id > 0:
                raise ValueError(
                    "DynaFlowTypeSchedule is already added"
                    f": {str(code)} {str(dyna_flow_type_schedule_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dyna_flow_type_schedules)
        await self._session_context.session.flush()
        return dyna_flow_type_schedules

    async def update_bulk(
        self,
        dyna_flow_type_schedule_updates: List[Dict[str, Any]]
    ) -> List[DynaFlowTypeSchedule]:
        """
        Update multiple dyna_flow_type_schedules
        with the provided updates.

        Args:
            dyna_flow_type_schedule_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dyna_flow_type_schedule.

        Returns:
            List[DynaFlowTypeSchedule]: A list of updated
                DynaFlowTypeSchedule objects.

        Raises:
            TypeError: If the dyna_flow_type_schedule_id is not an integer.
            DynaFlowTypeScheduleNotFoundError: If a
                dyna_flow_type_schedule with the
                provided dyna_flow_type_schedule_id is not found.
        """

        logging.info(
            "DynaFlowTypeScheduleManager.update_bulk start")
        updated_dyna_flow_type_schedules = []
        for update in dyna_flow_type_schedule_updates:
            dyna_flow_type_schedule_id = update.get(
                "dyna_flow_type_schedule_id")
            if not isinstance(dyna_flow_type_schedule_id, int):
                raise TypeError(
                    f"The dyna_flow_type_schedule_id must be an integer, "
                    f"got {type(dyna_flow_type_schedule_id)} instead."
                )
            if not dyna_flow_type_schedule_id:
                continue

            logging.info(
                "DynaFlowTypeScheduleManager.update_bulk "
                "dyna_flow_type_schedule_id:%s",
                dyna_flow_type_schedule_id)

            dyna_flow_type_schedule = await self.get_by_id(
                dyna_flow_type_schedule_id)

            if not dyna_flow_type_schedule:
                raise DynaFlowTypeScheduleNotFoundError(
                    f"DynaFlowTypeSchedule with ID "
                    f"{dyna_flow_type_schedule_id} not found!")

            for key, value in update.items():
                if key != "dyna_flow_type_schedule_id":
                    setattr(dyna_flow_type_schedule, key, value)

            dyna_flow_type_schedule.last_update_user_id =\
                self._session_context.customer_code

            updated_dyna_flow_type_schedules.append(dyna_flow_type_schedule)

        await self._session_context.session.flush()

        logging.info(
            "DynaFlowTypeScheduleManager.update_bulk end")

        return updated_dyna_flow_type_schedules

    async def delete_bulk(
            self, dyna_flow_type_schedule_ids: List[int]) -> bool:
        """
        Delete multiple dyna_flow_type_schedules
        by their IDs.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.delete_bulk")

        for dyna_flow_type_schedule_id in dyna_flow_type_schedule_ids:
            if not isinstance(dyna_flow_type_schedule_id, int):
                raise TypeError(
                    f"The dyna_flow_type_schedule_id must be an integer, "
                    f"got {type(dyna_flow_type_schedule_id)} instead."
                )

            dyna_flow_type_schedule = await self.get_by_id(
                dyna_flow_type_schedule_id)
            if not dyna_flow_type_schedule:
                raise DynaFlowTypeScheduleNotFoundError(
                    f"DynaFlowTypeSchedule with ID "
                    f"{dyna_flow_type_schedule_id} not found!"
                )

            if dyna_flow_type_schedule:
                await self._session_context.session.delete(
                    dyna_flow_type_schedule)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dyna_flow_type_schedules.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.count")
        result = await self._session_context.session.execute(
            select(DynaFlowTypeSchedule))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dyna_flow_type_schedule: DynaFlowTypeSchedule
    ) -> DynaFlowTypeSchedule:
        """
        Refresh the state of a given
        dyna_flow_type_schedule instance
        from the database.
        """

        logging.info(
            "DynaFlowTypeScheduleManager.refresh")

        await self._session_context.session.refresh(dyna_flow_type_schedule)

        return dyna_flow_type_schedule

    async def exists(self, dyna_flow_type_schedule_id: int) -> bool:
        """
        Check if a dyna_flow_type_schedule
        with the given ID exists.
        """
        logging.info(
            "DynaFlowTypeScheduleManager.exists %s",
            dyna_flow_type_schedule_id)
        if not isinstance(dyna_flow_type_schedule_id, int):
            raise TypeError(
                f"The dyna_flow_type_schedule_id must be an integer, "
                f"got {type(dyna_flow_type_schedule_id)} instead."
            )
        dyna_flow_type_schedule = await self.get_by_id(
            dyna_flow_type_schedule_id)
        return bool(dyna_flow_type_schedule)

    def is_equal(
        self,
        dyna_flow_type_schedule1: DynaFlowTypeSchedule,
        dyna_flow_type_schedule2: DynaFlowTypeSchedule
    ) -> bool:
        """
        Check if two DynaFlowTypeSchedule
        objects are equal.

        Args:
            dyna_flow_type_schedule1 (DynaFlowTypeSchedule): The first
                DynaFlowTypeSchedule object.
            dyna_flow_type_schedule2 (DynaFlowTypeSchedule): The second
                DynaFlowTypeSchedule object.

        Returns:
            bool: True if the two DynaFlowTypeSchedule
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dyna_flow_type_schedule1
                or dyna_flow_type_schedule2
                is not provided or is not an instance of
                DynaFlowTypeSchedule.
        """
        if not dyna_flow_type_schedule1:
            raise TypeError("DynaFlowTypeSchedule1 required.")

        if not dyna_flow_type_schedule2:
            raise TypeError("DynaFlowTypeSchedule2 required.")

        if not isinstance(dyna_flow_type_schedule1,
                          DynaFlowTypeSchedule):
            raise TypeError("The dyna_flow_type_schedule1 must be an "
                            "DynaFlowTypeSchedule instance.")

        if not isinstance(dyna_flow_type_schedule2,
                          DynaFlowTypeSchedule):
            raise TypeError("The dyna_flow_type_schedule2 must be an "
                            "DynaFlowTypeSchedule instance.")

        dict1 = self.to_dict(dyna_flow_type_schedule1)
        dict2 = self.to_dict(dyna_flow_type_schedule2)

        return dict1 == dict2
    # DynaFlowTypeID

    async def get_by_dyna_flow_type_id(
            self,
            dyna_flow_type_id: int) -> List[DynaFlowTypeSchedule]:
        """
        Retrieve a list of dyna_flow_type_schedules
            based on the
            given dyna_flow_type_id.

        Args:
            dyna_flow_type_id (int): The
                dyna_flow_type_id
                to filter the
                dyna_flow_type_schedules.

        Returns:
            List[DynaFlowTypeSchedule]: A list of DynaFlowTypeSchedule
                objects
                matching the given
                dyna_flow_type_id.
        """

        logging.info(
            "DynaFlowTypeScheduleManager.get_by_dyna_flow_type_id")
        if not isinstance(dyna_flow_type_id, int):
            raise TypeError(
                f"The dyna_flow_type_schedule_id must be an integer, "
                f"got {type(dyna_flow_type_id)} instead."
            )

        query_filter = DynaFlowTypeSchedule._dyna_flow_type_id == dyna_flow_type_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[DynaFlowTypeSchedule]:
        """
        Retrieve a list of dyna_flow_type_schedules by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[DynaFlowTypeSchedule]: A list of
                dyna_flow_type_schedules associated
                with the specified pac ID.
        """

        logging.info(
            "DynaFlowTypeScheduleManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The dyna_flow_type_schedule_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = DynaFlowTypeSchedule._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
