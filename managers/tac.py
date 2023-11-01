import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tac import Tac
from models.serialization_schema.tac import TacSchema
class TacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> Tac:
        return Tac(**kwargs)
    async def add(self, tac: Tac) -> Tac:
        self.session.add(tac)
        await self.session.commit()
        return tac
    async def get_by_id(self, tac_id: int) -> Optional[Tac]:
        result = await self.session.execute(select(Tac).filter(Tac.tac_id == tac_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Tac]:
        result = await self.session.execute(select(Tac).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, tac: Tac, **kwargs) -> Optional[Tac]:
        if tac:
            for key, value in kwargs.items():
                setattr(tac, key, value)
            await self.session.commit()
        return tac
    async def delete(self, tac_id: int) -> Optional[Tac]:
        tac = await self.get_by_id(tac_id)
        if tac:
            self.session.delete(tac)
            await self.session.commit()
        return tac
    async def get_list(self) -> List[Tac]:
        result = await self.session.execute(select(Tac))
        return result.scalars().all()
    def to_json(self, tac:Tac) -> str:
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return json.dumps(tac_data)
    def from_json(self, json_str: str) -> Tac:
        """
        Deserialize a JSON string into a Tac object using the TacSchema.
        """
        schema = TacSchema()
        data = json.loads(json_str)
        tac_dict = schema.load(data)
        new_tac = Tac(**tac_dict)
        return new_tac
    async def add_bulk(self, tacs_data: List[Dict]) -> List[Tac]:
        """Add multiple tacs at once."""
        tacs = [Tac(**data) for data in tacs_data]
        self.session.add_all(tacs)
        await self.session.commit()
        return tacs
    async def update_bulk(self, tac_updates: List[Dict[int, Dict]]) -> List[Tac]:
        """Update multiple tacs at once."""
        updated_tacs = []
        for update in tac_updates:
            tac_id = update.get("tac_id")
            if not tac_id:
                continue
            tac = await self.get_by_id(tac_id)
            if not tac:
                continue
            for key, value in update.items():
                if key != "tac_id":
                    setattr(tac, key, value)
            updated_tacs.append(tac)
        await self.session.commit()
        return updated_tacs
    async def delete_bulk(self, tac_ids: List[int]) -> bool:
        """Delete multiple tacs by their IDs."""
        for tac_id in tac_ids:
            tac = await self.get_by_id(tac_id)
            if tac:
                self.session.delete(tac)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of tacs."""
        result = await self.session.execute(select(Tac))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Tac]:
        """Retrieve tacs sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Tac).order_by(getattr(Tac, sort_by).asc()))
        else:
            result = await self.session.execute(select(Tac).order_by(getattr(Tac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, tac: Tac) -> Tac:
        """Refresh the state of a given tac instance from the database."""
        self.session.refresh(tac)
        return tac
    async def exists(self, tac_id: int) -> bool:
        """Check if a tac with the given ID exists."""
        tac = await self.get_by_id(tac_id)
        return bool(tac)

    async def get_by_pac_id(self, pac_id: int): # PacID
        result = await self.session.execute(select(Tac).filter(Tac.pac_id == pac_id))
        return result.scalars().all()

