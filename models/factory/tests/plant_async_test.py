import asyncio
from decimal import Decimal
import pytest
import pytest_asyncio 
import time
from typing import AsyncGenerator
from decimal import Decimal
from datetime import datetime, date, timedelta
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import Base, Plant
from models.factory import PlantFactory
from services.db_config import db_dialect 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

db_dialect = "sqlite"

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
    
class TestPlantFactoryAsync:

    @pytest.fixture(scope="function")
    def event_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()


    @pytest.fixture(scope="function")
    def engine(self):
        engine = create_async_engine(DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose() 

    @pytest_asyncio.fixture(scope="function")
    async def session(self,engine) -> AsyncGenerator[AsyncSession, None]:
        
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            TestingSessionLocal = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with TestingSessionLocal(bind=connection) as session:
                @event.listens_for(
                    session.sync_session, "after_transaction_end"
                )
                def end_savepoint(session, transaction):
                    if connection.closed:
                        return

                    if not connection.in_nested_transaction():
                        connection.sync_connection.begin_nested()
                yield session
                await session.flush()
                await session.rollback()   
  
    @pytest.mark.asyncio
    async def test_plant_creation(self, session):
        plant = await PlantFactory.create_async(session=session)
        assert plant.plant_id is not None

    @pytest.mark.asyncio
    async def test_code_default(self, session):
        plant = await PlantFactory.create_async(session=session) 
        if db_dialect == 'postgresql': 
            assert isinstance(plant.code, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.code, str)

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        plant:Plant = await PlantFactory.build_async(session=session)
        assert plant.last_change_code == 0
        
    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        plant:Plant = await PlantFactory.create_async(session=session)
        assert plant.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        plant = await PlantFactory.create_async(session=session)
        initial_code = plant.last_change_code
        plant.code = generate_uuid()
        await session.commit()
        assert plant.last_change_code != initial_code

    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        plant = await PlantFactory.build_async(session=session)
        assert plant.insert_utc_date_time is not None 
        assert isinstance(plant.insert_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        plant = await PlantFactory.build_async(session=session)
        assert plant.insert_utc_date_time is not None 
        assert isinstance(plant.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        plant.code = generate_uuid()  
        await session.commit()
        assert plant.insert_utc_date_time > initial_time

    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        plant = await PlantFactory.create_async(session=session)
        assert plant.insert_utc_date_time is not None 
        assert isinstance(plant.insert_utc_date_time, datetime)
        initial_time = plant.insert_utc_date_time
        plant.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert plant.insert_utc_date_time == initial_time

        
    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        plant = await PlantFactory.build_async(session=session)
        assert plant.last_update_utc_date_time is not None 
        assert isinstance(plant.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        plant = await PlantFactory.build_async(session=session)
        assert plant.last_update_utc_date_time is not None 
        assert isinstance(plant.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        plant.code = generate_uuid() 
        await session.commit()
        assert plant.last_update_utc_date_time > initial_time 

    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        plant = await PlantFactory.create_async(session=session)
        assert plant.last_update_utc_date_time is not None 
        assert isinstance(plant.last_update_utc_date_time, datetime)
        initial_time = plant.last_update_utc_date_time
        plant.code = generate_uuid()
        time.sleep(1)
        await session.commit()
        assert plant.last_update_utc_date_time > initial_time 

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        plant = await PlantFactory.create_async(session=session)
        await session.delete(plant)
        await session.commit()

        
        # Construct the select statement
        stmt = select(Plant).where(Plant.plant_id==plant.plant_id)

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_plant = result.scalars().first()

        # deleted_plant = await session.query(Plant).filter_by(plant_id=plant.plant_id).first()
        assert deleted_plant is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        plant = await PlantFactory.create_async(session=session) 
        assert isinstance(plant.plant_id, int)
        if db_dialect == 'postgresql': 
            assert isinstance(plant.code, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.code, str)
            
        assert isinstance(plant.last_change_code, int) 

        if db_dialect == 'postgresql': 
            assert isinstance(plant.insert_user_id, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.insert_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.insert_user_id, str)
            
        if db_dialect == 'postgresql': 
            assert isinstance(plant.last_update_user_id, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.last_update_user_id, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.last_update_user_id, str)

        assert isinstance(plant.flvr_foreign_key_id, int)
        assert isinstance(plant.is_delete_allowed, bool)
        assert isinstance(plant.is_edit_allowed, bool)
        assert isinstance(plant.land_id, int)
        assert plant.other_flavor == "" or isinstance(plant.other_flavor, str)
        assert isinstance(plant.some_big_int_val, int)
        assert isinstance(plant.some_bit_val, bool)
        assert isinstance(plant.some_date_val, date)
        assert isinstance(plant.some_decimal_val, Decimal)  # Numeric type can be float or int based on the value
        assert plant.some_email_address == "" or isinstance(plant.some_email_address, str)
        assert isinstance(plant.some_float_val, float)
        assert isinstance(plant.some_int_val, int)
        assert isinstance(plant.some_money_val, Decimal)  # Numeric type can be float or int based on the value
        assert plant.some_n_var_char_val == "" or isinstance(plant.some_n_var_char_val, str)
        assert plant.some_phone_number == "" or isinstance(plant.some_phone_number, str)
        assert plant.some_text_val == "" or isinstance(plant.some_text_val, str) 
        #SomeUniqueidentifierVal
        if db_dialect == 'postgresql': 
            assert isinstance(plant.some_uniqueidentifier_val, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.some_uniqueidentifier_val, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.some_uniqueidentifier_val, str)
        assert isinstance(plant.some_utc_date_time_val, datetime)
        assert plant.some_var_char_val == "" or isinstance(plant.some_var_char_val, str)
        # Check for the peek values, assuming they are UUIDs based on your model
        
#endset   
    
        #isDeleteAllowed,
        #isEditAllowed,
        #otherFlavor, 
        #someBigIntVal,
        #someBitVal, 
        #someDecimalVal,
        #someEmailAddress,
        #someFloatVal,
        #someIntVal,
        #someMoneyVal,
        #someVarCharVal,
        #someDateVal
        #someUTCDateTimeVal 
        #flvrForeignKeyID
        if db_dialect == 'postgresql': 
            assert isinstance(plant.flvr_foreign_key_code_peek, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.flvr_foreign_key_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.flvr_foreign_key_code_peek, str)
        #landID
        if db_dialect == 'postgresql': 
            assert isinstance(plant.land_code_peek, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.land_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.land_code_peek, str)
        #someNVarCharVal, 
        #somePhoneNumber,
        #someTextVal,
        #someUniqueidentifierVal, 
        
#endset

        assert isinstance(plant.insert_utc_date_time, datetime)
        assert isinstance(plant.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        plant_1 = await PlantFactory.create_async(session=session)
        plant_2 = await PlantFactory.create_async(session=session)
        plant_2.code = plant_1.code
        session.add_all([plant_1, plant_2])
        with pytest.raises(Exception):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()

    @pytest.mark.asyncio
    async def test_fields_default(self, session):
        plant = Plant()
        assert plant.code is not None
        assert plant.last_change_code is not None
        assert plant.insert_user_id is None
        assert plant.last_update_user_id is None
        assert plant.insert_utc_date_time is not None
        assert plant.last_update_utc_date_time is not None

#endset
        #isDeleteAllowed,
        #isEditAllowed,
        #otherFlavor, 
        #someBigIntVal,
        #someBitVal, 
        #someDecimalVal,
        #someEmailAddress,
        #someFloatVal,
        #someIntVal,
        #someMoneyVal,
        #someNVarCharVal, 
        #someDateVal
        #someUTCDateTimeVal 
        #LandID
        if db_dialect == 'postgresql': 
            assert isinstance(plant.land_code_peek, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.land_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.land_code_peek, str)

        #FlvrForeignKeyID
        if db_dialect == 'postgresql': 
            assert isinstance(plant.flvr_foreign_key_code_peek, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.flvr_foreign_key_code_peek, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.flvr_foreign_key_code_peek, str)

        #somePhoneNumber,
        #someTextVal,
        #someUniqueidentifierVal, 
        #someVarCharVal,
#endset

        assert plant.flvr_foreign_key_id == 0
        assert plant.is_delete_allowed == False
        assert plant.is_edit_allowed == False
        assert plant.land_id == 0
        assert plant.other_flavor == ""
        assert plant.some_big_int_val == 0
        assert plant.some_bit_val == False
        assert plant.some_date_val == date(1753, 1, 1)
        assert plant.some_decimal_val == 0
        assert plant.some_email_address == ""
        assert plant.some_float_val == 0.0
        assert plant.some_int_val == 0
        assert plant.some_money_val == 0
        assert plant.some_n_var_char_val == ""
        assert plant.some_phone_number == ""
        assert plant.some_text_val == "" 
        #SomeUniqueIdentifierVal
        if db_dialect == 'postgresql': 
            assert isinstance(plant.some_uniqueidentifier_val, UUID)
        elif db_dialect == 'mssql': 
            assert isinstance(plant.some_uniqueidentifier_val, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases 
            assert isinstance(plant.some_uniqueidentifier_val, str)
        assert plant.some_utc_date_time_val == datetime(1753, 1, 1)
        assert plant.some_var_char_val == "" 
#endset


    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        plant = await PlantFactory.create_async(session=session)
        original_last_change_code = plant.last_change_code

        
        stmt = select(Plant).where(Plant.plant_id==plant.plant_id) 
        result = await session.execute(stmt) 
        plant_1 = result.scalars().first()

        # plant_1 = await session.query(Plant).filter_by(plant_id=plant.plant_id).first()
        plant_1.code = generate_uuid()
        await session.commit()
        
        stmt = select(Plant).where(Plant.plant_id==plant.plant_id) 
        result = await session.execute(stmt) 
        plant_2 = result.scalars().first()

        # plant_2 = await session.query(Plant).filter_by(plant_id=plant.plant_id).first()
        plant_2.code = generate_uuid()
        await session.commit()
        assert plant_2.last_change_code != original_last_change_code
#endset


    #isDeleteAllowed,
    #isEditAllowed,
    #otherFlavor, 
    #someBigIntVal,
    #someBitVal, 
    #someDecimalVal,
    #someEmailAddress,
    #someFloatVal,
    #someIntVal,
    #someMoneyVal,
    #someNVarCharVal, 
    #someDateVal
    #someUTCDateTimeVal 
    #LandID
    @pytest.mark.asyncio
    async def test_invalid_land_id(self, session):  
        plant = await PlantFactory.create_async(session=session)
        plant.land_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit() 
        await session.rollback()
    #FlvrForeignKeyID
    @pytest.mark.asyncio
    async def test_invalid_flvr_foreign_key_id(self, session):  
        plant = await PlantFactory.create_async(session=session)
        plant.flvr_foreign_key_id = 99999
        with pytest.raises(IntegrityError):  # adjust for the specific DB exception you'd expect
            await session.commit()
        await session.rollback()
    #somePhoneNumber,
    #someTextVal,
    #someUniqueidentifierVal, 
    #someVarCharVal,
#endset