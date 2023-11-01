import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import PlantManager, Plant
from models.factory import PlantFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Plant

DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"

class TestPlantManager:
    @pytest.fixture(scope="module") 
    def engine(self):
        engine = create_engine(DATABASE_URL, echo=True)
        #FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.connection.execute("PRAGMA foreign_keys=ON")
        yield engine
        engine.dispose()
    @pytest.fixture
    def session(self, engine):
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()

    @pytest.fixture
    async def plant_manager(self, session):
        return PlantManager(session)
     
    @pytest.mark.asyncio
    async def test_build(self, plant_manager):
        # Define some mock data for our plant
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }

        # Call the build function of the manager
        plant = await plant_manager.build(**mock_data)

        # Assert that the returned object is an instance of Plant
        assert isinstance(plant, Plant)

        # Assert that the attributes of the plant match our mock data
        assert plant.name == mock_data["name"]
        assert plant.species == mock_data["species"]
        assert plant.age == mock_data["age"]

        # Optionally, if the build method has some default values or computations:
        # assert plant.some_attribute == some_expected_value

    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, plant_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }

        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await plant_manager.build(**mock_data)

    @pytest.mark.asyncio
    async def test_add(self, plant_manager, mock_session):
        plant_data = PlantFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        plant = await plant_manager.add(**plant_data)
        
        mock_session.add.assert_called_once_with(plant)
        mock_session.commit.assert_called_once()
        assert isinstance(plant, Plant)

    
    @pytest.mark.asyncio
    async def test_add_correctly_adds_plant_to_database(self, plant_manager, db_session):
        # Create a test plant using the PlantFactory without persisting it to the database
        test_plant = PlantFactory.build()
        
        # Add the plant using the manager's add method
        added_plant = await plant_manager.add(plant=test_plant)

        # Fetch the plant from the database directly
        result = await db_session.execute(select(Plant).filter(Plant.plant_id == added_plant.plant_id))
        fetched_plant = result.scalars().first()

        # Assert that the fetched plant is not None and matches the added plant
        assert fetched_plant is not None
        assert fetched_plant.plant_id == added_plant.plant_id
        assert fetched_plant.name == added_plant.name
        # ... other attribute checks ...

    @pytest.mark.asyncio
    async def test_add_returns_correct_plant_object(self, plant_manager):
        # Create a test plant using the PlantFactory without persisting it to the database
        test_plant = PlantFactory.build()
        
        # Add the plant using the manager's add method
        added_plant = await plant_manager.add(plant=test_plant)

        # Assert that the returned plant matches the test plant
        assert added_plant.plant_id == test_plant.plant_id
        assert added_plant.name == test_plant.name
        # ... other attribute checks ...

    @pytest.mark.asyncio
    async def test_get_by_id(self, plant_manager, mock_session):
        plant_data = PlantFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=plant_data)))

        plant = await plant_manager.get_by_id(1)

        mock_session.execute.assert_called_once()
        assert isinstance(plant, Plant)

    
    async def test_get_by_id(self, session: AsyncSession, sample_plant: Plant):
        manager = PlantManager(session)
        retrieved_plant = await manager.get_by_id(sample_plant.plant_id)
        
        assert retrieved_plant is not None
        assert retrieved_plant.plant_id == sample_plant.plant_id
        assert retrieved_plant.name == "Rose"
        assert retrieved_plant.color == "Red"
    
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = PlantManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_plant = await manager.get_by_id(non_existent_id)
        
        assert retrieved_plant is None

    @pytest.mark.asyncio
    async def test_get_by_code_returns_plant(self, plant_manager, db_session):
        # Use your PlantFactory to create and save a Plant object
        code = uuid.uuid4()
        plant = PlantFactory(code=code)
        db_session.add(plant)
        await db_session.commit()

        # Fetch the plant using the manager's get_by_code method
        fetched_plant = await plant_manager.get_by_code(code)

        # Assert that the fetched plant is not None and has the expected code
        assert fetched_plant is not None
        assert fetched_plant.code == code

    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, plant_manager):
        # Generate a random UUID that doesn't correspond to any Plant in the database
        random_code = uuid.uuid4()

        # Try fetching a plant using the manager's get_by_code method
        fetched_plant = await plant_manager.get_by_code(random_code)

        # Assert that the result is None since no plant with the given code exists
        assert fetched_plant is None

    @pytest.mark.asyncio
    async def test_update(self, plant_manager, mock_session):
        plant_data = PlantFactory.build()
        updated_data = {"name": "Updated Plant"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=plant_data)))
        mock_session.commit.return_value = None

        updated_plant = await plant_manager.update(1, **updated_data)

        assert updated_plant.name == "Updated Plant"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_plant, Plant)
    
    
    async def test_update_valid_plant(self):
        # Mocking a plant instance
        plant = Plant(plant_id=1, name="Rose", code="ROSE123")
        
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()

        # Update the plant with new attributes
        updated_plant = await self.manager.update(plant, name="Red Rose", code="REDROSE123")

        # Assertions
        assert updated_plant.name == "Red Rose"
        assert updated_plant.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()

    async def test_update_invalid_plant(self):
        # None plant
        plant = None
        
        updated_plant = await self.manager.update(plant, name="Red Rose", code="REDROSE123")

        # Assertions
        assert updated_plant is None
        self.session_mock.commit.assert_not_called()

    async def test_update_with_nonexistent_attribute(self):
        # Mocking a plant instance
        plant = Plant(plant_id=1, name="Rose", code="ROSE123")
        
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()

        # This should raise an AttributeError since 'color' is not an attribute of Plant
        with pytest.raises(AttributeError):
            await self.manager.update(plant, color="Red")
        
        self.session_mock.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete(self, plant_manager, mock_session):
        plant_data = PlantFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=plant_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        deleted_plant = await plant_manager.delete(1)

        mock_session.delete.assert_called_once_with(deleted_plant)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_plant, Plant) 

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, plant_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))

        with pytest.raises(ValueError, match="Plant not found"):
            await plant_manager.delete(999)


    @pytest.mark.asyncio
    async def test_get_list(self, plant_manager, mock_session):
        plants_data = [PlantFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=plants_data)))

        plants = await plant_manager.get_list()

        mock_session.execute.assert_called_once()
        assert len(plants) == 5
        assert all(isinstance(plant, Plant) for plant in plants)

    @pytest.mark.asyncio
    async def test_to_json(self, plant_manager):
        plant_data = PlantFactory.build()
        plant = Plant(**plant_data)
        json_data = plant_manager.to_json(plant)
        
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure

    @pytest.mark.asyncio
    async def test_from_json(self, plant_manager):
        plant_data = PlantFactory.build()
        plant = Plant(**plant_data)
        json_data = plant_manager.to_json(plant)
        
        deserialized_plant = plant_manager.from_json(json_data)
        assert isinstance(deserialized_plant, Plant)
        # Additional checks on the deserialized data can be added

    @pytest.mark.asyncio
    async def test_add_bulk(self, plant_manager, mock_session):
        plants_data = [PlantFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None

        plants = await plant_manager.add_bulk(plants_data)

        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(plants) == 5

    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = PlantManager()
        session_mock = AsyncMock()
        manager.session = session_mock

        # Mocking plant instances
        plant1 = Plant(plant_id=1, name="Rose", code="ROSE123")
        plant2 = Plant(plant_id=2, name="Tulip", code="TULIP123")

        # Mocking the get_by_id method to return the corresponding plant
        async def mock_get_by_id(plant_id):
            if plant_id == 1:
                return plant1
            if plant_id == 2:
                return plant2
        manager.get_by_id = mock_get_by_id

        # Mocking the commit method
        session_mock.commit = AsyncMock()

        # Update plants
        updates = [{"plant_id": 1, "name": "Red Rose"}, {"plant_id": 2, "name": "Yellow Tulip"}]
        updated_plants = await manager.update_bulk(updates)

        # Assertions
        assert len(updated_plants) == 2
        assert updated_plants[0].name == "Red Rose"
        assert updated_plants[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_bulk_missing_plant_id():
        manager = PlantManager()

        # No plants to update since plant_id is missing
        updates = [{"name": "Red Rose"}]
        updated_plants = await manager.update_bulk(updates)

        # Assertions
        assert len(updated_plants) == 0

    @pytest.mark.asyncio
    async def test_update_bulk_plant_not_found():
        manager = PlantManager()
        session_mock = AsyncMock()
        manager.session = session_mock

        # Mocking the get_by_id method to return None (plant not found)
        manager.get_by_id = AsyncMock(return_value=None)

        # Mocking the commit method
        session_mock.commit = AsyncMock()

        # Update plants
        updates = [{"plant_id": 1, "name": "Red Rose"}]
        updated_plants = await manager.update_bulk(updates)

        # Assertions
        assert len(updated_plants) == 0
        session_mock.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = PlantManager()
        session_mock = AsyncMock()
        manager.session = session_mock

        # Mocking plant instances
        plant1 = Plant(plant_id=1, name="Rose", code="ROSE123")
        plant2 = Plant(plant_id=2, name="Tulip", code="TULIP123")

        # Mocking the get_by_id method to return the corresponding plant
        async def mock_get_by_id(plant_id):
            if plant_id == 1:
                return plant1
            if plant_id == 2:
                return plant2
        manager.get_by_id = mock_get_by_id

        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()

        # Delete plants
        plant_ids = [1, 2]
        result = await manager.delete_bulk(plant_ids)

        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_bulk_some_plants_not_found():
        manager = PlantManager()
        session_mock = AsyncMock()
        manager.session = session_mock

        # Mocking the get_by_id method to return None (plant not found)
        async def mock_get_by_id(plant_id):
            if plant_id == 1:
                return None
            if plant_id == 2:
                return Plant(plant_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id

        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()

        # Delete plants
        plant_ids = [1, 2]
        result = await manager.delete_bulk(plant_ids)

        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Plant(plant_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = PlantManager()
        session_mock = AsyncMock()
        manager.session = session_mock

        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()

        # Delete plants with an empty list
        plant_ids = []
        result = await manager.delete_bulk(plant_ids)

        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_count(self, plant_manager, mock_session):
        plants_data = [PlantFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=plants_data)))

        count = await plant_manager.count()

        mock_session.execute.assert_called_once()
        assert count == 5

        
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a plant
        new_plant = Plant()
        async_session.add(new_plant)
        await async_session.commit()

        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 1

    @pytest.mark.asyncio
    async def test_count_empty_database(async_session):
        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 0

    @pytest.mark.asyncio
    async def test_count_multiple_additions(async_session):
        # Add multiple plants
        plants = [Plant() for _ in range(5)]
        async_session.add_all(plants)
        await async_session.commit()

        manager = YourManagerClass(session=async_session)
        count = await manager.count()
        assert count == 5

    @pytest.mark.asyncio
    async def test_count_database_connection_issues(async_session, mocker):
        # Mock the session's execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))

        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.count()

    
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(async_session):
        # Add plants
        plants = [Plant(name=f"Plant_{i}") for i in range(5)]
        async_session.add_all(plants)
        await async_session.commit()

        manager = YourManagerClass(session=async_session)
        sorted_plants = await manager.get_sorted_list(sort_by="name")
        assert [plant.name for plant in sorted_plants] == [f"Plant_{i}" for i in range(5)]

    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add plants
        plants = [Plant(name=f"Plant_{i}") for i in range(5)]
        async_session.add_all(plants)
        await async_session.commit()

        manager = YourManagerClass(session=async_session)
        sorted_plants = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [plant.name for plant in sorted_plants] == [f"Plant_{i}" for i in reversed(range(5))]

    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(async_session):
        manager = YourManagerClass(session=async_session)
        with pytest.raises(AttributeError):
            await manager.get_sorted_list(sort_by="invalid_attribute")

    @pytest.mark.asyncio
    async def test_get_sorted_list_database_connection_issues(async_session, mocker):
        # Mock the session's execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))

        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_sorted_list(sort_by="name")

    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(async_session):
        manager = YourManagerClass(session=async_session)
        sorted_plants = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_plants) == 0

    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a plant
        plant = Plant(name="Plant_1")
        async_session.add(plant)
        await async_session.commit()

        # Modify the plant directly in the database
        await async_session.execute('UPDATE plants SET name = :new_name WHERE id = :plant_id', {"new_name": "Modified_Plant", "plant_id": plant.id})
        await async_session.commit()

        # Now, refresh the plant using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_plant = await manager.refresh(plant)
        assert refreshed_plant.name == "Modified_Plant"

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_plant(async_session):
        plant = Plant(id=999, name="Nonexistent_Plant")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(plant)

    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))

        plant = Plant(name="Plant_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(plant)

    @pytest.mark.asyncio
    async def test_exists_with_existing_plant(async_session):
        # Add a plant
        plant = Plant(name="Plant_1")
        async_session.add(plant)
        await async_session.commit()

        # Check if the plant exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(plant.id) == True

    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_plant(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(non_existent_id) == False

    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.exists(invalid_id)

    @pytest.mark.asyncio
    async def test_exists_database_connection_issues(async_session, mocker):
        # Mock the get_by_id method to simulate a database connection error
        mocker.patch.object(YourManagerClass, 'get_by_id', side_effect=Exception("DB connection error"))

        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.exists(1)

    #get_by_flvr_foreign_key_id
    

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_existing(async_session):
        # Add a plant with a specific flvr_foreign_key_id
        plant = Plant(name="Plant_1", flvr_foreign_key_id=5)
        async_session.add(plant)
        await async_session.commit()

        # Fetch the plant using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_plants = await manager.get_by_flvr_foreign_key_id(5)
        assert len(fetched_plants) == 1
        assert fetched_plants[0].name == "Plant_1"

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_plants = await manager.get_by_flvr_foreign_key_id(non_existent_id)
        assert len(fetched_plants) == 0

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_flvr_foreign_key_id(invalid_id)

    @pytest.mark.asyncio
    async def test_get_by_flvr_foreign_key_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))

        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_flvr_foreign_key_id(1)


    #get_by_land_id
    

    @pytest.mark.asyncio
    async def test_get_by_land_id_existing(async_session):
        # Add a plant with a specific land_id
        plant = Plant(name="Plant_1", land_id=5)
        async_session.add(plant)
        await async_session.commit()

        # Fetch the plant using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_plants = await manager.get_by_land_id(5)
        assert len(fetched_plants) == 1
        assert fetched_plants[0].name == "Plant_1"

    @pytest.mark.asyncio
    async def test_get_by_land_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_plants = await manager.get_by_land_id(non_existent_id)
        assert len(fetched_plants) == 0

    @pytest.mark.asyncio
    async def test_get_by_land_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_land_id(invalid_id)

    @pytest.mark.asyncio
    async def test_get_by_land_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))

        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_land_id(1)
