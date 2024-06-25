# models/managers/error_log.py
# pylint: disable=unused-import

"""
This module contains the
ErrorLogManager class, which is
responsible for managing
error_logs in the system.
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
from models.error_log import ErrorLog
from models.serialization_schema.error_log import ErrorLogSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class ErrorLogNotFoundError(Exception):
    """
    Exception raised when a specified
    error_log is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="ErrorLog not found"):
        self.message = message
        super().__init__(self.message)


class ErrorLogManager:
    """
    The ErrorLogManager class
    is responsible for managing
    error_logs in the system.
    It provides methods for adding, updating, deleting,
    and retrieving error_logs.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        ErrorLogManager class.

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
        Initializes the ErrorLogManager.
        """
        logging.info("ErrorLogManager.Initialize")


    async def build(self, **kwargs) -> ErrorLog:
        """
        Builds a new ErrorLog
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                error_log.

        Returns:
            ErrorLog: The newly created
                ErrorLog object.
        """
        logging.info("ErrorLogManager.build")
        return ErrorLog(**kwargs)

    async def add(
        self,
        error_log: ErrorLog
    ) -> ErrorLog:
        """
        Adds a new error_log to the system.

        Args:
            error_log (ErrorLog): The
                error_log to add.

        Returns:
            ErrorLog: The added
                error_log.
        """
        logging.info("ErrorLogManager.add")
        error_log.insert_user_id = self._session_context.customer_code
        error_log.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            error_log)
        await self._session_context.session.flush()
        return error_log

    def _build_query(self):
        """
        Builds the base query for retrieving
        error_logs.

        Returns:
            The base query for retrieving
            error_logs.
        """
        logging.info("ErrorLogManager._build_query")

        query = select(
            ErrorLog,
            Pac,  # pac_id
        )
        query = query.outerjoin(  # pac_id
            Pac,
            and_(ErrorLog._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 ErrorLog._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[ErrorLog]:
        """
        Runs the query to retrieve
        error_logs from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[ErrorLog]: The list of
                error_logs that match the query.
        """
        logging.info("ErrorLogManager._run_query")
        error_log_query_all = self._build_query()

        if query_filter is not None:
            query = error_log_query_all.filter(query_filter)
        else:
            query = error_log_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            error_log = query_result_row[i]
            i = i + 1
            pac = query_result_row[i]  # pac_id
            i = i + 1
            error_log.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
            result.append(error_log)

        return result

    def _first_or_none(
        self,
        error_log_list: List['ErrorLog']
    ) -> Optional['ErrorLog']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            error_log_list (List[ErrorLog]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[ErrorLog]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            error_log_list[0]
            if error_log_list
            else None
        )

    async def get_by_id(self, error_log_id: int) -> Optional[ErrorLog]:
        """
        Retrieves a error_log by its ID.

        Args:
            error_log_id (int): The ID of the
                error_log to retrieve.

        Returns:
            Optional[ErrorLog]: The retrieved
                error_log, or None if not found.
        """
        logging.info(
            "ErrorLogManager.get_by_id start error_log_id: %s",
            str(error_log_id))
        if not isinstance(error_log_id, int):
            raise TypeError(
                "The error_log_id must be an integer, "
                f"got {type(error_log_id)} instead.")

        query_filter = (
            ErrorLog._error_log_id == error_log_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(self, code: uuid.UUID) -> Optional[ErrorLog]:
        """
        Retrieves a error_log
        by its code.

        Args:
            code (uuid.UUID): The code of the
                error_log to retrieve.

        Returns:
            Optional[ErrorLog]: The retrieved
                error_log, or None if not found.
        """
        logging.info("ErrorLogManager.get_by_code %s", code)

        query_filter = ErrorLog._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        error_log: ErrorLog, **kwargs
    ) -> Optional[ErrorLog]:
        """
        Updates a error_log with
        the specified attributes.

        Args:
            error_log (ErrorLog): The
                error_log to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[ErrorLog]: The updated
                error_log, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("ErrorLogManager.update")
        property_list = ErrorLog.property_list()
        if error_log:
            error_log.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(error_log, key, value)
            await self._session_context.session.flush()
        return error_log

    async def delete(self, error_log_id: int):
        """
        Deletes a error_log by its ID.

        Args:
            error_log_id (int): The ID of the
                error_log to delete.

        Raises:
            TypeError: If the error_log_id
                is not an integer.
            ErrorLogNotFoundError: If the
                error_log with the
                specified ID is not found.
        """
        logging.info("ErrorLogManager.delete %s", error_log_id)
        if not isinstance(error_log_id, int):
            raise TypeError(
                f"The error_log_id must be an integer, "
                f"got {type(error_log_id)} instead."
            )
        error_log = await self.get_by_id(
            error_log_id)
        if not error_log:
            raise ErrorLogNotFoundError(f"ErrorLog with ID {error_log_id} not found!")

        await self._session_context.session.delete(
            error_log)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[ErrorLog]:
        """
        Retrieves a list of all error_logs.

        Returns:
            List[ErrorLog]: The list of
                error_logs.
        """
        logging.info("ErrorLogManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            error_log: ErrorLog) -> str:
        """
        Serializes a ErrorLog object
        to a JSON string.

        Args:
            error_log (ErrorLog): The
                error_log to serialize.

        Returns:
            str: The JSON string representation of the
                error_log.
        """
        logging.info("ErrorLogManager.to_json")
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        return json.dumps(error_log_data)

    def to_dict(
        self,
        error_log: ErrorLog
    ) -> Dict[str, Any]:
        """
        Serializes a ErrorLog
        object to a dictionary.

        Args:
            error_log (ErrorLog): The
                error_log to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                error_log.
        """
        logging.info("ErrorLogManager.to_dict")
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)

        assert isinstance(error_log_data, dict)

        return error_log_data

    def from_json(self, json_str: str) -> ErrorLog:
        """
        Deserializes a JSON string into a
        ErrorLog object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            ErrorLog: The deserialized
                ErrorLog object.
        """
        logging.info("ErrorLogManager.from_json")
        schema = ErrorLogSchema()
        data = json.loads(json_str)
        error_log_dict = schema.load(data)

        #TODO: we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        new_error_log = ErrorLog(**error_log_dict)

        return new_error_log

    def from_dict(self, error_log_dict: Dict[str, Any]) -> ErrorLog:
        """
        Creates a ErrorLog
        instance from a dictionary of attributes.

        Args:
            error_log_dict (Dict[str, Any]): A dictionary
                containing error_log
                attributes.

        Returns:
            ErrorLog: A new
                ErrorLog instance
                created from the given
                dictionary.
        """
        logging.info("ErrorLogManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = ErrorLogSchema()
        error_log_dict_converted = schema.load(
            error_log_dict)

        #TODO: we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new ErrorLog instance
        # using the validated data
        new_error_log = ErrorLog(**error_log_dict_converted)
        return new_error_log

    async def add_bulk(
        self,
        error_logs: List[ErrorLog]
    ) -> List[ErrorLog]:
        """
        Adds multiple error_logs
        to the system.

        Args:
            error_logs (List[ErrorLog]): The list of
                error_logs to add.

        Returns:
            List[ErrorLog]: The added
                error_logs.
        """
        logging.info("ErrorLogManager.add_bulk")
        for error_log in error_logs:
            error_log_id = error_log.error_log_id
            code = error_log.code
            if error_log.error_log_id is not None and error_log.error_log_id > 0:
                raise ValueError(
                    "ErrorLog is already added"
                    f": {str(code)} {str(error_log_id)}"
                )
            error_log.insert_user_id = self._session_context.customer_code
            error_log.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(error_logs)
        await self._session_context.session.flush()
        return error_logs

    async def update_bulk(
        self,
        error_log_updates: List[Dict[str, Any]]
    ) -> List[ErrorLog]:
        """
        Update multiple error_logs
        with the provided updates.

        Args:
            error_log_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            error_log.

        Returns:
            List[ErrorLog]: A list of updated
                ErrorLog objects.

        Raises:
            TypeError: If the error_log_id is not an integer.
            ErrorLogNotFoundError: If a
                error_log with the
                provided error_log_id is not found.
        """

        logging.info("ErrorLogManager.update_bulk start")
        updated_error_logs = []
        for update in error_log_updates:
            error_log_id = update.get("error_log_id")
            if not isinstance(error_log_id, int):
                raise TypeError(
                    f"The error_log_id must be an integer, "
                    f"got {type(error_log_id)} instead."
                )
            if not error_log_id:
                continue

            logging.info("ErrorLogManager.update_bulk error_log_id:%s", error_log_id)

            error_log = await self.get_by_id(
                error_log_id)

            if not error_log:
                raise ErrorLogNotFoundError(
                    f"ErrorLog with ID {error_log_id} not found!")

            for key, value in update.items():
                if key != "error_log_id":
                    setattr(error_log, key, value)

            error_log.last_update_user_id = self._session_context.customer_code

            updated_error_logs.append(error_log)

        await self._session_context.session.flush()

        logging.info("ErrorLogManager.update_bulk end")

        return updated_error_logs

    async def delete_bulk(self, error_log_ids: List[int]) -> bool:
        """
        Delete multiple error_logs
        by their IDs.
        """
        logging.info("ErrorLogManager.delete_bulk")

        for error_log_id in error_log_ids:
            if not isinstance(error_log_id, int):
                raise TypeError(
                    f"The error_log_id must be an integer, "
                    f"got {type(error_log_id)} instead."
                )

            error_log = await self.get_by_id(
                error_log_id)
            if not error_log:
                raise ErrorLogNotFoundError(
                    f"ErrorLog with ID {error_log_id} not found!"
                )

            if error_log:
                await self._session_context.session.delete(
                    error_log)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        error_logs.
        """
        logging.info("ErrorLogManager.count")
        result = await self._session_context.session.execute(
            select(ErrorLog))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        error_log: ErrorLog
    ) -> ErrorLog:
        """
        Refresh the state of a given
        error_log instance
        from the database.
        """

        logging.info("ErrorLogManager.refresh")

        await self._session_context.session.refresh(error_log)

        return error_log

    async def exists(self, error_log_id: int) -> bool:
        """
        Check if a error_log
        with the given ID exists.
        """
        logging.info("ErrorLogManager.exists %s", error_log_id)
        if not isinstance(error_log_id, int):
            raise TypeError(
                f"The error_log_id must be an integer, "
                f"got {type(error_log_id)} instead."
            )
        error_log = await self.get_by_id(
            error_log_id)
        return bool(error_log)

    def is_equal(
        self,
        error_log1: ErrorLog,
        error_log2: ErrorLog
    ) -> bool:
        """
        Check if two ErrorLog
        objects are equal.

        Args:
            error_log1 (ErrorLog): The first
                ErrorLog object.
            error_log2 (ErrorLog): The second
                ErrorLog object.

        Returns:
            bool: True if the two ErrorLog
                objects are equal, False otherwise.

        Raises:
            TypeError: If either error_log1
                or error_log2
                is not provided or is not an instance of
                ErrorLog.
        """
        if not error_log1:
            raise TypeError("ErrorLog1 required.")

        if not error_log2:
            raise TypeError("ErrorLog2 required.")

        if not isinstance(error_log1, ErrorLog):
            raise TypeError("The error_log1 must be an "
                            "ErrorLog instance.")

        if not isinstance(error_log2, ErrorLog):
            raise TypeError("The error_log2 must be an "
                            "ErrorLog instance.")

        dict1 = self.to_dict(error_log1)
        dict2 = self.to_dict(error_log2)

        return dict1 == dict2
    async def get_by_pac_id(self, pac_id: int) -> List[ErrorLog]:  # PacID
        """
        Retrieve a list of error_logs by
        pac ID.

        Args:
            pac_id (int): The ID of the pac.

        Returns:
            List[ErrorLog]: A list of
                error_logs associated
                with the specified pac ID.
        """

        logging.info("ErrorLogManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The error_log_id must be an integer, "
                f"got {type(pac_id)} instead."
            )

        query_filter = ErrorLog._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results

