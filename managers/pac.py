import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pac import Pac
from models.serialization_schema.pac import PacSchema
class PacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> Pac:
        return Pac(**kwargs)
    async def add(self, pac: Pac) -> Pac:
        self.session.add(pac)
        await self.session.commit()
        return pac
    async def get_by_id(self, pac_id: int) -> Optional[Pac]:
        result = await self.session.execute(select(Pac).filter(Pac.pac_id == pac_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Pac]:
        result = await self.session.execute(select(Pac).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, pac: Pac, **kwargs) -> Optional[Pac]:
        if pac:
            for key, value in kwargs.items():
                setattr(pac, key, value)
            await self.session.commit()
        return pac
    async def delete(self, pac_id: int) -> Optional[Pac]:
        pac = await self.get_by_id(pac_id)
        if pac:
            self.session.delete(pac)
            await self.session.commit()
        return pac
    async def get_list(self) -> List[Pac]:
        result = await self.session.execute(select(Pac))
        return result.scalars().all()
    def to_json(self, pac:Pac) -> str:
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return json.dumps(pac_data)
    def from_json(self, json_str: str) -> Pac:
        """
        Deserialize a JSON string into a Pac object using the PacSchema.
        """
        schema = PacSchema()
        data = json.loads(json_str)
        pac_dict = schema.load(data)
        new_pac = Pac(**pac_dict)
        return new_pac
    async def add_bulk(self, pacs_data: List[Dict]) -> List[Pac]:
        """Add multiple pacs at once."""
        pacs = [Pac(**data) for data in pacs_data]
        self.session.add_all(pacs)
        await self.session.commit()
        return pacs
    async def update_bulk(self, pac_updates: List[Dict[int, Dict]]) -> List[Pac]:
        """Update multiple pacs at once."""
        updated_pacs = []
        for update in pac_updates:
            pac_id = update.get("pac_id")
            if not pac_id:
                continue
            pac = await self.get_by_id(pac_id)
            if not pac:
                continue
            for key, value in update.items():
                if key != "pac_id":
                    setattr(pac, key, value)
            updated_pacs.append(pac)
        await self.session.commit()
        return updated_pacs
    async def delete_bulk(self, pac_ids: List[int]) -> bool:
        """Delete multiple pacs by their IDs."""
        for pac_id in pac_ids:
            pac = await self.get_by_id(pac_id)
            if pac:
                self.session.delete(pac)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of pacs."""
        result = await self.session.execute(select(Pac))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Pac]:
        """Retrieve pacs sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Pac).order_by(getattr(Pac, sort_by).asc()))
        else:
            result = await self.session.execute(select(Pac).order_by(getattr(Pac, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, pac: Pac) -> Pac:
        """Refresh the state of a given pac instance from the database."""
        self.session.refresh(pac)
        return pac
    async def exists(self, pac_id: int) -> bool:
        """Check if a pac with the given ID exists."""
        pac = await self.get_by_id(pac_id)
        return bool(pac)
