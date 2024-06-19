# models/managers/error_log.py
# pylint: disable=unused-import
"""
    #TODO add comment
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
    Exception raised when a specified error_log is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="ErrorLog not found"):
        self.message = message
        super().__init__(self.message)

class ErrorLogManager:
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
            #TODO add comment
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        # Conditionally set the UUID column type
        return value

    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.Initialize")

    async def build(self, **kwargs) -> ErrorLog:
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.build")
        return ErrorLog(**kwargs)
    async def add(self, error_log: ErrorLog) -> ErrorLog:
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.add")
        error_log.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        error_log.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(error_log)
        await self._session_context.session.flush()
        return error_log
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager._build_query")
        query = select(
            ErrorLog,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(ErrorLog._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 ErrorLog._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[ErrorLog]:
        """
            #TODO add comment
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
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            error_log.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(error_log)
        return result
    def _first_or_none(
        self,
        error_log_list: List['ErrorLog']
    ) -> Optional['ErrorLog']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            error_log_list (List[ErrorLog]):
                The list to retrieve the first element from.
        Returns:
            Optional[ErrorLog]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            error_log_list[0]
            if error_log_list
            else None
        )
    async def get_by_id(self, error_log_id: int) -> Optional[ErrorLog]:
        """
            #TODO add comment
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
            #TODO add comment
        """
        logging.info("ErrorLogManager.get_by_code %s", code)
        query_filter = ErrorLog._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, error_log: ErrorLog, **kwargs) -> Optional[ErrorLog]:
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.update")
        property_list = ErrorLog.property_list()
        if error_log:
            error_log.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(error_log, key, value)
            await self._session_context.session.flush()
        return error_log
    async def delete(self, error_log_id: int):
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.delete %s", error_log_id)
        if not isinstance(error_log_id, int):
            raise TypeError(
                f"The error_log_id must be an integer, "
                f"got {type(error_log_id)} instead."
            )
        error_log = await self.get_by_id(error_log_id)
        if not error_log:
            raise ErrorLogNotFoundError(f"ErrorLog with ID {error_log_id} not found!")
        await self._session_context.session.delete(error_log)
        await self._session_context.session.flush()
    async def get_list(self) -> List[ErrorLog]:
        """
            #TODO add comment
        """
        logging.info("ErrorLogManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, error_log: ErrorLog) -> str:
        """
        Serialize the ErrorLog object to a JSON string using the ErrorLogSchema.
        """
        logging.info("ErrorLogManager.to_json")
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        return json.dumps(error_log_data)
    def to_dict(self, error_log: ErrorLog) -> Dict[str, Any]:
        """
        Serialize the ErrorLog object to a JSON string using the ErrorLogSchema.
        """
        logging.info("ErrorLogManager.to_dict")
        schema = ErrorLogSchema()
        error_log_data = schema.dump(error_log)
        assert isinstance(error_log_data, dict)
        return error_log_data
    def from_json(self, json_str: str) -> ErrorLog:
        """
        Deserialize a JSON string into a ErrorLog object using the ErrorLogSchema.
        """
        logging.info("ErrorLogManager.from_json")
        schema = ErrorLogSchema()
        data = json.loads(json_str)
        error_log_dict = schema.load(data)
        new_error_log = ErrorLog(**error_log_dict)
        return new_error_log
    def from_dict(self, error_log_dict: Dict[str, Any]) -> ErrorLog:
        """
        Create a ErrorLog instance from a dictionary of attributes.
        Args:
            error_log_dict (Dict[str, Any]): A dictionary containing
                error_log attributes.
        Returns:
            ErrorLog: A new ErrorLog instance created from the given dictionary.
        """
        logging.info("ErrorLogManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = ErrorLogSchema()
        error_log_dict_converted = schema.load(error_log_dict)
        # Create a new ErrorLog instance using the validated data
        new_error_log = ErrorLog(**error_log_dict_converted)
        return new_error_log
    async def add_bulk(self, error_logs: List[ErrorLog]) -> List[ErrorLog]:
        """
        Add multiple error_logs at once.
        """
        logging.info("ErrorLogManager.add_bulk")
        for error_log in error_logs:
            error_log_id = error_log.error_log_id
            code = error_log.code
            if error_log.error_log_id is not None and error_log.error_log_id > 0:
                raise ValueError(
                    f"ErrorLog is already added: {str(code)} {str(error_log_id)}"
                )
            error_log.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            error_log.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(error_logs)
        await self._session_context.session.flush()
        return error_logs
    async def update_bulk(
        self,
        error_log_updates: List[Dict[str, Any]]
    ) -> List[ErrorLog]:
        """
        #TODO add comment
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
            error_log = await self.get_by_id(error_log_id)
            if not error_log:
                raise ErrorLogNotFoundError(
                    f"ErrorLog with ID {error_log_id} not found!")
            for key, value in update.items():
                if key != "error_log_id":
                    setattr(error_log, key, value)
            error_log.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_error_logs.append(error_log)
        await self._session_context.session.flush()
        logging.info("ErrorLogManager.update_bulk end")
        return updated_error_logs
    async def delete_bulk(self, error_log_ids: List[int]) -> bool:
        """
        Delete multiple error_logs by their IDs.
        """
        logging.info("ErrorLogManager.delete_bulk")
        for error_log_id in error_log_ids:
            if not isinstance(error_log_id, int):
                raise TypeError(
                    f"The error_log_id must be an integer, "
                    f"got {type(error_log_id)} instead."
                )
            error_log = await self.get_by_id(error_log_id)
            if not error_log:
                raise ErrorLogNotFoundError(
                    f"ErrorLog with ID {error_log_id} not found!"
                )
            if error_log:
                await self._session_context.session.delete(error_log)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of error_logs.
        """
        logging.info("ErrorLogManager.count")
        result = await self._session_context.session.execute(select(ErrorLog))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[ErrorLog]:
        """
        Retrieve error_logs sorted by a particular attribute.
        """
        if sort_by == "error_log_id":
            sort_by = "_error_log_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(ErrorLog).order_by(getattr(ErrorLog, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(ErrorLog).order_by(getattr(ErrorLog, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, error_log: ErrorLog) -> ErrorLog:
        """
        Refresh the state of a given error_log instance from the database.
        """
        logging.info("ErrorLogManager.refresh")
        await self._session_context.session.refresh(error_log)
        return error_log
    async def exists(self, error_log_id: int) -> bool:
        """
        Check if a error_log with the given ID exists.
        """
        logging.info("ErrorLogManager.exists %s", error_log_id)
        if not isinstance(error_log_id, int):
            raise TypeError(
                f"The error_log_id must be an integer, "
                f"got {type(error_log_id)} instead."
            )
        error_log = await self.get_by_id(error_log_id)
        return bool(error_log)
    def is_equal(self, error_log1: ErrorLog, error_log2: ErrorLog) -> bool:
        """
        #TODO add comment
        """
        if not error_log1:
            raise TypeError("ErrorLog1 required.")
        if not error_log2:
            raise TypeError("ErrorLog2 required.")
        if not isinstance(error_log1, ErrorLog):
            raise TypeError("The error_log1 must be an ErrorLog instance.")
        if not isinstance(error_log2, ErrorLog):
            raise TypeError("The error_log2 must be an ErrorLog instance.")
        dict1 = self.to_dict(error_log1)
        dict2 = self.to_dict(error_log2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[ErrorLog]:  # PacID
        """
        #TODO add comment
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
# endset

