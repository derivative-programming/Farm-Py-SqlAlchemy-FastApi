# models/managers/date_greater_than_filter.py

"""
    #TODO add comment
"""

import json
import uuid
import logging
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.date_greater_than_filter import DateGreaterThanFilter
from models.serialization_schema.date_greater_than_filter import (
    DateGreaterThanFilterSchema)
from services.db_config import generate_uuid, DB_DIALECT
from services.logging_config import get_logger
logger = get_logger(__name__)


class DateGreaterThanFilterNotFoundError(Exception):
    """
        #TODO add comment
    """
    pass


##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start
class DateGreaterThanFilterEnum(Enum):
    """
    #TODO add comment
    """
    Last_24_Hours = 'Last_24_Hours'
    Last_7_Days = 'Last_7_Days'
    Last_30_Days = 'Last_30_Days'
    Last_90_Days = 'Last_90_Days'
    Last_365_Days = 'Last_365_Days'
    Unknown = 'Unknown'
##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End


class DateGreaterThanFilterManager:
    """
        #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context

    def convert_uuid_to_model_uuid(self, value: uuid):
        # Conditionally set the UUID column type
        if DB_DIALECT == 'postgresql':
            return value
        elif DB_DIALECT == 'mssql':
            return value
        else:  # This will cover SQLite, MySQL, and other databases
            return str(value)

##GENTrainingBlock[caseIsLookupObject]Start
##GENLearn[isLookup=true]Start
    async def _build_lookup_item(self, pac: Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item

    async def initialize(self):
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(DateGreaterThanFilterEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.Last_24_Hours) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 24 Hours"
            item.lookup_enum_name = "Last_24_Hours"
            item.description = "Last 24 Hours"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 1
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.Last_7_Days) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 7 Days"
            item.lookup_enum_name = "Last_7_Days"
            item.description = "Last 7 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 7
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.Last_30_Days) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 30 Days"
            item.lookup_enum_name = "Last_30_Days"
            item.description = "Last 30 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 30
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.Last_90_Days) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 90 Days"
            item.lookup_enum_name = "Last_90_Days"
            item.description = "Last 90 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 90
            await self.add(item)
        if await self.from_enum(DateGreaterThanFilterEnum.Last_365_Days) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Last 365 Days"
            item.lookup_enum_name = "Last_365_Days"
            item.description = "Last 365 Days"
            item.display_order = await self.count()
            item.is_active = True
            # item.day_count = 365
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")

    async def from_enum(
        self,
        enum_val: DateGreaterThanFilterEnum
    ) -> DateGreaterThanFilter:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = DateGreaterThanFilter.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
##GENLearn[isLookup=true]End
##GENTrainingBlock[caseIsLookupObject]End

    async def build(self, **kwargs) -> DateGreaterThanFilter:
        logging.info("DateGreaterThanFilterManager.build")
        return DateGreaterThanFilter(**kwargs)

    async def add(
        self,
        date_greater_than_filter: DateGreaterThanFilter
    ) -> DateGreaterThanFilter:
        logging.info("DateGreaterThanFilterManager.add")
        date_greater_than_filter.insert_user_id = (
            self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            )
        date_greater_than_filter.last_update_user_id = (
            self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        )
        self._session_context.session.add(date_greater_than_filter)
        await self._session_context.session.flush()
        return date_greater_than_filter

    def _build_query(self):
        logging.info("DateGreaterThanFilterManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Pac, and_(DateGreaterThanFilter.pac_id == Pac.pac_id, DateGreaterThanFilter.pac_id != 0))
#
#         if join_condition is not None:
#             query = select(DateGreaterThanFilter
#                         , Pac  # pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(DateGreaterThanFilter)
        query = select(DateGreaterThanFilter
                    , Pac  # pac_id
                    )

        query = query.outerjoin(Pac, and_(DateGreaterThanFilter.pac_id == Pac.pac_id, DateGreaterThanFilter.pac_id != 0))

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[DateGreaterThanFilter]:
        logging.info("DateGreaterThanFilterManager._run_query")
        date_greater_than_filter_query_all = self._build_query()
        if query_filter is not None:
            query = date_greater_than_filter_query_all.filter(query_filter)
        else:
            query = date_greater_than_filter_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            date_greater_than_filter = query_result_row[i]
            i = i + 1

            pac = query_result_row[i]  # pac_id
            i = i + 1

            date_greater_than_filter.pac_code_peek = pac.code if pac else uuid.UUID(int=0)  # pac_id

            result.append(date_greater_than_filter)
        return result

    def _first_or_none(
        self,
        date_greater_than_filter_list: List
    ) -> DateGreaterThanFilter:
        return date_greater_than_filter_list[0] if date_greater_than_filter_list else None

    async def get_by_id(
        self,
        date_greater_than_filter_id: int
    ) -> Optional[DateGreaterThanFilter]:
        logging.info(
            "DateGreaterThanFilterManager.get_by_id "
            "start date_greater_than_filter_id:" + str(date_greater_than_filter_id))
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(
                "The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
        query_filter = DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def get_by_code(
        self,
        code: uuid.UUID
    ) -> Optional[DateGreaterThanFilter]:
        logging.info("DateGreaterThanFilterManager.get_by_code {code}")
        query_filter = DateGreaterThanFilter.code == code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def update(
        self,
        date_greater_than_filter: DateGreaterThanFilter,
        **kwargs
    ) -> Optional[DateGreaterThanFilter]:
        logging.info("DateGreaterThanFilterManager.update")
        property_list = DateGreaterThanFilter.property_list()
        if date_greater_than_filter:
            date_greater_than_filter.last_update_user_id = (
                self.convert_uuid_to_model_uuid(
                    self._session_context.customer_code)
            )
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(date_greater_than_filter, key, value)
            await self._session_context.session.flush()
        return date_greater_than_filter

    async def delete(self, date_greater_than_filter_id: int):
        logging.info(
            "DateGreaterThanFilterManager.delete %s",
            date_greater_than_filter_id)
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError(
                "The date_greater_than_filter_id must be an integer, "
                "got {type(date_greater_than_filter_id)} instead.")
        date_greater_than_filter = await self.get_by_id(
            date_greater_than_filter_id)
        if not date_greater_than_filter:
            raise DateGreaterThanFilterNotFoundError(
                f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
        await self._session_context.session.delete(date_greater_than_filter)
        await self._session_context.session.flush()

    async def get_list(self) -> List[DateGreaterThanFilter]:
        logging.info(
            "DateGreaterThanFilterManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    
    def to_json(
        self,
        date_greater_than_filter: DateGreaterThanFilter
    ) -> str:
        """
        Serialize the DateGreaterThanFilter object to a JSON string using 
        the DateGreaterThanFilterSchema.
        """
        logging.info("DateGreaterThanFilterManager.to_json")
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        return json.dumps(date_greater_than_filter_data)

    def to_dict(
        self,
        date_greater_than_filter: DateGreaterThanFilter
    ) -> dict:
        """
        Serialize the DateGreaterThanFilter object to a JSON string using 
        the DateGreaterThanFilterSchema.
        """
        logging.info("DateGreaterThanFilterManager.to_dict")
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        return date_greater_than_filter_data

    def from_json(
        self,
        json_str: str
    ) -> DateGreaterThanFilter:
        """
        Deserialize a JSON string into a DateGreaterThanFilter object 
        using the DateGreaterThanFilterSchema.
        """
        logging.info("DateGreaterThanFilterManager.from_json")
        schema = DateGreaterThanFilterSchema()
        data = json.loads(json_str)
        date_greater_than_filter_dict = schema.load(data)
        new_date_greater_than_filter = DateGreaterThanFilter(
            **date_greater_than_filter_dict)
        return new_date_greater_than_filter

    def from_dict(
        self,
        date_greater_than_filter_dict: str
    ) -> DateGreaterThanFilter:
        logging.info("DateGreaterThanFilterManager.from_dict")
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_dict_converted = schema.load(
            date_greater_than_filter_dict)
        new_date_greater_than_filter = DateGreaterThanFilter(
            **date_greater_than_filter_dict_converted)
        return new_date_greater_than_filter

    async def add_bulk(
        self,
        date_greater_than_filters: List[DateGreaterThanFilter]
    ) -> List[DateGreaterThanFilter]:
        """Add multiple date_greater_than_filters at once."""
        logging.info("DateGreaterThanFilterManager.add_bulk")
        for date_greater_than_filter in date_greater_than_filters:
            if date_greater_than_filter.date_greater_than_filter_id is not None and date_greater_than_filter.date_greater_than_filter_id > 0:
                raise ValueError(
                    "DateGreaterThanFilter is already added: " + str(date_greater_than_filter.code) + " " + str(date_greater_than_filter.date_greater_than_filter_id))
            date_greater_than_filter.insert_user_id = (
                self.convert_uuid_to_model_uuid(
                    self._session_context.customer_code)
            )
            date_greater_than_filter.last_update_user_id = (
                self.convert_uuid_to_model_uuid(
                    self._session_context.customer_code)
            )
        self._session_context.session.add_all(date_greater_than_filters)
        await self._session_context.session.flush()
        return date_greater_than_filters

    async def update_bulk(
        self,
        date_greater_than_filter_updates: List[Dict[int, Dict]]
    ) -> List[DateGreaterThanFilter]:
        logging.info(
            "DateGreaterThanFilterManager.update_bulk start")
        updated_date_greater_than_filters = []
        for update in date_greater_than_filter_updates:
            date_greater_than_filter_id = update.get(
                "date_greater_than_filter_id")
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError(
                    "The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
            if not date_greater_than_filter_id:
                continue
            logging.info(
                "DateGreaterThanFilterManager.update_bulk date_greater_than_filter_id:{date_greater_than_filter_id}")
            date_greater_than_filter = await self.get_by_id(
                date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(
                    f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
            for key, value in update.items():
                if key != "date_greater_than_filter_id":
                    setattr(date_greater_than_filter, key, value)
            date_greater_than_filter.last_update_user_id = (
                self.convert_uuid_to_model_uuid(
                    self._session_context.customer_code)
            )
            updated_date_greater_than_filters.append(date_greater_than_filter)
        await self._session_context.session.flush()
        logging.info("DateGreaterThanFilterManager.update_bulk end")
        return updated_date_greater_than_filters

    async def delete_bulk(self, date_greater_than_filter_ids: List[int]) -> bool:
        logging.info("DateGreaterThanFilterManager.delete_bulk")
        """Delete multiple date_greater_than_filters by their IDs."""
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            if not isinstance(date_greater_than_filter_id, int):
                raise TypeError("The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
            date_greater_than_filter = await self.get_by_id(
                date_greater_than_filter_id)
            if not date_greater_than_filter:
                raise DateGreaterThanFilterNotFoundError(
                    f"DateGreaterThanFilter with ID {date_greater_than_filter_id} not found!")
            if date_greater_than_filter:
                await self._session_context.session.delete(
                    date_greater_than_filter)
        await self._session_context.session.flush()
        return True

    async def count(self) -> int:
        logging.info("DateGreaterThanFilterManager.count")
        """Return the total number of date_greater_than_filters."""
        result = await self._session_context.session.execute(select(DateGreaterThanFilter))
        return len(result.scalars().all())
    
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
        self,
        sort_by: str,
        order: Optional[str] = "asc"
    ) -> List[DateGreaterThanFilter]:
        """
        Retrieve date_greater_than_filters sorted by a 
        particular attribute.
        """
        if order == "asc":
            result = await self._session_context.session.execute(
                select(DateGreaterThanFilter).order_by(
                    getattr(DateGreaterThanFilter, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(DateGreaterThanFilter).order_by(
                    getattr(DateGreaterThanFilter, sort_by).desc()))
        return result.scalars().all()

    async def refresh(
        self,
        date_greater_than_filter: DateGreaterThanFilter
    ) -> DateGreaterThanFilter:
        """
        Refresh the state of a given date_greater_than_filter 
        instance from the database.
        """
        logging.info("DateGreaterThanFilterManager.refresh")
        await self._session_context.session.refresh(date_greater_than_filter)
        return date_greater_than_filter

    async def exists(
        self,
        date_greater_than_filter_id: int
    ) -> bool:
        """
        Check if a date_greater_than_filter with 
        the given ID exists.
        """
        logging.info("DateGreaterThanFilterManager.exists {date_greater_than_filter_id}")
        if not isinstance(date_greater_than_filter_id, int):
            raise TypeError("The date_greater_than_filter_id must be an integer, got {type(date_greater_than_filter_id)} instead.")
        date_greater_than_filter = await self.get_by_id(
            date_greater_than_filter_id)
        return bool(date_greater_than_filter)

    def is_equal(
        self,
        date_greater_than_filter1: DateGreaterThanFilter,
        date_greater_than_filter2: DateGreaterThanFilter
    ) -> bool:
        if not date_greater_than_filter1:
            raise TypeError("DateGreaterThanFilter1 required.")
        if not date_greater_than_filter2:
            raise TypeError("DateGreaterThanFilter2 required.")
        if not isinstance(date_greater_than_filter1, DateGreaterThanFilter):
            raise TypeError(
                "The date_greater_than_filter1 must be an DateGreaterThanFilter instance.")
        if not isinstance(date_greater_than_filter2, DateGreaterThanFilter):
            raise TypeError(
                "The date_greater_than_filter2 must be an DateGreaterThanFilter instance.")
        dict1 = self.to_dict(date_greater_than_filter1)
        dict2 = self.to_dict(date_greater_than_filter2)
        return dict1 == dict2

    async def get_by_pac_id(  # PacID
        self,
        pac_id: int
    ) -> List[DateGreaterThanFilter]:
        logging.info("DateGreaterThanFilterManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError("The date_greater_than_filter_id must be an integer, got {type(pac_id)} instead.")
        query_filter = DateGreaterThanFilter.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
