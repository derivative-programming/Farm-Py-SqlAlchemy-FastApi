import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.pac import Pac # PacID
from models.tac import Tac
from models.serialization_schema.tac import TacSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class TacNotFoundError(Exception):
    pass

class TacEnum(Enum):
    Unknown = 'Unknown'
    Primary = 'Primary'

class TacManager:
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

        if await self.from_enum(TacEnum.Unknown) is None:
            item = await self._build_lookup_item(pac)
            item.name = ""
            item.lookup_enum_name = "Unknown"
            item.description = ""
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)
        if await self.from_enum(TacEnum.Primary) is None:
            item = await self._build_lookup_item(pac)
            item.name = "Primary"
            item.lookup_enum_name = "Primary"
            item.description = "Primary"
            item.display_order = await self.count()
            item.is_active = True
            # item. = 1
            await self.add(item)

        logging.info("PlantMaanger.Initialize end")
    async def from_enum(self, enum_val:TacEnum) -> Tac:
        # return self.get(lookup_enum_name=enum_val.value)
        query_filter = Tac.lookup_enum_name==enum_val.value
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)

    async def build(self, **kwargs) -> Tac:
        logging.info("TacManager.build")
        return Tac(**kwargs)
    async def add(self, tac: Tac) -> Tac:
        logging.info("TacManager.add")
        self.session.add(tac)
        await self.session.flush()
        return tac
    def _build_query(self):
        logging.info("TacManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Pac, and_(Tac.pac_id == Pac.pac_id, Tac.pac_id != 0))
#
#         if join_condition is not None:
#             query = select(Tac
#                         ,Pac #pac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Tac)
        query = select(Tac
                    ,Pac #pac_id
                    )

        query = query.outerjoin(Pac, and_(Tac.pac_id == Pac.pac_id, Tac.pac_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[Tac]:
        logging.info("TacManager._run_query")
        tac_query_all = self._build_query()
        if query_filter is not None:
            query = tac_query_all.filter(query_filter)
        else:
            query = tac_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            tac = query_result_row[i]
            i = i + 1

            pac = query_result_row[i] #pac_id
            i = i + 1

            tac.pac_code_peek = pac.code if pac else uuid.UUID(int=0) #pac_id

            result.append(tac)
        return result
    def _first_or_none(self,tac_list:List) -> Tac:
        return tac_list[0] if tac_list else None
    async def get_by_id(self, tac_id: int) -> Optional[Tac]:
        logging.info("TacManager.get_by_id start tac_id:" + str(tac_id))
        if not isinstance(tac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
        # result = await self.session.execute(select(Tac).filter(Tac.tac_id == tac_id))
        # result = await self.session.execute(select(Tac).filter(Tac.tac_id == tac_id))
        # return result.scalars().first()
        query_filter = Tac.tac_id == tac_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Tac]:
        logging.info(f"TacManager.get_by_code {code}")
        # result = await self.session.execute(select(Tac).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Tac.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, tac: Tac, **kwargs) -> Optional[Tac]:
        logging.info("TacManager.update")
        if tac:
            for key, value in kwargs.items():
                setattr(tac, key, value)
            await self.session.flush()
        return tac
    async def delete(self, tac_id: int):
        logging.info(f"TacManager.delete {tac_id}")
        if not isinstance(tac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
        tac = await self.get_by_id(tac_id)
        if not tac:
            raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
        await self.session.delete(tac)
        await self.session.flush()
    async def get_list(self) -> List[Tac]:
        logging.info("TacManager.get_list")
        # result = await self.session.execute(select(Tac))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, tac:Tac) -> str:
        logging.info("TacManager.to_json")
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return json.dumps(tac_data)
    def to_dict(self, tac:Tac) -> dict:
        logging.info("TacManager.to_dict")
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return tac_data
    def from_json(self, json_str: str) -> Tac:
        logging.info("TacManager.from_json")
        """
        Deserialize a JSON string into a Tac object using the TacSchema.
        """
        schema = TacSchema()
        data = json.loads(json_str)
        tac_dict = schema.load(data)
        new_tac = Tac(**tac_dict)
        return new_tac
    def from_dict(self, tac_dict: str) -> Tac:
        logging.info("TacManager.from_dict")
        schema = TacSchema()
        tac_dict_converted = schema.load(tac_dict)
        new_tac = Tac(**tac_dict_converted)
        return new_tac
    async def add_bulk(self, tacs: List[Tac]) -> List[Tac]:
        logging.info("TacManager.add_bulk")
        """Add multiple tacs at once."""
        self.session.add_all(tacs)
        await self.session.flush()
        return tacs
    async def update_bulk(self, tac_updates: List[Dict[int, Dict]]) -> List[Tac]:
        logging.info("TacManager.update_bulk start")
        updated_tacs = []
        for update in tac_updates:
            tac_id = update.get("tac_id")
            if not isinstance(tac_id, int):
                raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
            if not tac_id:
                continue
            logging.info(f"TacManager.update_bulk tac_id:{tac_id}")
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
            for key, value in update.items():
                if key != "tac_id":
                    setattr(tac, key, value)
            updated_tacs.append(tac)
        await self.session.flush()
        logging.info("TacManager.update_bulk end")
        return updated_tacs
    async def delete_bulk(self, tac_ids: List[int]) -> bool:
        logging.info("TacManager.delete_bulk")
        """Delete multiple tacs by their IDs."""
        for tac_id in tac_ids:
            if not isinstance(tac_id, int):
                raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
            if tac:
                await self.session.delete(tac)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("TacManager.count")
        """Return the total number of tacs."""
        result = await self.session.execute(select(Tac))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Tac]:
        """Retrieve tacs sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Tac).order_by(getattr(Tac, sort_by).asc()))
        else:
            result = await self.session.execute(select(Tac).order_by(getattr(Tac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, tac: Tac) -> Tac:
        logging.info("TacManager.refresh")
        """Refresh the state of a given tac instance from the database."""
        await self.session.refresh(tac)
        return tac
    async def exists(self, tac_id: int) -> bool:
        logging.info(f"TacManager.exists {tac_id}")
        """Check if a tac with the given ID exists."""
        if not isinstance(tac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
        tac = await self.get_by_id(tac_id)
        return bool(tac)
    def is_equal(self, tac1:Tac, tac2:Tac) -> bool:
        if not tac1:
            raise TypeError("Tac1 required.")
        if not tac2:
            raise TypeError("Tac2 required.")
        if not isinstance(tac1, Tac):
            raise TypeError("The tac1 must be an Tac instance.")
        if not isinstance(tac2, Tac):
            raise TypeError("The tac2 must be an Tac instance.")
        dict1 = self.to_dict(tac1)
        dict2 = self.to_dict(tac2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Tac]: # PacID
        logging.info("TacManager.get_by_pac_id")
        if not isinstance(pac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(pac_id)} instead.")
        # result = await self.session.execute(select(Tac).filter(Tac.pac_id == pac_id))
        # return result.scalars().all()
        query_filter = Tac.pac_id == pac_id
        query_results = await self._run_query(query_filter)
        return query_results

