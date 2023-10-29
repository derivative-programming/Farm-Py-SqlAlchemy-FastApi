from uuid import uuid4
from sqlalchemy.orm import Session
from managers.plant_manager import PlantManager

def create_plant(session: Session, land_id: int, flavor_id: int):
    plant_manager = PlantManager(session)
    plant = plant_manager.create(code=uuid4(), land_id=land_id, flavor_id=flavor_id)
    return plant
