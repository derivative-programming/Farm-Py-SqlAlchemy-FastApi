import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.land import Land
from models.serialization_schema.land import LandSchema
class LandManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> Land:
        return Land(**kwargs)
    async def add(self, land: Land) -> Land:
        self.session.add(land)
        await self.session.commit()
        return land
    async def get_by_id(self, land_id: int) -> Optional[Land]:
        result = await self.session.execute(select(Land).filter(Land.land_id == land_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Land]:
        result = await self.session.execute(select(Land).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, land: Land, **kwargs) -> Optional[Land]:
        if land:
            for key, value in kwargs.items():
                setattr(land, key, value)
            await self.session.commit()
        return land
    async def delete(self, land_id: int) -> Optional[Land]:
        land = await self.get_by_id(land_id)
        if land:
            self.session.delete(land)
            await self.session.commit()
        return land
    async def get_list(self) -> List[Land]:
        result = await self.session.execute(select(Land))
        return result.scalars().all()
    def to_json(self, land:Land) -> str:
        """
        Serialize the Land object to a JSON string using the LandSchema.
        """
        schema = LandSchema()
        land_data = schema.dump(land)
        return json.dumps(land_data)
    def from_json(self, json_str: str) -> Land:
        """
        Deserialize a JSON string into a Land object using the LandSchema.
        """
        schema = LandSchema()
        data = json.loads(json_str)
        land_dict = schema.load(data)
        new_land = Land(**land_dict)
        return new_land
    async def add_bulk(self, lands_data: List[Dict]) -> List[Land]:
        """Add multiple lands at once."""
        lands = [Land(**data) for data in lands_data]
        self.session.add_all(lands)
        await self.session.commit()
        return lands
    async def update_bulk(self, land_updates: List[Dict[int, Dict]]) -> List[Land]:
        """Update multiple lands at once."""
        updated_lands = []
        for update in land_updates:
            land_id = update.get("land_id")
            if not land_id:
                continue
            land = await self.get_by_id(land_id)
            if not land:
                continue
            for key, value in update.items():
                if key != "land_id":
                    setattr(land, key, value)
            updated_lands.append(land)
        await self.session.commit()
        return updated_lands
    async def delete_bulk(self, land_ids: List[int]) -> bool:
        """Delete multiple lands by their IDs."""
        for land_id in land_ids:
            land = await self.get_by_id(land_id)
            if land:
                self.session.delete(land)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of lands."""
        result = await self.session.execute(select(Land))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Land]:
        """Retrieve lands sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Land).order_by(getattr(Land, sort_by).asc()))
        else:
            result = await self.session.execute(select(Land).order_by(getattr(Land, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, land: Land) -> Land:
        """Refresh the state of a given land instance from the database."""
        self.session.refresh(land)
        return land
    async def exists(self, land_id: int) -> bool:
        """Check if a land with the given ID exists."""
        land = await self.get_by_id(land_id)
        return bool(land)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(Land).filter(Land.pac_id == pac_id))
        return result.scalars().all()

