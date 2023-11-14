import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.flavor import Flavor
from models.serialization_schema.flavor import FlavorSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class FlavorNotFoundError(Exception):
    pass

class FlavorEnum(Enum):
    Unknown = 'Unknown'
    Sweet = 'Sweet'
    Sour = 'Sour'

class FlavorManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _build_lookup_item(self, pac:Pac):
        item = await self.build()
        item.pac_id = pac.pac_id
        return item
    async def initialize(self):
        logging.info("PlantManager.Initialize start")
        pac_result = await self.session.execute(select(Pac))
        pac = pac_result.scalars().first()

        if self.from_enum(FlavorEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Unknown"
            item.lookup_enum_name = "Unknown"
            item.description = "Unknown"
            item.display_order = self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if self.from_enum(FlavorEnum.Sweet) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sweet"
            item.lookup_enum_name = "Sweet"
            item.description = "Sweet"
            item.display_order = self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if self.from_enum(FlavorEnum.Sour) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Sour"
            item.lookup_enum_name = "Sour"
            item.description = "Sour"
            item.display_order = self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)

        logging.info("PlantMaanger.Initialize end")
    async def from_enum(self, enum_val:FlavorEnum) -> Flavor:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Flavor.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Flavor:
        logging.info("FlavorManager.build")
        return Flavor(**kwargs)
    async def add(self, flavor: Flavor) -> Flavor:
        logging.info("FlavorManager.add")
        self.session.add(flavor)
        await self.session.flush()
        return flavor
    def _build_query(self):
        logging.info("FlavorManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Pac, and_(Flavor.pac_id == Pac.pac_id, Flavor.pac_id != 0))
#
#         if join_condition is not None:
#             query = select(Flavor
#                         ,Pac #pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Flavor)
        query = select(Flavor
                    ,Pac #pac_id
                    )

        query = query.outerjoin(Pac, and_(Flavor.pac_id == Pac.pac_id, Flavor.pac_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[Flavor]:
        logging.info("FlavorManager._run_query")
        flavor_query_all = self._build_query()
        if query_filter is not None:
            query = flavor_query_all.filter(query_filter)
        else:
            query = flavor_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            flavor = query_result_row[i]
            i = i + 1

            pac = query_result_row[i] #pac_id
            i = i + 1

            flavor.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(flavor)
        return result
    def _first_or_none(self,flavor_list:List) -> Flavor:
        return flavor_list[0] if flavor_list else None
    async def get_by_id(self, flavor_id: int) -> Optional[Flavor]:
        logging.info("FlavorManager.get_by_id start flavor_id:" + str(flavor_id))
        if not isinstance(flavor_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
        # result = await self.session.execute(select(Flavor).filter(Flavor.flavor_id == flavor_id))
        # result = await self.session.execute(select(Flavor).filter(Flavor.flavor_id == flavor_id))
        # return result.scalars().first()
        query_filter = Flavor.flavor_id == flavor_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Flavor]:
        logging.info(f"FlavorManager.get_by_code {code}")
        # result = await self.session.execute(select(Flavor).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Flavor.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, flavor: Flavor, **kwargs) -> Optional[Flavor]:
        logging.info("FlavorManager.update")
        if flavor:
            for key, value in kwargs.items():
                setattr(flavor, key, value)
            await self.session.flush()
        return flavor
    async def delete(self, flavor_id: int):
        logging.info(f"FlavorManager.delete {flavor_id}")
        if not isinstance(flavor_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
        flavor = await self.get_by_id(flavor_id)
        if not flavor:
            raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
        await self.session.delete(flavor)
        await self.session.flush()
    async def get_list(self) -> List[Flavor]:
        logging.info("FlavorManager.get_list")
        # result = await self.session.execute(select(Flavor))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, flavor:Flavor) -> str:
        logging.info("FlavorManager.to_json")
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return json.dumps(flavor_data)
    def to_dict(self, flavor:Flavor) -> dict:
        logging.info("FlavorManager.to_dict")
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return flavor_data
    def from_json(self, json_str: str) -> Flavor:
        logging.info("FlavorManager.from_json")
        """
        Deserialize a JSON string into a Flavor object using the FlavorSchema.
        """
        schema = FlavorSchema()
        data = json.loads(json_str)
        flavor_dict = schema.load(data)
        new_flavor = Flavor(**flavor_dict)
        return new_flavor
    def from_dict(self, flavor_dict: str) -> Flavor:
        logging.info("FlavorManager.from_dict")
        schema = FlavorSchema()
        flavor_dict_converted = schema.load(flavor_dict)
        new_flavor = Flavor(**flavor_dict_converted)
        return new_flavor
    async def add_bulk(self, flavors: List[Flavor]) -> List[Flavor]:
        logging.info("FlavorManager.add_bulk")
        """Add multiple flavors at once."""
        self.session.add_all(flavors)
        await self.session.flush()
        return flavors
    async def update_bulk(self, flavor_updates: List[Dict[int, Dict]]) -> List[Flavor]:
        logging.info("FlavorManager.update_bulk start")
        updated_flavors = []
        for update in flavor_updates:
            flavor_id = update.get("flavor_id")
            if not isinstance(flavor_id, int):
                raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
            if not flavor_id:
                continue
            logging.info(f"FlavorManager.update_bulk flavor_id:{flavor_id}")
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
            for key, value in update.items():
                if key != "flavor_id":
                    setattr(flavor, key, value)
            updated_flavors.append(flavor)
        await self.session.flush()
        logging.info("FlavorManager.update_bulk end")
        return updated_flavors
    async def delete_bulk(self, flavor_ids: List[int]) -> bool:
        logging.info("FlavorManager.delete_bulk")
        """Delete multiple flavors by their IDs."""
        for flavor_id in flavor_ids:
            if not isinstance(flavor_id, int):
                raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
            if flavor:
                await self.session.delete(flavor)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("FlavorManager.count")
        """Return the total number of flavors."""
        result = await self.session.execute(select(Flavor))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Flavor]:
        """Retrieve flavors sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Flavor).order_by(getattr(Flavor, sort_by).asc()))
        else:
            result = await self.session.execute(select(Flavor).order_by(getattr(Flavor, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, flavor: Flavor) -> Flavor:
        logging.info("FlavorManager.refresh")
        """Refresh the state of a given flavor instance from the database."""
        await self.session.refresh(flavor)
        return flavor
    async def exists(self, flavor_id: int) -> bool:
        logging.info(f"FlavorManager.exists {flavor_id}")
        """Check if a flavor with the given ID exists."""
        if not isinstance(flavor_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
        flavor = await self.get_by_id(flavor_id)
        return bool(flavor)
    def is_equal(self, flavor1:Flavor, flavor2:Flavor) -> bool:
        if not flavor1:
            raise TypeError("Flavor1 required.")
        if not flavor2:
            raise TypeError("Flavor2 required.")
        if not isinstance(flavor1, Flavor):
            raise TypeError("The flavor1 must be an Flavor instance.")
        if not isinstance(flavor2, Flavor):
            raise TypeError("The flavor2 must be an Flavor instance.")
        dict1 = self.to_dict(flavor1)
        dict2 = self.to_dict(flavor2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Flavor]: # PacID
        logging.info("FlavorManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(pac_id)} instead.")
        # result = await self.session.execute(select(Flavor).filter(Flavor.pac_id == pac_id))
        # return result.scalars().all()
        query_filter = Flavor.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

