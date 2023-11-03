import json
import uuid
from typing import List, Optional, Dict 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.plant import Plant
from models.serialization_schema.plant import PlantSchema

class PlantNotFoundError(Exception):
    pass

class PlantManager:
    
    def __init__(self, session: AsyncSession):
        self.session = session 

    async def build(self, **kwargs) -> Plant:
        return Plant(**kwargs)  

    async def add(self, plant: Plant) -> Plant:
        self.session.add(plant)
        await self.session.commit()
        return plant

    async def get_by_id(self, plant_id: int) -> Optional[Plant]:
        if not isinstance(plant_id, int):
            raise TypeError(f"The plant_id must be an integer, got {type(plant_id)} instead.")
        result = await self.session.execute(select(Plant).filter(Plant.plant_id == plant_id))
        return result.scalars().first()

    async def get_by_code(self, code: uuid.UUID) -> Optional[Plant]:
        result = await self.session.execute(select(Plant).filter_by(code=code))
        return result.scalars().one_or_none()
    
    async def update(self, plant: Plant, **kwargs) -> Optional[Plant]:
        if plant:
            for key, value in kwargs.items():
                setattr(plant, key, value)
            await self.session.commit()
        return plant


    async def delete(self, plant_id: int):
        if not isinstance(plant_id, int):
            raise TypeError(f"The plant_id must be an integer, got {type(plant_id)} instead.")
        plant = await self.get_by_id(plant_id)
        if not plant:
            raise PlantNotFoundError(f"Plant with ID {plant_id} not found!") 
        
        await self.session.delete(plant)
        await self.session.commit() 



    async def get_list(self) -> List[Plant]:
        result = await self.session.execute(select(Plant))
        return result.scalars().all()
    
    def to_json(self, plant:Plant) -> str:
        """
        Serialize the Plant object to a JSON string using the PlantSchema.
        """ 
        schema = PlantSchema()
        plant_data = schema.dump(plant)
        return json.dumps(plant_data)
    
    
    
    def to_dict(self, plant:Plant) -> dict:
        """
        Serialize the Plant object to a JSON string using the PlantSchema.
        """ 
        schema = PlantSchema()
        plant_data = schema.dump(plant)
        return plant_data
        

    def from_json(self, json_str: str) -> Plant:
        """
        Deserialize a JSON string into a Plant object using the PlantSchema.
        """ 
        schema = PlantSchema()
        data = json.loads(json_str)
        plant_dict = schema.load(data)
    
        new_plant = Plant(**plant_dict) 

        return new_plant
    
    async def add_bulk(self, plants: List[Plant]) -> List[Plant]:
        """Add multiple plants at once.""" 
        self.session.add_all(plants) 
        await self.session.commit()
        return plants

    async def update_bulk(self, plant_updates: List[Dict[int, Dict]]) -> List[Plant]:
        """Update multiple plants at once."""
        updated_plants = []
        for update in plant_updates:
            plant_id = update.get("plant_id")
            if not isinstance(plant_id, int):
                raise TypeError(f"The plant_id must be an integer, got {type(plant_id)} instead.")
            if not plant_id:
                continue
            plant = await self.get_by_id(plant_id)
            if not plant:
                raise PlantNotFoundError(f"Plant with ID {plant_id} not found!")  
            for key, value in update.items():
                if key != "plant_id":
                    setattr(plant, key, value)
            updated_plants.append(plant)
        await self.session.commit()
        return updated_plants

    async def delete_bulk(self, plant_ids: List[int]) -> bool:
        """Delete multiple plants by their IDs."""
        for plant_id in plant_ids:
            if not isinstance(plant_id, int):
                raise TypeError(f"The plant_id must be an integer, got {type(plant_id)} instead.")
            plant = await self.get_by_id(plant_id)
            if not plant:
                raise PlantNotFoundError(f"Plant with ID {plant_id} not found!")  
            if plant:
                await self.session.delete(plant)
        await self.session.commit()
        return True

    async def count(self) -> int:
        """Return the total number of plants."""
        result = await self.session.execute(select(Plant))
        return len(result.scalars().all())

    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Plant]:
        """Retrieve plants sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Plant).order_by(getattr(Plant, sort_by).asc()))
        else:
            result = await self.session.execute(select(Plant).order_by(getattr(Plant, sort_by).desc()))
        return result.scalars().all()

    async def refresh(self, plant: Plant) -> Plant:
        """Refresh the state of a given plant instance from the database."""
        await self.session.refresh(plant)
        return plant

    async def exists(self, plant_id: int) -> bool:
        """Check if a plant with the given ID exists."""
        if not isinstance(plant_id, int):
            raise TypeError(f"The plant_id must be an integer, got {type(plant_id)} instead.")
        plant = await self.get_by_id(plant_id)
        return bool(plant)
    
#endset
    async def get_by_flvr_foreign_key_id(self, flvr_foreign_key_id: int): # FlvrForeignKeyID
        if not isinstance(flvr_foreign_key_id, int):
            raise TypeError(f"The plant_id must be an integer, got {type(flvr_foreign_key_id)} instead.")
        result = await self.session.execute(select(Plant).filter(Plant.flvr_foreign_key_id == flvr_foreign_key_id))
        return result.scalars().all()
    
    async def get_by_land_id(self, land_id: int): # LandID
        if not isinstance(land_id, int):
            raise TypeError(f"The plant_id must be an integer, got {type(land_id)} instead.")
        result = await self.session.execute(select(Plant).filter(Plant.land_id == land_id))
        return result.scalars().all()
#endset
