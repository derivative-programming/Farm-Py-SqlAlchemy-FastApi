# models/managers/tri_state_filter.py
# pylint: disable=unused-import
"""
This module contains the TriStateFilterManager class, which is
responsible for managing tri_state_filters in the system.
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
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class TriStateFilterNotFoundError(Exception):
    """
    Exception raised when a specified tri_state_filter is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="TriStateFilter not found"):
        self.message = message
        super().__init__(self.message)

class TriStateFilterEnum(Enum):
    """
    #TODO add comment
    """
    UNKNOWN = 'Unknown'
    YES = 'Yes'
    NO = 'No'

class TriStateFilterManager:
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

    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(TriStateFilterEnum.UNKNOWN) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.YES) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Yes"
            item.lookup_enum_name = "Yes"
            item.description = "Yes"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.NO) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "No"
            item.lookup_enum_name = "No"
            item.description = "No"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
# endset
        logging.info("TriStateFilterManager.Initialize end")
    async def from_enum(
        self,
        enum_val: TriStateFilterEnum
    ) -> TriStateFilter:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = (
            TriStateFilter._lookup_enum_name == enum_val.value)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> TriStateFilter:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.build")
        return TriStateFilter(**kwargs)
    async def add(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.add")
        tri_state_filter.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        tri_state_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(tri_state_filter)
        await self._session_context.session.flush()
        return tri_state_filter
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager._build_query")
        query = select(
            TriStateFilter,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(TriStateFilter._pac_id == Pac._pac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 TriStateFilter._pac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager._run_query")
        tri_state_filter_query_all = self._build_query()
        if query_filter is not None:
            query = tri_state_filter_query_all.filter(query_filter)
        else:
            query = tri_state_filter_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            tri_state_filter = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            tri_state_filter.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(tri_state_filter)
        return result
    def _first_or_none(
        self,
        tri_state_filter_list: List['TriStateFilter']
    ) -> Optional['TriStateFilter']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            tri_state_filter_list (List[TriStateFilter]):
                The list to retrieve the first element from.
        Returns:
            Optional[TriStateFilter]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            tri_state_filter_list[0]
            if tri_state_filter_list
            else None
        )
    async def get_by_id(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info(
            "TriStateFilterManager.get_by_id start tri_state_filter_id: %s",
            str(tri_state_filter_id))
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                "The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead.")
        query_filter = (
            TriStateFilter._tri_state_filter_id == tri_state_filter_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.get_by_code %s", code)
        query_filter = TriStateFilter._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, tri_state_filter: TriStateFilter, **kwargs) -> Optional[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.update")
        property_list = TriStateFilter.property_list()
        if tri_state_filter:
            tri_state_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(tri_state_filter, key, value)
            await self._session_context.session.flush()
        return tri_state_filter
    async def delete(self, tri_state_filter_id: int):
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.delete %s", tri_state_filter_id)
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead."
            )
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        if not tri_state_filter:
            raise TriStateFilterNotFoundError(f"TriStateFilter with ID {tri_state_filter_id} not found!")
        await self._session_context.session.delete(tri_state_filter)
        await self._session_context.session.flush()
    async def get_list(self) -> List[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, tri_state_filter: TriStateFilter) -> str:
        """
        Serialize the TriStateFilter object to a JSON string using the TriStateFilterSchema.
        """
        logging.info("TriStateFilterManager.to_json")
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        return json.dumps(tri_state_filter_data)
    def to_dict(self, tri_state_filter: TriStateFilter) -> Dict[str, Any]:
        """
        Serialize the TriStateFilter object to a JSON string using the TriStateFilterSchema.
        """
        logging.info("TriStateFilterManager.to_dict")
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        assert isinstance(tri_state_filter_data, dict)
        return tri_state_filter_data
    def from_json(self, json_str: str) -> TriStateFilter:
        """
        Deserializes a JSON string into a TriStateFilter object using the TriStateFilterSchema.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            TriStateFilter: The deserialized TriStateFilter object.
        """
        logging.info("TriStateFilterManager.from_json")
        schema = TriStateFilterSchema()
        data = json.loads(json_str)
        tri_state_filter_dict = schema.load(data)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)
        return new_tri_state_filter
    def from_dict(self, tri_state_filter_dict: Dict[str, Any]) -> TriStateFilter:
        """
        Creates a TriStateFilter instance from a dictionary of attributes.
        Args:
            tri_state_filter_dict (Dict[str, Any]): A dictionary containing
                tri_state_filter attributes.
        Returns:
            TriStateFilter: A new TriStateFilter instance created from the given dictionary.
        """
        logging.info("TriStateFilterManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = TriStateFilterSchema()
        tri_state_filter_dict_converted = schema.load(tri_state_filter_dict)
        # Create a new TriStateFilter instance using the validated data
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict_converted)
        return new_tri_state_filter
    async def add_bulk(self, tri_state_filters: List[TriStateFilter]) -> List[TriStateFilter]:
        """
        Adds multiple tri_state_filters at once.
        Args:
            tri_state_filters (List[TriStateFilter]): The list of tri_state_filters to add.
        Returns:
            List[TriStateFilter]: The list of added tri_state_filters.
        """
        logging.info("TriStateFilterManager.add_bulk")
        for tri_state_filter in tri_state_filters:
            tri_state_filter_id = tri_state_filter.tri_state_filter_id
            code = tri_state_filter.code
            if tri_state_filter.tri_state_filter_id is not None and tri_state_filter.tri_state_filter_id > 0:
                raise ValueError(
                    f"TriStateFilter is already added: {str(code)} {str(tri_state_filter_id)}"
                )
            tri_state_filter.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            tri_state_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(tri_state_filters)
        await self._session_context.session.flush()
        return tri_state_filters
    async def update_bulk(
        self,
        tri_state_filter_updates: List[Dict[str, Any]]
    ) -> List[TriStateFilter]:
        """
        #TODO add comment
        """
        logging.info("TriStateFilterManager.update_bulk start")
        updated_tri_state_filters = []
        for update in tri_state_filter_updates:
            tri_state_filter_id = update.get("tri_state_filter_id")
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(
                    f"The tri_state_filter_id must be an integer, "
                    f"got {type(tri_state_filter_id)} instead."
                )
            if not tri_state_filter_id:
                continue
            logging.info("TriStateFilterManager.update_bulk tri_state_filter_id:%s", tri_state_filter_id)
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(
                    f"TriStateFilter with ID {tri_state_filter_id} not found!")
            for key, value in update.items():
                if key != "tri_state_filter_id":
                    setattr(tri_state_filter, key, value)
            tri_state_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_tri_state_filters.append(tri_state_filter)
        await self._session_context.session.flush()
        logging.info("TriStateFilterManager.update_bulk end")
        return updated_tri_state_filters
    async def delete_bulk(self, tri_state_filter_ids: List[int]) -> bool:
        """
        Delete multiple tri_state_filters by their IDs.
        """
        logging.info("TriStateFilterManager.delete_bulk")
        for tri_state_filter_id in tri_state_filter_ids:
            if not isinstance(tri_state_filter_id, int):
                raise TypeError(
                    f"The tri_state_filter_id must be an integer, "
                    f"got {type(tri_state_filter_id)} instead."
                )
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(
                    f"TriStateFilter with ID {tri_state_filter_id} not found!"
                )
            if tri_state_filter:
                await self._session_context.session.delete(tri_state_filter)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of tri_state_filters.
        """
        logging.info("TriStateFilterManager.count")
        result = await self._session_context.session.execute(select(TriStateFilter))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[TriStateFilter]:
        """
        Retrieve tri_state_filters sorted by a particular attribute.
        """
        if sort_by == "tri_state_filter_id":
            sort_by = "_tri_state_filter_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(TriStateFilter).order_by(getattr(TriStateFilter, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(TriStateFilter).order_by(getattr(TriStateFilter, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, tri_state_filter: TriStateFilter) -> TriStateFilter:
        """
        Refresh the state of a given tri_state_filter instance from the database.
        """
        logging.info("TriStateFilterManager.refresh")
        await self._session_context.session.refresh(tri_state_filter)
        return tri_state_filter
    async def exists(self, tri_state_filter_id: int) -> bool:
        """
        Check if a tri_state_filter with the given ID exists.
        """
        logging.info("TriStateFilterManager.exists %s", tri_state_filter_id)
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(tri_state_filter_id)} instead."
            )
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        return bool(tri_state_filter)
    def is_equal(self, tri_state_filter1: TriStateFilter, tri_state_filter2: TriStateFilter) -> bool:
        """
        #TODO add comment
        """
        if not tri_state_filter1:
            raise TypeError("TriStateFilter1 required.")
        if not tri_state_filter2:
            raise TypeError("TriStateFilter2 required.")
        if not isinstance(tri_state_filter1, TriStateFilter):
            raise TypeError("The tri_state_filter1 must be an TriStateFilter instance.")
        if not isinstance(tri_state_filter2, TriStateFilter):
            raise TypeError("The tri_state_filter2 must be an TriStateFilter instance.")
        dict1 = self.to_dict(tri_state_filter1)
        dict2 = self.to_dict(tri_state_filter2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[TriStateFilter]:  # PacID
        """
        #TODO add comment
        """
        logging.info("TriStateFilterManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The tri_state_filter_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = TriStateFilter._pac_id == pac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

