# models/managers/dyna_flow.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
# pylint: disable=protected-access
"""
This module contains the
DynaFlowManager class, which is
responsible for managing
dyna_flows in the system.
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
from models.dyna_flow import DynaFlow
from models.serialization_schema.dyna_flow import \
    DynaFlowSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class DynaFlowNotFoundError(Exception):
    """
    Exception raised when a specified
    dyna_flow is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="DynaFlow not found"):
        self.message = message
        super().__init__(self.message)


class DynaFlowManager:
    """
    The DynaFlowManager class
    is responsible for managing
    dyna_flows in the system.
    It provides methods for adding, updating, deleting,
    and retrieving dyna_flows.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        DynaFlowManager class.

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
        Initializes the DynaFlowManager.
        """
        logging.info(
            "DynaFlowManager.Initialize")


    async def build(self, **kwargs) -> DynaFlow:
        """
        Builds a new DynaFlow
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                dyna_flow.

        Returns:
            DynaFlow: The newly created
                DynaFlow object.
        """
        logging.info(
            "DynaFlowManager.build")
        return DynaFlow(**kwargs)

    async def add(
        self,
        dyna_flow: DynaFlow
    ) -> DynaFlow:
        """
        Adds a new dyna_flow to the system.

        Args:
            dyna_flow (DynaFlow): The
                dyna_flow to add.

        Returns:
            DynaFlow: The added
                dyna_flow.
        """
        logging.info(
            "DynaFlowManager.add")
        dyna_flow.insert_user_id = (
            self._session_context.customer_code)
        dyna_flow.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            dyna_flow)
        await self._session_context.session.flush()
        return dyna_flow

    def _build_query(self):
        """
        Builds the base query for retrieving
        dyna_flows.

        Returns:
            The base query for retrieving
            dyna_flows.
        """
        logging.info(
            "DynaFlowManager._build_query")

        query = select(
            DynaFlow,
            DynaFlowType,  # dyna_flow_type_id
            Pac,  # pac_id
        )
        query = query.outerjoin(  # dyna_flow_type_id
            DynaFlowType,
            and_(DynaFlow._dyna_flow_type_id == DynaFlowType._dyna_flow_type_id,  # type: ignore
                 DynaFlow._dyna_flow_type_id != 0)  # type: ignore
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(DynaFlow._pac_id == Pac._pac_id,  # type: ignore
                 DynaFlow._pac_id != 0)  # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DynaFlow]:
        """
        Runs the query to retrieve
        dyna_flows from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[DynaFlow]: The list of
                dyna_flows that match the query.
        """
        logging.info(
            "DynaFlowManager._run_query")
        dyna_flow_query_all = self._build_query()

        if query_filter is not None:
            query = dyna_flow_query_all.filter(query_filter)
        else:
            query = dyna_flow_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = []

        for query_result_row in query_results:
            i = 0
            dyna_flow = query_result_row[i]
            i = i + 1
            dyna_flow_type = query_result_row[i]  # dyna_flow_type_id
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            dyna_flow.dyna_flow_type_code_peek = (  # dyna_flow_type_id
                dyna_flow_type.code if dyna_flow_type else uuid.UUID(int=0))
            dyna_flow.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(dyna_flow)

        return result

    def _first_or_none(
        self,
        dyna_flow_list: List['DynaFlow']
    ) -> Optional['DynaFlow']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            dyna_flow_list (List[DynaFlow]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[DynaFlow]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            dyna_flow_list[0]
            if dyna_flow_list
            else None
        )

    async def get_by_id(
        self, dyna_flow_id: int
    ) -> Optional[DynaFlow]:
        """
        Retrieves a dyna_flow by its ID.

        Args:
            dyna_flow_id (int): The ID of the
                dyna_flow to retrieve.

        Returns:
            Optional[DynaFlow]: The retrieved
                dyna_flow, or None if not found.
        """
        logging.info(
            "DynaFlowManager.get_by_id "
            "start dyna_flow_id: %s",
            str(dyna_flow_id))
        if not isinstance(dyna_flow_id, int):
            raise TypeError(
                "The dyna_flow_id must be an integer, "
                f"got {type(dyna_flow_id)} instead.")

        query_filter = (
            DynaFlow._dyna_flow_id == dyna_flow_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[DynaFlow]:
        """
        Retrieves a dyna_flow
        by its code.

        Args:
            code (uuid.UUID): The code of the
                dyna_flow to retrieve.

        Returns:
            Optional[DynaFlow]: The retrieved
                dyna_flow, or None if not found.
        """
        logging.info("DynaFlowManager.get_by_code %s",
                     code)

        query_filter = DynaFlow._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        dyna_flow: DynaFlow, **kwargs
    ) -> Optional[DynaFlow]:
        """
        Updates a dyna_flow with
        the specified attributes.

        Args:
            dyna_flow (DynaFlow): The
                dyna_flow to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[DynaFlow]: The updated
                dyna_flow, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("DynaFlowManager.update")
        property_list = DynaFlow.property_list()
        if dyna_flow:
            dyna_flow.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(dyna_flow, key, value)
            await self._session_context.session.flush()
        return dyna_flow

    async def delete(self, dyna_flow_id: int):
        """
        Deletes a dyna_flow by its ID.

        Args:
            dyna_flow_id (int): The ID of the
                dyna_flow to delete.

        Raises:
            TypeError: If the dyna_flow_id
                is not an integer.
            DynaFlowNotFoundError: If the
                dyna_flow with the
                specified ID is not found.
        """
        logging.info(
            "DynaFlowManager.delete %s",
            dyna_flow_id)
        if not isinstance(dyna_flow_id, int):
            raise TypeError(
                f"The dyna_flow_id must be an integer, "
                f"got {type(dyna_flow_id)} instead."
            )
        dyna_flow = await self.get_by_id(
            dyna_flow_id)
        if not dyna_flow:
            raise DynaFlowNotFoundError(
                f"DynaFlow with ID "
                f"{dyna_flow_id} not found!")

        await self._session_context.session.delete(
            dyna_flow)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[DynaFlow]:
        """
        Retrieves a list of all dyna_flows.

        Returns:
            List[DynaFlow]: The list of
                dyna_flows.
        """
        logging.info(
            "DynaFlowManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            dyna_flow: DynaFlow) -> str:
        """
        Serializes a DynaFlow object
        to a JSON string.

        Args:
            dyna_flow (DynaFlow): The
                dyna_flow to serialize.

        Returns:
            str: The JSON string representation of the
                dyna_flow.
        """
        logging.info(
            "DynaFlowManager.to_json")
        schema = DynaFlowSchema()
        dyna_flow_data = schema.dump(dyna_flow)
        return json.dumps(dyna_flow_data)

    def to_dict(
        self,
        dyna_flow: DynaFlow
    ) -> Dict[str, Any]:
        """
        Serializes a DynaFlow
        object to a dictionary.

        Args:
            dyna_flow (DynaFlow): The
                dyna_flow to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                dyna_flow.
        """
        logging.info(
            "DynaFlowManager.to_dict")
        schema = DynaFlowSchema()
        dyna_flow_data = schema.dump(dyna_flow)

        assert isinstance(dyna_flow_data, dict)

        return dyna_flow_data

    async def from_json(self, json_str: str) -> DynaFlow:
        """
        Deserializes a JSON string into a
        DynaFlow object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            DynaFlow: The deserialized
                DynaFlow object.
        """
        logging.info(
            "DynaFlowManager.from_json")
        schema = DynaFlowSchema()
        data = json.loads(json_str)
        dyna_flow_dict = schema.load(data)

        # we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # load or create
        new_dyna_flow = await self.get_by_id(
            dyna_flow_dict["dyna_flow_id"])
        if new_dyna_flow is None:
            new_dyna_flow = DynaFlow(
                **dyna_flow_dict)
            self._session_context.session.add(new_dyna_flow)
        else:
            for key, value in dyna_flow_dict.items():
                setattr(new_dyna_flow, key, value)

        return new_dyna_flow

    async def from_dict(
        self, dyna_flow_dict: Dict[str, Any]
    ) -> DynaFlow:
        """
        Creates a DynaFlow
        instance from a dictionary of attributes.

        Args:
            dyna_flow_dict (Dict[str, Any]): A dictionary
                containing dyna_flow
                attributes.

        Returns:
            DynaFlow: A new
                DynaFlow instance
                created from the given
                dictionary.
        """
        logging.info(
            "DynaFlowManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = DynaFlowSchema()
        dyna_flow_dict_converted = schema.load(
            dyna_flow_dict)

        # load or create
        new_dyna_flow = await self.get_by_id(
            dyna_flow_dict_converted["dyna_flow_id"])
        if new_dyna_flow is None:
            new_dyna_flow = DynaFlow(
                **dyna_flow_dict_converted)
            self._session_context.session.add(new_dyna_flow)
        else:
            for key, value in dyna_flow_dict_converted.items():
                setattr(new_dyna_flow, key, value)

        return new_dyna_flow

    async def add_bulk(
        self,
        dyna_flows: List[DynaFlow]
    ) -> List[DynaFlow]:
        """
        Adds multiple dyna_flows
        to the system.

        Args:
            dyna_flows (List[DynaFlow]): The list of
                dyna_flows to add.

        Returns:
            List[DynaFlow]: The added
                dyna_flows.
        """
        logging.info(
            "DynaFlowManager.add_bulk")
        for list_item in dyna_flows:
            dyna_flow_id = \
                list_item.dyna_flow_id
            code = list_item.code
            if list_item.dyna_flow_id is not None and \
                    list_item.dyna_flow_id > 0:
                raise ValueError(
                    "DynaFlow is already added"
                    f": {str(code)} {str(dyna_flow_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(dyna_flows)
        await self._session_context.session.flush()
        return dyna_flows

    async def update_bulk(
        self,
        dyna_flow_updates: List[Dict[str, Any]]
    ) -> List[DynaFlow]:
        """
        Update multiple dyna_flows
        with the provided updates.

        Args:
            dyna_flow_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            dyna_flow.

        Returns:
            List[DynaFlow]: A list of updated
                DynaFlow objects.

        Raises:
            TypeError: If the dyna_flow_id is not an integer.
            DynaFlowNotFoundError: If a
                dyna_flow with the
                provided dyna_flow_id is not found.
        """

        logging.info(
            "DynaFlowManager.update_bulk start")
        updated_dyna_flows = []
        for update in dyna_flow_updates:
            dyna_flow_id = update.get(
                "dyna_flow_id")
            if not isinstance(dyna_flow_id, int):
                raise TypeError(
                    f"The dyna_flow_id must be an integer, "
                    f"got {type(dyna_flow_id)} instead."
                )
            if not dyna_flow_id:
                continue

            logging.info(
                "DynaFlowManager.update_bulk "
                "dyna_flow_id:%s",
                dyna_flow_id)

            dyna_flow = await self.get_by_id(
                dyna_flow_id)

            if not dyna_flow:
                raise DynaFlowNotFoundError(
                    f"DynaFlow with ID "
                    f"{dyna_flow_id} not found!")

            for key, value in update.items():
                if key != "dyna_flow_id":
                    setattr(dyna_flow, key, value)

            dyna_flow.last_update_user_id =\
                self._session_context.customer_code

            updated_dyna_flows.append(dyna_flow)

        await self._session_context.session.flush()

        logging.info(
            "DynaFlowManager.update_bulk end")

        return updated_dyna_flows

    async def delete_bulk(
            self, dyna_flow_ids: List[int]) -> bool:
        """
        Delete multiple dyna_flows
        by their IDs.
        """
        logging.info(
            "DynaFlowManager.delete_bulk")

        for dyna_flow_id in dyna_flow_ids:
            if not isinstance(dyna_flow_id, int):
                raise TypeError(
                    f"The dyna_flow_id must be an integer, "
                    f"got {type(dyna_flow_id)} instead."
                )

            dyna_flow = await self.get_by_id(
                dyna_flow_id)
            if not dyna_flow:
                raise DynaFlowNotFoundError(
                    f"DynaFlow with ID "
                    f"{dyna_flow_id} not found!"
                )

            if dyna_flow:
                await self._session_context.session.delete(
                    dyna_flow)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        dyna_flows.
        """
        logging.info(
            "DynaFlowManager.count")
        result = await self._session_context.session.execute(
            select(DynaFlow))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        dyna_flow: DynaFlow
    ) -> DynaFlow:
        """
        Refresh the state of a given
        dyna_flow instance
        from the database.
        """

        logging.info(
            "DynaFlowManager.refresh")

        await self._session_context.session.refresh(dyna_flow)

        return dyna_flow

    async def exists(self, dyna_flow_id: int) -> bool:
        """
        Check if a dyna_flow
        with the given ID exists.
        """
        logging.info(
            "DynaFlowManager.exists %s",
            dyna_flow_id)
        if not isinstance(dyna_flow_id, int):
            raise TypeError(
                f"The dyna_flow_id must be an integer, "
                f"got {type(dyna_flow_id)} instead."
            )
        dyna_flow = await self.get_by_id(
            dyna_flow_id)
        return bool(dyna_flow)

    def is_equal(
        self,
        dyna_flow1: DynaFlow,
        dyna_flow2: DynaFlow
    ) -> bool:
        """
        Check if two DynaFlow
        objects are equal.

        Args:
            dyna_flow1 (DynaFlow): The first
                DynaFlow object.
            dyna_flow2 (DynaFlow): The second
                DynaFlow object.

        Returns:
            bool: True if the two DynaFlow
                objects are equal, False otherwise.

        Raises:
            TypeError: If either dyna_flow1
                or dyna_flow2
                is not provided or is not an instance of
                DynaFlow.
        """
        if not dyna_flow1:
            raise TypeError("DynaFlow1 required.")

        if not dyna_flow2:
            raise TypeError("DynaFlow2 required.")

        if not isinstance(dyna_flow1,
                          DynaFlow):
            raise TypeError("The dyna_flow1 must be an "
                            "DynaFlow instance.")

        if not isinstance(dyna_flow2,
                          DynaFlow):
            raise TypeError("The dyna_flow2 must be an "
                            "DynaFlow instance.")

        dict1 = self.to_dict(dyna_flow1)
        dict2 = self.to_dict(dyna_flow2)

        return dict1 == dict2
    # DynaFlowTypeID

    async def get_by_dyna_flow_type_id(
            self,
            dyna_flow_type_id: int) -> List[DynaFlow]:
        """
        Retrieve a list of dyna_flows
            based on the
            given dyna_flow_type_id.

        Args:
            dyna_flow_type_id (int): The
                dyna_flow_type_id
                to filter the
                dyna_flows.

        Returns:
            List[DynaFlow]: A list of DynaFlow
                objects
                matching the given
                dyna_flow_type_id.
        """

        logging.info(
            "DynaFlowManager.get_by_dyna_flow_type_id")
        if not isinstance(dyna_flow_type_id, int):
            raise TypeError(
                f"The dyna_flow_id must be an integer, "
                f"got {type(dyna_flow_type_id)} instead."
            )

        query_filter = DynaFlow._dyna_flow_type_id == dyna_flow_type_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    # PacID
    async def get_by_pac_id(
            self,
            pac_id: int) -> List[DynaFlow]:
        """
        Retrieve a list of dyna_flows by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[DynaFlow]: A list of
                dyna_flows associated
                with the specified pac ID.
        """

        logging.info(
            "DynaFlowManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The dyna_flow_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = DynaFlow._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    async def get_by_dependency_dyna_flow_id_prop(
        self,
        dependency_dyna_flow_id
    ) -> List[DynaFlow]:
        """
        Retrieve a list of DynaFlow by
        dependency_dyna_flow_id.
        """
        logging.info(
            "DynaFlowManager"
            ".get_by_dependency_dyna_flow_id_prop")
        query_filter = (
            DynaFlow._dependency_dyna_flow_id == dependency_dyna_flow_id)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_is_completed_prop(
        self,
        is_completed
    ) -> List[DynaFlow]:
        """
        Retrieve a list of DynaFlow by
        is_completed.
        """
        logging.info(
            "DynaFlowManager"
            ".get_by_is_completed_prop")
        query_filter = (
            DynaFlow._is_completed == is_completed)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_root_dyna_flow_id_prop(
        self,
        root_dyna_flow_id
    ) -> List[DynaFlow]:
        """
        Retrieve a list of DynaFlow by
        root_dyna_flow_id.
        """
        logging.info(
            "DynaFlowManager"
            ".get_by_root_dyna_flow_id_prop")
        query_filter = (
            DynaFlow._root_dyna_flow_id == root_dyna_flow_id)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_subject_code_prop(
        self,
        subject_code
    ) -> List[DynaFlow]:
        """
        Retrieve a list of DynaFlow by
        subject_code.
        """
        logging.info(
            "DynaFlowManager"
            ".get_by_subject_code_prop")
        query_filter = (
            DynaFlow._subject_code == subject_code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
