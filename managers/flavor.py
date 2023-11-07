import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pac import Pac # PacID
from models.flavor import Flavor
from models.serialization_schema.flavor import FlavorSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class FlavorNotFoundError(Exception):
    pass
class FlavorManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> Flavor:
        return Flavor(**kwargs)
    async def add(self, flavor: Flavor) -> Flavor:
        self.session.add(flavor)
        await self.session.commit()
        return flavor
    async def get_by_id(self, flavor_id: int) -> Optional[Flavor]:
        if not isinstance(flavor_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
        result = await self.session.execute(select(Flavor).filter(Flavor.flavor_id == flavor_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Flavor]:
        result = await self.session.execute(select(Flavor).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, flavor: Flavor, **kwargs) -> Optional[Flavor]:
        if flavor:
            for key, value in kwargs.items():
                setattr(flavor, key, value)
            await self.session.commit()
        return flavor
    async def delete(self, flavor_id: int):
        if not isinstance(flavor_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
        flavor = await self.get_by_id(flavor_id)
        if not flavor:
            raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
        await self.session.delete(flavor)
        await self.session.commit()
    async def get_list(self) -> List[Flavor]:
        result = await self.session.execute(select(Flavor))
        return result.scalars().all()
    def to_json(self, flavor:Flavor) -> str:
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return json.dumps(flavor_data)
    def to_dict(self, flavor:Flavor) -> dict:
        """
        Serialize the Flavor object to a JSON string using the FlavorSchema.
        """
        schema = FlavorSchema()
        flavor_data = schema.dump(flavor)
        return flavor_data
    def from_json(self, json_str: str) -> Flavor:
        """
        Deserialize a JSON string into a Flavor object using the FlavorSchema.
        """
        schema = FlavorSchema()
        data = json.loads(json_str)
        flavor_dict = schema.load(data)
        new_flavor = Flavor(**flavor_dict)
        return new_flavor
    def from_dict(self, flavor_dict: str) -> Flavor:
        schema = FlavorSchema()
        flavor_dict_converted = schema.load(flavor_dict)
        new_flavor = Flavor(**flavor_dict_converted)
        return new_flavor
    async def add_bulk(self, flavors: List[Flavor]) -> List[Flavor]:
        """Add multiple flavors at once."""
        self.session.add_all(flavors)
        await self.session.commit()
        return flavors
    async def update_bulk(self, flavor_updates: List[Dict[int, Dict]]) -> List[Flavor]:
        """Update multiple flavors at once."""
        updated_flavors = []
        for update in flavor_updates:
            flavor_id = update.get("flavor_id")
            if not isinstance(flavor_id, int):
                raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
            if not flavor_id:
                continue
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
            for key, value in update.items():
                if key != "flavor_id":
                    setattr(flavor, key, value)
            updated_flavors.append(flavor)
        await self.session.commit()
        return updated_flavors
    async def delete_bulk(self, flavor_ids: List[int]) -> bool:
        """Delete multiple flavors by their IDs."""
        for flavor_id in flavor_ids:
            if not isinstance(flavor_id, int):
                raise TypeError(f"The flavor_id must be an integer, got {type(flavor_id)} instead.")
            flavor = await self.get_by_id(flavor_id)
            if not flavor:
                raise FlavorNotFoundError(f"Flavor with ID {flavor_id} not found!")
            if flavor:
                await self.session.delete(flavor)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of flavors."""
        result = await self.session.execute(select(Flavor))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Flavor]:
        """Retrieve flavors sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Flavor).order_by(getattr(Flavor, sort_by).asc()))
        else:
            result = await self.session.execute(select(Flavor).order_by(getattr(Flavor, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, flavor: Flavor) -> Flavor:
        """Refresh the state of a given flavor instance from the database."""
        await self.session.refresh(flavor)
        return flavor
    async def exists(self, flavor_id: int) -> bool:
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
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_pac_id(self, pac_id: int) -> List[Pac]: # PacID
        if not isinstance(pac_id, int):
            raise TypeError(f"The flavor_id must be an integer, got {type(pac_id)} instead.")
        result = await self.session.execute(select(Flavor).filter(Flavor.pac_id == pac_id))
        return result.scalars().all()

