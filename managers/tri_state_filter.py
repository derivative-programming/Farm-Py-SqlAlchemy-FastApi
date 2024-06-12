# models/managers/tri_state_filter.py
"""
    #TODO add comment
"""
import json
import logging
import random
import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.tri_state_filter import TriStateFilter
from models.serialization_schema.tri_state_filter import TriStateFilterSchema
from services.db_config import generate_uuid, DB_DIALECT
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
    Unknown = 'Unknown'
    Yes = 'Yes'
    No = 'No'

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
    def convert_uuid_to_model_uuid(self, value: uuid):
        """
            #TODO add comment
        """
        # Conditionally set the UUID column type
        if DB_DIALECT == 'postgresql':
            return value
        elif DB_DIALECT == 'mssql':
            return value
        else:  # This will cover SQLite, MySQL, and other databases
            return str(value)

    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(TriStateFilterEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.Yes) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Yes"
            item.lookup_enum_name = "Yes"
            item.description = "Yes"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
        if await self.from_enum(TriStateFilterEnum.No) is None:
            item = await self._build_lookup_item(pac)
            item.name = "No"
            item.lookup_enum_name = "No"
            item.description = "No"
            item.display_order = await self.count()
            item.is_active = True
            # item.state_int_value = 1
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")
    async def from_enum(
        self,
        enum_val: TriStateFilterEnum
    ) -> TriStateFilter:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = TriStateFilter.lookup_enum_name == enum_val.value
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
#         join_condition = None
# # endset
#         join_condition = outerjoin(join_condition, Pac, and_(TriStateFilter.pac_id == Pac.pac_id, TriStateFilter.pac_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(TriStateFilter
#                         , Pac  # pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(TriStateFilter)
        query = select(
            TriStateFilter
            , Pac  # pac_id
            )
# endset
        query = query.outerjoin(Pac, and_(TriStateFilter.pac_id == Pac.pac_id, TriStateFilter.pac_id != 0))
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
            tri_state_filter.pac_code_peek = pac.code if pac else uuid.UUID(int=0)  # pac_id
# endset
            result.append(tri_state_filter)
        return result
    def _first_or_none(self, tri_state_filter_list: List) -> TriStateFilter:
        """
            #TODO add comment
        """
        return tri_state_filter_list[0] if tri_state_filter_list else None
    async def get_by_id(self, tri_state_filter_id: int) -> Optional[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info(
            "TriStateFilterManager.get_by_id start tri_state_filter_id: %s",
            str(tri_state_filter_id))
        if not isinstance(tri_state_filter_id, int):
            raise TypeError(
                "The tri_state_filter_id must be an integer, got %s instead.",
                type(tri_state_filter_id))
        query_filter = TriStateFilter.tri_state_filter_id == tri_state_filter_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[TriStateFilter]:
        """
            #TODO add comment
        """
        logging.info("TriStateFilterManager.get_by_code %s", code)
        query_filter = TriStateFilter.code == code
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
                "The tri_state_filter_id must be an integer, got %s instead.",
                type(tri_state_filter_id))
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
    def to_dict(self, tri_state_filter: TriStateFilter) -> dict:
        """
        Serialize the TriStateFilter object to a JSON string using the TriStateFilterSchema.
        """
        logging.info("TriStateFilterManager.to_dict")
        schema = TriStateFilterSchema()
        tri_state_filter_data = schema.dump(tri_state_filter)
        return tri_state_filter_data
    def from_json(self, json_str: str) -> TriStateFilter:
        """
        Deserialize a JSON string into a TriStateFilter object using the TriStateFilterSchema.
        """
        logging.info("TriStateFilterManager.from_json")
        schema = TriStateFilterSchema()
        data = json.loads(json_str)
        tri_state_filter_dict = schema.load(data)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict)
        return new_tri_state_filter
    def from_dict(self, tri_state_filter_dict: str) -> TriStateFilter:
        """
        #TODO add comment
        """
        logging.info("TriStateFilterManager.from_dict")
        schema = TriStateFilterSchema()
        tri_state_filter_dict_converted = schema.load(tri_state_filter_dict)
        new_tri_state_filter = TriStateFilter(**tri_state_filter_dict_converted)
        return new_tri_state_filter
    async def add_bulk(self, tri_state_filters: List[TriStateFilter]) -> List[TriStateFilter]:
        """
        Add multiple tri_state_filters at once.
        """
        logging.info("TriStateFilterManager.add_bulk")
        for tri_state_filter in tri_state_filters:
            if tri_state_filter.tri_state_filter_id is not None and tri_state_filter.tri_state_filter_id > 0:
                raise ValueError("TriStateFilter is already added: " +
                                 str(tri_state_filter.code) +
                                 " " + str(tri_state_filter.tri_state_filter_id))
            tri_state_filter.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            tri_state_filter.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(tri_state_filters)
        await self._session_context.session.flush()
        return tri_state_filters
    async def update_bulk(
            self,
            tri_state_filter_updates: List[Dict[int, Dict]]
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
                    "The tri_state_filter_id must be an integer, got %s instead.",
                    type(tri_state_filter_id))
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
                    "The tri_state_filter_id must be an integer, got %s instead.",
                    type(tri_state_filter_id))
            tri_state_filter = await self.get_by_id(tri_state_filter_id)
            if not tri_state_filter:
                raise TriStateFilterNotFoundError(
                    "TriStateFilter with ID %s not found!",
                    tri_state_filter_id)
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
                "The tri_state_filter_id must be an integer, got %s instead.",
                type(tri_state_filter_id))
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
        logging.info("TriStateFilterManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                "The tri_state_filter_id must be an integer, got %s instead.",
                type(pac_id)
                )
        query_filter = TriStateFilter.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

