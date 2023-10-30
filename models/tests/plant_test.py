import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, Plant
from models.factory import PlantFactory
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
@pytest.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()
@pytest.fixture
async def session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    SessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session
@pytest.mark.asyncio
async def test_plant_creation(session):
    plant = await PlantFactory.create_async(session=session)
    assert plant.plant_id is not None
@pytest.mark.asyncio
async def test_code_default(session):
    plant = await PlantFactory.create_async(session=session)
    assert isinstance(plant.code, uuid.UUID)

@pytest.mark.asyncio
async def test_last_change_code_default_on_creation(session):
    plant = await PlantFactory.create_async(session=session) 
    assert isinstance(plant.last_change_code, uuid.UUID)

@pytest.mark.asyncio
async def test_last_change_code_default_on_update(session):
    plant = await PlantFactory.create_async(session=session) 
    initial_code = plant.last_change_code
    plant.code = uuid.uuid4()
    await session.commit()
    assert plant.last_change_code != initial_code
@pytest.mark.asyncio
async def test_date_inserted(session):
    plant = PlantFactory.build_async(session=session)
    assert plant.insert_utc_date_time is None 
    await session.commit()
    assert isinstance(plant.insert_utc_date_time, datetime)
@pytest.mark.asyncio
async def test_date_updated(session):
    plant = await PlantFactory.create_async(session=session) 

    initial_time = plant.last_update_utc_date_time

    plant.code = uuid.uuid4()
    await session.commit()
    assert plant.last_update_utc_date_time > initial_time
     
# @pytest.mark.asyncio
# async def test_string_length_limits(session):
#     long_string = "a" * 300
#     plant = PlantFactory(some_varchar_val=long_string, some_text_val=long_string)
#     session.add(plant)
#     # Adjust this for the specific DB limit exception you'd expect if these fields are too long
#     with pytest.raises(Exception):
#         await session.commit()
@pytest.mark.asyncio
async def test_model_deletion(session):
    plant = await PlantFactory.create_async(session=session)
    session.delete(plant)
    await session.commit()
    deleted_plant = await session.get(Plant, plant.plant_id)
    assert deleted_plant is None
@pytest.mark.asyncio
async def test_data_types(session):
    plant = await PlantFactory.create_async(session=session) 
    # Check the data types for each property
    assert isinstance(plant.plant_id, int)
    assert isinstance(plant.code, uuid.UUID)
    assert isinstance(plant.last_change_code, uuid.UUID)
    assert isinstance(plant.insert_user_id, uuid.UUID)
    assert isinstance(plant.last_update_user_id, uuid.UUID)
    assert isinstance(plant.flvr_foreign_key_id, int)
    assert isinstance(plant.is_delete_allowed, bool)
    assert isinstance(plant.is_edit_allowed, bool)
    assert isinstance(plant.land_id, int)
    assert plant.other_flavor == "" or isinstance(plant.other_flavor, str)
    assert isinstance(plant.some_big_int_val, int)
    assert isinstance(plant.some_bit_val, bool)
    assert isinstance(plant.some_date_val, datetime.datetime)
    assert isinstance(plant.some_decimal_val, (float, int))  # Numeric type can be float or int based on the value
    assert plant.some_email_address == "" or isinstance(plant.some_email_address, str)
    assert isinstance(plant.some_float_val, float)
    assert isinstance(plant.some_int_val, int)
    assert isinstance(plant.some_money_val, (float, int))  # Numeric type can be float or int based on the value
    assert plant.some_n_varchar_val == "" or isinstance(plant.some_n_varchar_val, str)
    assert plant.some_phone_number == "" or isinstance(plant.some_phone_number, str)
    assert plant.some_text_val == "" or isinstance(plant.some_text_val, str)
    assert isinstance(plant.some_uniqueidentifier_val, uuid.UUID)
    assert isinstance(plant.some_utc_date_time_val, datetime.datetime)
    assert plant.some_varchar_val == "" or isinstance(plant.some_varchar_val, str)
    # Check for the peek values, assuming they are UUIDs based on your model
    assert isinstance(plant.flvr_foreign_key_code_peek, uuid.UUID)
    assert isinstance(plant.land_code_peek, uuid.UUID)
    assert isinstance(plant.insert_utc_date_time, datetime.datetime)
    assert isinstance(plant.last_update_utc_date_time, datetime.datetime)
#endset

@pytest.mark.asyncio
async def test_unique_code_constraint(session):
    plant_1 = await PlantFactory.create_async(session=session)
    plant_2 = await PlantFactory.create_async(session=session)
    plant_2.code = plant_1.code  # Intentionally set the same code
    session.add_all([plant_1, plant_2])
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio
async def test_boolean_fields_default(session):
    plant = await PlantFactory.create_async(session=session)
    assert plant.code is not None
    assert plant.last_change_code is not None
    assert plant.insert_user_id is not None
    assert plant.last_update_user_id is not None
    assert plant.insert_utc_date_time is not None
    assert plant.last_update_utc_date_time is not None
    assert isinstance(plant.some_utc_date_time_val, datetime.datetime)
    assert plant.some_varchar_val == "" or isinstance(plant.some_varchar_val, str)
    assert isinstance(plant.flvr_foreign_key_code_peek, uuid.UUID) #FlvrForeignKeyID
    assert isinstance(plant.land_code_peek, uuid.UUID) #LandID

    assert plant.flvr_foreign_key_id > 0
    assert plant.is_delete_allowed == False
    assert plant.is_edit_allowed == False
    assert plant.land_id > 0
    assert plant.other_flavor == ""
    assert plant.some_big_int_val == 0
    assert plant.some_bit_val == False
    assert plant.some_date_val == datetime(1753, 1, 1)
    assert plant.some_decimal_val == 0
    assert plant.some_email_address == ""
    assert plant.some_float_val == 0.0
    assert plant.some_int_val == 0
    assert plant.some_money_val == 0
    assert plant.some_n_var_char_val == ""
    assert plant.some_phone_number == ""
    assert plant.some_text_val == ""
    assert isinstance(plant.some_uniqueidentifier_val, uuid.UUID)
    assert plant.some_utc_date_time_val == datetime(1753, 1, 1)
    assert plant.some_varchar_val == ""
#endset
@pytest.mark.asyncio
async def test_last_change_code_concurrency(session):
    # Step 1: Create a Plant instance and commit
    plant = await PlantFactory.create_async(session=session)
    # Store the original last_change_code
    original_last_change_code = plant.last_change_code
    # Step 2: Fetch the Plant instance in a new session and modify it
    session_1 = session  # Using the existing session
    plant_1 = await session_1.execute(select(Plant).filter_by(plant_id=plant.plant_id))
    plant_1 = plant_1.scalar_one()
    plant_1.code = uuid.uuid4() 
    await session_1.commit()
    # Step 3: Fetch the same Plant instance in another session and modify it
    session_2 = session  # Using the same session object, but it's a new transaction after commit
    plant_2 = await session_2.execute(select(Plant).filter_by(plant_id=plant.plant_id))
    plant_2 = plant_2.scalar_one()
    plant_2.code = uuid.uuid4()
    # Step 4: Commit changes in session_2 and check the last_change_code
    await session_2.commit()
    assert plant_2.last_change_code != original_last_change_code
@pytest.mark.asyncio #FlvrForeignKeyID
async def test_invalid_flvr_foreign_key_id(session):
    plant = await PlantFactory.create_async(session=session)
    plant.flvr_foreign_key_id=99999  
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
@pytest.mark.asyncio #LandID
async def test_invalid_land_id(session):
    plant = await PlantFactory.create_async(session=session)
    plant.land_id=99999   
    with pytest.raises(Exception):  # Adjust for the specific DB exception you'd expect
        await session.commit()
