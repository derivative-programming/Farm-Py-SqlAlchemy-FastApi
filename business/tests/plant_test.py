import pytest
import pytest_asyncio  
from datetime import datetime, date 
from sqlalchemy.ext.asyncio import AsyncSession
from models import Plant
from models.factory import PlantFactory
from managers.plant import PlantManager
from business.plant import PlantBusObj 
from services.db_config import db_dialect 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String 
from services.logging_config import get_logger
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

logger = get_logger(__name__) 

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
    
class TestPlantBusObj: 

    @pytest_asyncio.fixture(scope="function")
    async def plant_manager(self, session:AsyncSession):
        return PlantManager(session)
     
    @pytest_asyncio.fixture(scope="function")
    async def plant_bus_obj(self, session):
        # Assuming that the PlantBusObj requires a session object
        return PlantBusObj(session)

    @pytest_asyncio.fixture(scope="function")
    async def new_plant(self, session):
        # Use the PlantFactory to create a new plant instance
        # Assuming PlantFactory.create() is an async function
        return await PlantFactory.create_async(session)

    @pytest.mark.asyncio
    async def test_create_plant(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
        # Test creating a new plant 
        
        assert plant_bus_obj.plant_id is None

        # assert isinstance(plant_bus_obj.plant_id, int)
        if db_dialect == 'postgresql': 
            assert isinstance(plant_bus_obj.code, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant_bus_obj.code, str)
            
        assert isinstance(plant_bus_obj.last_change_code, int) 
 
        assert plant_bus_obj.insert_user_id is None
             
        assert plant_bus_obj.last_update_user_id is None

        assert isinstance(plant_bus_obj.flvr_foreign_key_id, int)
        assert isinstance(plant_bus_obj.is_delete_allowed, bool)
        assert isinstance(plant_bus_obj.is_edit_allowed, bool)
        assert isinstance(plant_bus_obj.land_id, int)
        assert plant_bus_obj.other_flavor == "" or isinstance(plant_bus_obj.other_flavor, str)
        assert isinstance(plant_bus_obj.some_big_int_val, int)
        assert isinstance(plant_bus_obj.some_bit_val, bool)
        assert isinstance(plant_bus_obj.some_date_val, date)
        assert isinstance(plant_bus_obj.some_decimal_val, int or float)  # Numeric type can be float or int based on the value
        assert plant_bus_obj.some_email_address == "" or isinstance(plant_bus_obj.some_email_address, str)
        assert isinstance(plant_bus_obj.some_float_val, float)
        assert isinstance(plant_bus_obj.some_int_val, int)
        assert isinstance(plant_bus_obj.some_money_val, int or float)  # Numeric type can be float or int based on the value
        assert plant_bus_obj.some_n_var_char_val == "" or isinstance(plant_bus_obj.some_n_var_char_val, str)
        assert plant_bus_obj.some_phone_number == "" or isinstance(plant_bus_obj.some_phone_number, str)
        assert plant_bus_obj.some_text_val == "" or isinstance(plant_bus_obj.some_text_val, str) 
        #SomeUniqueidentifierVal
        if db_dialect == 'postgresql': 
            assert isinstance(plant_bus_obj.some_uniqueidentifier_val, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant_bus_obj.some_uniqueidentifier_val, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant_bus_obj.some_uniqueidentifier_val, str)
        assert isinstance(plant_bus_obj.some_utc_date_time_val, datetime)
        assert plant_bus_obj.some_var_char_val == "" or isinstance(plant_bus_obj.some_var_char_val, str)

    @pytest.mark.asyncio
    async def test_load_with_plant_obj(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
         
        await plant_bus_obj.load(plant_obj_instance=new_plant) 
        
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant) == True
 
        
    @pytest.mark.asyncio
    async def test_load_with_plant_id(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
         
        await plant_bus_obj.load(plant_id=new_plant.plant_id)
        
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant)  == True
        
    @pytest.mark.asyncio
    async def test_load_with_plant_code(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
         
        await plant_bus_obj.load(code=new_plant.code)
        
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant)  == True
        
    @pytest.mark.asyncio
    async def test_load_with_plant_json(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
         
        plant_json = plant_manager.to_json(new_plant)

        await plant_bus_obj.load(json_data=plant_json)
        
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant)  == True
 
    @pytest.mark.asyncio
    async def test_load_with_plant_dict(self, session, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
         
        logger.info("test_load_with_plant_dict 1") 
           
        plant_dict = plant_manager.to_dict(new_plant)

        logger.info(plant_dict)

        await plant_bus_obj.load(plant_dict=plant_dict) 
        
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant)  == True

    @pytest.mark.asyncio
    async def test_get_nonexistent_plant(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
        # Test retrieving a nonexistent plant raises an exception
        assert await plant_bus_obj.load(plant_id=-1) is None # Assuming -1 is an id that wouldn't exist

    @pytest.mark.asyncio
    async def test_update_plant(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
        # Test updating a plant's data  

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)
          
        new_code = generate_uuid() 

        await plant_bus_obj.load(plant_obj_instance=new_plant) 
 
        plant_bus_obj.code = new_code

        await plant_bus_obj.save()

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)
         
        assert plant_manager.is_equal(plant_bus_obj.plant,new_plant)  == True

    @pytest.mark.asyncio
    async def test_delete_plant(self, plant_manager:PlantManager, plant_bus_obj:PlantBusObj, new_plant:Plant):
        
        assert new_plant.plant_id is not None
        
        assert plant_bus_obj.plant_id is None

        await plant_bus_obj.load(plant_id=new_plant.plant_id) 
        
        assert plant_bus_obj.plant_id is not None
        

        await plant_bus_obj.delete()

        new_plant = await plant_manager.get_by_id(new_plant.plant_id)

        assert new_plant is None 
 

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]