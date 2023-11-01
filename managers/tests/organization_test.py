import pytest
import uuid
from unittest.mock import AsyncMock, patch
from managers import OrganizationManager, Organization
from models.factory import OrganizationFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Organization
DATABASE_URL = "sqlite:///:memory:"
db_dialect = "sqlite"
class TestOrganizationManager:
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
    async def organization_manager(self, session):
        return OrganizationManager(session)
    @pytest.mark.asyncio
    async def test_build(self, organization_manager):
        # Define some mock data for our organization
        mock_data = {
            "name": "Rose",
            "species": "Rosa",
            "age": 2
        }
        # Call the build function of the manager
        organization = await organization_manager.build(**mock_data)
        # Assert that the returned object is an instance of Organization
        assert isinstance(organization, Organization)
        # Assert that the attributes of the organization match our mock data
        assert organization.name == mock_data["name"]
        assert organization.species == mock_data["species"]
        assert organization.age == mock_data["age"]
        # Optionally, if the build method has some default values or computations:
        # assert organization.some_attribute == some_expected_value
    @pytest.mark.asyncio
    async def test_build_with_missing_data(self, organization_manager):
        # Define mock data with a missing key
        mock_data = {
            "name": "Rose",
            "age": 2
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(SomeSpecificException):
            await organization_manager.build(**mock_data)
    @pytest.mark.asyncio
    async def test_add(self, organization_manager, mock_session):
        organization_data = OrganizationFactory.build()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        organization = await organization_manager.add(**organization_data)
        mock_session.add.assert_called_once_with(organization)
        mock_session.commit.assert_called_once()
        assert isinstance(organization, Organization)
    @pytest.mark.asyncio
    async def test_add_correctly_adds_organization_to_database(self, organization_manager, db_session):
        # Create a test organization using the OrganizationFactory without persisting it to the database
        test_organization = OrganizationFactory.build()
        # Add the organization using the manager's add method
        added_organization = await organization_manager.add(organization=test_organization)
        # Fetch the organization from the database directly
        result = await db_session.execute(select(Organization).filter(Organization.organization_id == added_organization.organization_id))
        fetched_organization = result.scalars().first()
        # Assert that the fetched organization is not None and matches the added organization
        assert fetched_organization is not None
        assert fetched_organization.organization_id == added_organization.organization_id
        assert fetched_organization.name == added_organization.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_add_returns_correct_organization_object(self, organization_manager):
        # Create a test organization using the OrganizationFactory without persisting it to the database
        test_organization = OrganizationFactory.build()
        # Add the organization using the manager's add method
        added_organization = await organization_manager.add(organization=test_organization)
        # Assert that the returned organization matches the test organization
        assert added_organization.organization_id == test_organization.organization_id
        assert added_organization.name == test_organization.name
        # ... other attribute checks ...
    @pytest.mark.asyncio
    async def test_get_by_id(self, organization_manager, mock_session):
        organization_data = OrganizationFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=organization_data)))
        organization = await organization_manager.get_by_id(1)
        mock_session.execute.assert_called_once()
        assert isinstance(organization, Organization)
    async def test_get_by_id(self, session: AsyncSession, sample_organization: Organization):
        manager = OrganizationManager(session)
        retrieved_organization = await manager.get_by_id(sample_organization.organization_id)
        assert retrieved_organization is not None
        assert retrieved_organization.organization_id == sample_organization.organization_id
        assert retrieved_organization.name == "Rose"
        assert retrieved_organization.color == "Red"
    async def test_get_by_id_not_found(self, session: AsyncSession):
        manager = OrganizationManager(session)
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_organization = await manager.get_by_id(non_existent_id)
        assert retrieved_organization is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_organization(self, organization_manager, db_session):
        # Use your OrganizationFactory to create and save a Organization object
        code = uuid.uuid4()
        organization = OrganizationFactory(code=code)
        db_session.add(organization)
        await db_session.commit()
        # Fetch the organization using the manager's get_by_code method
        fetched_organization = await organization_manager.get_by_code(code)
        # Assert that the fetched organization is not None and has the expected code
        assert fetched_organization is not None
        assert fetched_organization.code == code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(self, organization_manager):
        # Generate a random UUID that doesn't correspond to any Organization in the database
        random_code = uuid.uuid4()
        # Try fetching a organization using the manager's get_by_code method
        fetched_organization = await organization_manager.get_by_code(random_code)
        # Assert that the result is None since no organization with the given code exists
        assert fetched_organization is None
    @pytest.mark.asyncio
    async def test_update(self, organization_manager, mock_session):
        organization_data = OrganizationFactory.build()
        updated_data = {"name": "Updated Organization"}
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=organization_data)))
        mock_session.commit.return_value = None
        updated_organization = await organization_manager.update(1, **updated_data)
        assert updated_organization.name == "Updated Organization"
        mock_session.commit.assert_called_once()
        assert isinstance(updated_organization, Organization)
    async def test_update_valid_organization(self):
        # Mocking a organization instance
        organization = Organization(organization_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # Update the organization with new attributes
        updated_organization = await self.manager.update(organization, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_organization.name == "Red Rose"
        assert updated_organization.code == "REDROSE123"
        self.session_mock.commit.assert_called_once()
    async def test_update_invalid_organization(self):
        # None organization
        organization = None
        updated_organization = await self.manager.update(organization, name="Red Rose", code="REDROSE123")
        # Assertions
        assert updated_organization is None
        self.session_mock.commit.assert_not_called()
    async def test_update_with_nonexistent_attribute(self):
        # Mocking a organization instance
        organization = Organization(organization_id=1, name="Rose", code="ROSE123")
        # Mocking the commit method
        self.session_mock.commit = AsyncMock()
        # This should raise an AttributeError since 'color' is not an attribute of Organization
        with pytest.raises(AttributeError):
            await self.manager.update(organization, color="Red")
        self.session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete(self, organization_manager, mock_session):
        organization_data = OrganizationFactory.build()
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=organization_data)))
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None
        deleted_organization = await organization_manager.delete(1)
        mock_session.delete.assert_called_once_with(deleted_organization)
        mock_session.commit.assert_called_once()
        assert isinstance(deleted_organization, Organization)
    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, organization_manager, mock_session):
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(first=AsyncMock(return_value=None)))
        with pytest.raises(ValueError, match="Organization not found"):
            await organization_manager.delete(999)
    @pytest.mark.asyncio
    async def test_get_list(self, organization_manager, mock_session):
        organizations_data = [OrganizationFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=organizations_data)))
        organizations = await organization_manager.get_list()
        mock_session.execute.assert_called_once()
        assert len(organizations) == 5
        assert all(isinstance(organization, Organization) for organization in organizations)
    @pytest.mark.asyncio
    async def test_to_json(self, organization_manager):
        organization_data = OrganizationFactory.build()
        organization = Organization(**organization_data)
        json_data = organization_manager.to_json(organization)
        assert json_data is not None
        # You might want to do more specific checks on the JSON structure
    @pytest.mark.asyncio
    async def test_from_json(self, organization_manager):
        organization_data = OrganizationFactory.build()
        organization = Organization(**organization_data)
        json_data = organization_manager.to_json(organization)
        deserialized_organization = organization_manager.from_json(json_data)
        assert isinstance(deserialized_organization, Organization)
        # Additional checks on the deserialized data can be added
    @pytest.mark.asyncio
    async def test_add_bulk(self, organization_manager, mock_session):
        organizations_data = [OrganizationFactory.build() for _ in range(5)]
        mock_session.add_all.return_value = None
        mock_session.commit.return_value = None
        organizations = await organization_manager.add_bulk(organizations_data)
        mock_session.add_all.assert_called_once()
        mock_session.commit.assert_called_once()
        assert len(organizations) == 5
    @pytest.mark.asyncio
    async def test_update_bulk_success():
        manager = OrganizationManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking organization instances
        organization1 = Organization(organization_id=1, name="Rose", code="ROSE123")
        organization2 = Organization(organization_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding organization
        async def mock_get_by_id(organization_id):
            if organization_id == 1:
                return organization1
            if organization_id == 2:
                return organization2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update organizations
        updates = [{"organization_id": 1, "name": "Red Rose"}, {"organization_id": 2, "name": "Yellow Tulip"}]
        updated_organizations = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_organizations) == 2
        assert updated_organizations[0].name == "Red Rose"
        assert updated_organizations[1].name == "Yellow Tulip"
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_update_bulk_missing_organization_id():
        manager = OrganizationManager()
        # No organizations to update since organization_id is missing
        updates = [{"name": "Red Rose"}]
        updated_organizations = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_organizations) == 0
    @pytest.mark.asyncio
    async def test_update_bulk_organization_not_found():
        manager = OrganizationManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (organization not found)
        manager.get_by_id = AsyncMock(return_value=None)
        # Mocking the commit method
        session_mock.commit = AsyncMock()
        # Update organizations
        updates = [{"organization_id": 1, "name": "Red Rose"}]
        updated_organizations = await manager.update_bulk(updates)
        # Assertions
        assert len(updated_organizations) == 0
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_delete_bulk_success():
        manager = OrganizationManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking organization instances
        organization1 = Organization(organization_id=1, name="Rose", code="ROSE123")
        organization2 = Organization(organization_id=2, name="Tulip", code="TULIP123")
        # Mocking the get_by_id method to return the corresponding organization
        async def mock_get_by_id(organization_id):
            if organization_id == 1:
                return organization1
            if organization_id == 2:
                return organization2
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete organizations
        organization_ids = [1, 2]
        result = await manager.delete_bulk(organization_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called()
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_some_organizations_not_found():
        manager = OrganizationManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the get_by_id method to return None (organization not found)
        async def mock_get_by_id(organization_id):
            if organization_id == 1:
                return None
            if organization_id == 2:
                return Organization(organization_id=2, name="Tulip", code="TULIP123")
        manager.get_by_id = mock_get_by_id
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete organizations
        organization_ids = [1, 2]
        result = await manager.delete_bulk(organization_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_called_once_with(Organization(organization_id=2, name="Tulip", code="TULIP123"))
        session_mock.commit.assert_called_once()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list():
        manager = OrganizationManager()
        session_mock = AsyncMock()
        manager.session = session_mock
        # Mocking the commit and delete methods
        session_mock.commit = AsyncMock()
        session_mock.delete = AsyncMock()
        # Delete organizations with an empty list
        organization_ids = []
        result = await manager.delete_bulk(organization_ids)
        # Assertions
        assert result is True
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()
    @pytest.mark.asyncio
    async def test_count(self, organization_manager, mock_session):
        organizations_data = [OrganizationFactory.build() for _ in range(5)]
        mock_session.execute.return_value = AsyncMock(scalars=AsyncMock(all=AsyncMock(return_value=organizations_data)))
        count = await organization_manager.count()
        mock_session.execute.assert_called_once()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_basic_functionality(async_session):
        # Add a organization
        new_organization = Organization()
        async_session.add(new_organization)
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
        # Add multiple organizations
        organizations = [Organization() for _ in range(5)]
        async_session.add_all(organizations)
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
        # Add organizations
        organizations = [Organization(name=f"Organization_{i}") for i in range(5)]
        async_session.add_all(organizations)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_organizations = await manager.get_sorted_list(sort_by="name")
        assert [organization.name for organization in sorted_organizations] == [f"Organization_{i}" for i in range(5)]
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(async_session):
        # Add organizations
        organizations = [Organization(name=f"Organization_{i}") for i in range(5)]
        async_session.add_all(organizations)
        await async_session.commit()
        manager = YourManagerClass(session=async_session)
        sorted_organizations = await manager.get_sorted_list(sort_by="name", order="desc")
        assert [organization.name for organization in sorted_organizations] == [f"Organization_{i}" for i in reversed(range(5))]
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
        sorted_organizations = await manager.get_sorted_list(sort_by="name")
        assert len(sorted_organizations) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(async_session):
        # Add a organization
        organization = Organization(name="Organization_1")
        async_session.add(organization)
        await async_session.commit()
        # Modify the organization directly in the database
        await async_session.execute('UPDATE organizations SET name = :new_name WHERE id = :organization_id', {"new_name": "Modified_Organization", "organization_id": organization.id})
        await async_session.commit()
        # Now, refresh the organization using the manager function
        manager = YourManagerClass(session=async_session)
        refreshed_organization = await manager.refresh(organization)
        assert refreshed_organization.name == "Modified_Organization"
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_organization(async_session):
        organization = Organization(id=999, name="Nonexistent_Organization")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior
            await manager.refresh(organization)
    @pytest.mark.asyncio
    async def test_refresh_database_connection_issues(async_session, mocker):
        # Mock the session's refresh method to simulate a database connection error
        mocker.patch.object(async_session, 'refresh', side_effect=Exception("DB connection error"))
        organization = Organization(name="Organization_1")
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.refresh(organization)
    @pytest.mark.asyncio
    async def test_exists_with_existing_organization(async_session):
        # Add a organization
        organization = Organization(name="Organization_1")
        async_session.add(organization)
        await async_session.commit()
        # Check if the organization exists using the manager function
        manager = YourManagerClass(session=async_session)
        assert await manager.exists(organization.id) == True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_organization(async_session):
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
    #get_by_tac_id
    @pytest.mark.asyncio
    async def test_get_by_tac_id_existing(async_session):
        # Add a organization with a specific tac_id
        organization = Organization(name="Organization_1", tac_id=5)
        async_session.add(organization)
        await async_session.commit()
        # Fetch the organization using the manager function
        manager = YourManagerClass(session=async_session)
        fetched_organizations = await manager.get_by_tac_id(5)
        assert len(fetched_organizations) == 1
        assert fetched_organizations[0].name == "Organization_1"
    @pytest.mark.asyncio
    async def test_get_by_tac_id_nonexistent(async_session):
        non_existent_id = 999
        manager = YourManagerClass(session=async_session)
        fetched_organizations = await manager.get_by_tac_id(non_existent_id)
        assert len(fetched_organizations) == 0
    @pytest.mark.asyncio
    async def test_get_by_tac_id_invalid_type(async_session):
        invalid_id = "invalid_id"
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception):  # Modify the exception type based on your ORM's behavior or validation
            await manager.get_by_tac_id(invalid_id)
    @pytest.mark.asyncio
    async def test_get_by_tac_id_database_connection_issues(async_session, mocker):
        # Mock the execute method to simulate a database connection error
        mocker.patch.object(async_session, 'execute', side_effect=Exception("DB connection error"))
        manager = YourManagerClass(session=async_session)
        with pytest.raises(Exception, match="DB connection error"):
            await manager.get_by_tac_id(1)
