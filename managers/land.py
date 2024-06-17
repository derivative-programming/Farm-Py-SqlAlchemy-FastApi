# models/managers/land.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.pac import Pac  # PacID
from models.land import Land
from models.serialization_schema.land import LandSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class LandNotFoundError(Exception):
    """
    Exception raised when a specified land is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Land not found"):
        self.message = message
        super().__init__(self.message)

class LandEnum(Enum):
    """
    #TODO add comment
    """
    Unknown = 'Unknown'
    Field_One = 'Field_One'

class LandManager:
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
        logging.info("PlantManager.Initialize start")
        pac_result = await self._session_context.session.execute(select(Pac))
        pac = pac_result.scalars().first()
# endset
        if await self.from_enum(LandEnum.Unknown) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(LandEnum.Field_One) \
                is None:
            item = await self._build_lookup_item(pac)
            item.name = "Field One"
            item.lookup_enum_name = "Field_One"
            item.description = "Field One"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
# endset
        logging.info("PlantMaanger.Initialize end")
    async def from_enum(
        self,
        enum_val: LandEnum
    ) -> Land:
        """
            #TODO add comment
        """
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Land.lookup_enum_name == enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Land:
        """
            #TODO add comment
        """
        logging.info("LandManager.build")
        return Land(**kwargs)
    async def add(self, land: Land) -> Land:
        """
            #TODO add comment
        """
        logging.info("LandManager.add")
        land.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        land.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(land)
        await self._session_context.session.flush()
        return land
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("LandManager._build_query")
        query = select(
            Land,
            Pac,  # pac_id
        )
# endset
        query = query.outerjoin(  # pac_id
            Pac,
            and_(Land.pac_id == Pac._pac_id,  # pylint: disable=protected-access
                 Land.pac_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Land]:
        """
            #TODO add comment
        """
        logging.info("LandManager._run_query")
        land_query_all = self._build_query()
        if query_filter is not None:
            query = land_query_all.filter(query_filter)
        else:
            query = land_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            land = query_result_row[i]
            i = i + 1
# endset
            pac = query_result_row[i]  # pac_id
            i = i + 1
# endset
            land.pac_code_peek = (  # pac_id
                pac.code if pac else uuid.UUID(int=0))
# endset
            result.append(land)
        return result
    def _first_or_none(
        self,
        land_list: List['Land']
    ) -> Optional['Land']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            land_list (List[Land]):
                The list to retrieve the first element from.
        Returns:
            Optional[Land]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            land_list[0]
            if land_list
            else None
        )
    async def get_by_id(self, land_id: int) -> Optional[Land]:
        """
            #TODO add comment
        """
        logging.info(
            "LandManager.get_by_id start land_id: %s",
            str(land_id))
        if not isinstance(land_id, int):
            raise TypeError(
                "The land_id must be an integer, "
                f"got {type(land_id)} instead.")
        query_filter = (
            Land._land_id == land_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Land]:
        """
            #TODO add comment
        """
        logging.info("LandManager.get_by_code %s", code)
        query_filter = Land._code == str(code)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, land: Land, **kwargs) -> Optional[Land]:
        """
            #TODO add comment
        """
        logging.info("LandManager.update")
        property_list = Land.property_list()
        if land:
            land.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(land, key, value)
            await self._session_context.session.flush()
        return land
    async def delete(self, land_id: int):
        """
            #TODO add comment
        """
        logging.info("LandManager.delete %s", land_id)
        if not isinstance(land_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(land_id)} instead."
            )
        land = await self.get_by_id(land_id)
        if not land:
            raise LandNotFoundError(f"Land with ID {land_id} not found!")
        await self._session_context.session.delete(land)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Land]:
        """
            #TODO add comment
        """
        logging.info("LandManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, land: Land) -> str:
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        logging.info("LandManager.to_json")
        schema = LandSchema()
        land_data = schema.dump(land)
        return json.dumps(land_data)
    def to_dict(self, land: Land) -> dict:
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        logging.info("LandManager.to_dict")
        schema = LandSchema()
        land_data = schema.dump(land)
        return land_data
    def from_json(self, json_str: str) -> Land:
        """
        Deserialize a JSON string into a Land object using the LandSchema.
        """
        logging.info("LandManager.from_json")
        schema = LandSchema()
        data = json.loads(json_str)
        land_dict = schema.load(data)
        new_land = Land(**land_dict)
        return new_land
    def from_dict(self, land_dict: str) -> Land:
        """
        #TODO add comment
        """
        logging.info("LandManager.from_dict")
        schema = LandSchema()
        land_dict_converted = schema.load(land_dict)
        new_land = Land(**land_dict_converted)
        return new_land
    async def add_bulk(self, lands: List[Land]) -> List[Land]:
        """
        Add multiple lands at once.
        """
        logging.info("LandManager.add_bulk")
        for land in lands:
            land_id = land.land_id
            code = land.code
            if land.land_id is not None and land.land_id > 0:
                raise ValueError(
                    f"Land is already added: {str(code)} {str(land_id)}"
                )
            land.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            land.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(lands)
        await self._session_context.session.flush()
        return lands
    async def update_bulk(
        self,
        land_updates: List[Dict[int, Dict]]
    ) -> List[Land]:
        """
        #TODO add comment
        """
        logging.info("LandManager.update_bulk start")
        updated_lands = []
        for update in land_updates:
            land_id = update.get("land_id")
            if not isinstance(land_id, int):
                raise TypeError(
                    f"The land_id must be an integer, "
                    f"got {type(land_id)} instead."
                )
            if not land_id:
                continue
            logging.info("LandManager.update_bulk land_id:%s", land_id)
            land = await self.get_by_id(land_id)
            if not land:
                raise LandNotFoundError(
                    f"Land with ID {land_id} not found!")
            for key, value in update.items():
                if key != "land_id":
                    setattr(land, key, value)
            land.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_lands.append(land)
        await self._session_context.session.flush()
        logging.info("LandManager.update_bulk end")
        return updated_lands
    async def delete_bulk(self, land_ids: List[int]) -> bool:
        """
        Delete multiple lands by their IDs.
        """
        logging.info("LandManager.delete_bulk")
        for land_id in land_ids:
            if not isinstance(land_id, int):
                raise TypeError(
                    f"The land_id must be an integer, "
                    f"got {type(land_id)} instead."
                )
            land = await self.get_by_id(land_id)
            if not land:
                raise LandNotFoundError(
                    f"Land with ID {land_id} not found!"
                )
            if land:
                await self._session_context.session.delete(land)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of lands.
        """
        logging.info("LandManager.count")
        result = await self._session_context.session.execute(select(Land))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Land]:
        """
        Retrieve lands sorted by a particular attribute.
        """
        if sort_by == "land_id":
            sort_by = "_land_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Land).order_by(getattr(Land, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Land).order_by(getattr(Land, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, land: Land) -> Land:
        """
        Refresh the state of a given land instance from the database.
        """
        logging.info("LandManager.refresh")
        await self._session_context.session.refresh(land)
        return land
    async def exists(self, land_id: int) -> bool:
        """
        Check if a land with the given ID exists.
        """
        logging.info("LandManager.exists %s", land_id)
        if not isinstance(land_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(land_id)} instead."
            )
        land = await self.get_by_id(land_id)
        return bool(land)
    def is_equal(self, land1: Land, land2: Land) -> bool:
        """
        #TODO add comment
        """
        if not land1:
            raise TypeError("Land1 required.")
        if not land2:
            raise TypeError("Land2 required.")
        if not isinstance(land1, Land):
            raise TypeError("The land1 must be an Land instance.")
        if not isinstance(land2, Land):
            raise TypeError("The land2 must be an Land instance.")
        dict1 = self.to_dict(land1)
        dict2 = self.to_dict(land2)
        return dict1 == dict2
# endset
    async def get_by_pac_id(self, pac_id: int) -> List[Land]:  # PacID
        """
        #TODO add comment
        """
        logging.info("LandManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(
                f"The land_id must be an integer, "
                f"got {type(pac_id)} instead."
            )
        query_filter = Land.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

