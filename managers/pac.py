import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.pac import Pac
from models.serialization_schema.pac import PacSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class PacNotFoundError(Exception):
    pass
class PacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> Pac:
        return Pac(**kwargs)
    async def add(self, pac: Pac) -> Pac:
        self.session.add(pac)
        await self.session.commit()
        return pac
    async def get_by_id(self, pac_id: int) -> Optional[Pac]:
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
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
    async def delete(self, pac_id: int):
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
        pac = await self.get_by_id(pac_id)
        if not pac:
            raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
        await self.session.delete(pac)
        await self.session.commit()
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
    def to_dict(self, pac:Pac) -> dict:
        """
        Serialize the Pac object to a JSON string using the PacSchema.
        """
        schema = PacSchema()
        pac_data = schema.dump(pac)
        return pac_data
    def from_json(self, json_str: str) -> Pac:
        """
        Deserialize a JSON string into a Pac object using the PacSchema.
        """
        schema = PacSchema()
        data = json.loads(json_str)
        pac_dict = schema.load(data)
        new_pac = Pac(**pac_dict)
        return new_pac
    def from_dict(self, pac_dict: str) -> Pac:
        schema = PacSchema()
        pac_dict_converted = schema.load(pac_dict)
        new_pac = Pac(**pac_dict_converted)
        return new_pac
    async def add_bulk(self, pacs: List[Pac]) -> List[Pac]:
        """Add multiple pacs at once."""
        self.session.add_all(pacs)
        await self.session.commit()
        return pacs
    async def update_bulk(self, pac_updates: List[Dict[int, Dict]]) -> List[Pac]:
        """Update multiple pacs at once."""
        updated_pacs = []
        for update in pac_updates:
            pac_id = update.get("pac_id")
            if not isinstance(pac_id, int):
                raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
            if not pac_id:
                continue
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
            for key, value in update.items():
                if key != "pac_id":
                    setattr(pac, key, value)
            updated_pacs.append(pac)
        await self.session.commit()
        return updated_pacs
    async def delete_bulk(self, pac_ids: List[int]) -> bool:
        """Delete multiple pacs by their IDs."""
        for pac_id in pac_ids:
            if not isinstance(pac_id, int):
                raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
            pac = await self.get_by_id(pac_id)
            if not pac:
                raise PacNotFoundError(f"Pac with ID {pac_id} not found!")
            if pac:
                await self.session.delete(pac)
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
        await self.session.refresh(pac)
        return pac
    async def exists(self, pac_id: int) -> bool:
        """Check if a pac with the given ID exists."""
        if not isinstance(pac_id, int):
            raise TypeError(f"The pac_id must be an integer, got {type(pac_id)} instead.")
        pac = await self.get_by_id(pac_id)
        return bool(pac)
    def is_equal(self, pac1:Pac, pac2:Pac) -> bool:
        if not pac1:
            raise TypeError("Pac1 required.")
        if not pac2:
            raise TypeError("Pac2 required.")
        if not isinstance(pac1, Pac):
            raise TypeError("The pac1 must be an Pac instance.")
        if not isinstance(pac2, Pac):
            raise TypeError("The pac2 must be an Pac instance.")
        dict1 = self.to_dict(pac1)
        dict2 = self.to_dict(pac2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

