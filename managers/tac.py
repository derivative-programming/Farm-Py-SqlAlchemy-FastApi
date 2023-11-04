import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tac import Tac
from models.serialization_schema.tac import TacSchema
class TacNotFoundError(Exception):
    pass
class TacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> Tac:
        return Tac(**kwargs)
    async def add(self, tac: Tac) -> Tac:
        self.session.add(tac)
        await self.session.commit()
        return tac
    async def get_by_id(self, tac_id: int) -> Optional[Tac]:
        if not isinstance(tac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
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
    async def delete(self, tac_id: int):
        if not isinstance(tac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
        tac = await self.get_by_id(tac_id)
        if not tac:
            raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
        await self.session.delete(tac)
        await self.session.commit()
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
    def to_dict(self, tac:Tac) -> dict:
        """
        Serialize the Tac object to a JSON string using the TacSchema.
        """
        schema = TacSchema()
        tac_data = schema.dump(tac)
        return tac_data
    def from_json(self, json_str: str) -> Tac:
        """
        Deserialize a JSON string into a Tac object using the TacSchema.
        """
        schema = TacSchema()
        data = json.loads(json_str)
        tac_dict = schema.load(data)
        new_tac = Tac(**tac_dict)
        return new_tac
    def from_dict(self, tac_dict: str) -> Tac:
        new_tac = Tac(**tac_dict)
        return new_tac
    async def add_bulk(self, tacs: List[Tac]) -> List[Tac]:
        """Add multiple tacs at once."""
        self.session.add_all(tacs)
        await self.session.commit()
        return tacs
    async def update_bulk(self, tac_updates: List[Dict[int, Dict]]) -> List[Tac]:
        """Update multiple tacs at once."""
        updated_tacs = []
        for update in tac_updates:
            tac_id = update.get("tac_id")
            if not isinstance(tac_id, int):
                raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
            if not tac_id:
                continue
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
            for key, value in update.items():
                if key != "tac_id":
                    setattr(tac, key, value)
            updated_tacs.append(tac)
        await self.session.commit()
        return updated_tacs
    async def delete_bulk(self, tac_ids: List[int]) -> bool:
        """Delete multiple tacs by their IDs."""
        for tac_id in tac_ids:
            if not isinstance(tac_id, int):
                raise TypeError(f"The tac_id must be an integer, got {type(tac_id)} instead.")
            tac = await self.get_by_id(tac_id)
            if not tac:
                raise TacNotFoundError(f"Tac with ID {tac_id} not found!")
            if tac:
                await self.session.delete(tac)
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
        await self.session.refresh(tac)
        return tac
    async def exists(self, tac_id: int) -> bool:
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

    async def get_by_pac_id(self, pac_id: int): # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The tac_id must be an integer, got {type(pac_id)} instead.")
        result = await self.session.execute(select(Tac).filter(Tac.pac_id == pac_id))
        return result.scalars().all()

