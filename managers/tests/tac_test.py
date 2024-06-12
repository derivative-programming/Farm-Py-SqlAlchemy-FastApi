# models/managers/tests/tac_test.py
"""
    #TODO add comment
"""
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import Tac
import models
from models.factory import TacFactory
from managers.tac import TacManager
from models.serialization_schema.tac import TacSchema
from services.db_config import DB_DIALECT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from sqlalchemy import String
from sqlalchemy.future import select
import logging
DB_DIALECT = "sqlite"
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestTacManager:
    """
    #TODO add comment
    """
    @pytest_asyncio.fixture(scope="function")
    async def tac_manager(self, session: AsyncSession):
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return TacManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data for our tac
        mock_data = {
            "code": generate_uuid()
        }
        # Call the build function of the manager
        tac = await tac_manager.build(**mock_data)
        # Assert that the returned object is an instance of Tac
        assert isinstance(tac, Tac)
        # Assert that the attributes of the tac match our mock data
        assert tac.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for missing data, test for that
        with pytest.raises(Exception):
            await tac_manager.build_async(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_tac_to_database(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.build_async(session)
        assert test_tac.tac_id is None
        # Add the tac using the manager's add method
        added_tac = await tac_manager.add(tac=test_tac)
        assert isinstance(added_tac, Tac)
        assert str(added_tac.insert_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(added_tac.last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert added_tac.tac_id > 0
        # Fetch the tac from the database directly
        result = await session.execute(
            select(Tac).filter(Tac.tac_id == added_tac.tac_id))
        fetched_tac = result.scalars().first()
        # Assert that the fetched tac is not None and matches the added tac
        assert fetched_tac is not None
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.tac_id == added_tac.tac_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_tac_object(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Create a test tac using the TacFactory without persisting it to the database
        test_tac = await TacFactory.build_async(session)
        assert test_tac.tac_id is None
        test_tac.code = generate_uuid()
        # Add the tac using the manager's add method
        added_tac = await tac_manager.add(tac=test_tac)
        assert isinstance(added_tac, Tac)
        assert str(added_tac.insert_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(added_tac.last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert added_tac.tac_id > 0
        # Assert that the returned tac matches the test tac
        assert added_tac.tac_id == test_tac.tac_id
        assert added_tac.code == test_tac.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.create_async(session)
        tac = await tac_manager.get_by_id(test_tac.tac_id)
        assert isinstance(tac, Tac)
        assert test_tac.tac_id == tac.tac_id
        assert test_tac.code == tac.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_tac = await tac_manager.get_by_id(non_existent_id)
        assert retrieved_tac is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.create_async(session)
        tac = await tac_manager.get_by_code(test_tac.code)
        assert isinstance(tac, Tac)
        assert test_tac.tac_id == tac.tac_id
        assert test_tac.code == tac.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Generate a random UUID that doesn't correspond to
        # any Tac in the database
        random_code = generate_uuid()
        tac = await tac_manager.get_by_code(random_code)
        assert tac is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.create_async(session)
        test_tac.code = generate_uuid()
        updated_tac = await tac_manager.update(tac=test_tac)
        assert isinstance(updated_tac, Tac)
        assert str(updated_tac.last_update_user_id) == str(
            tac_manager._session_context.customer_code)
        assert updated_tac.tac_id == test_tac.tac_id
        assert updated_tac.code == test_tac.code
        result = await session.execute(
            select(Tac).filter(
                Tac.tac_id == test_tac.tac_id)
        )
        fetched_tac = result.scalars().first()
        assert updated_tac.tac_id == fetched_tac.tac_id
        assert updated_tac.code == fetched_tac.code
        assert test_tac.tac_id == fetched_tac.tac_id
        assert test_tac.code == fetched_tac.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.create_async(session)
        new_code = generate_uuid()
        updated_tac = await tac_manager.update(
            tac=test_tac,
            code=new_code
        )
        assert isinstance(updated_tac, Tac)
        assert str(updated_tac.last_update_user_id) == str(
            tac_manager._session_context.customer_code
        )
        assert updated_tac.tac_id == test_tac.tac_id
        assert updated_tac.code == new_code
        result = await session.execute(
            select(Tac).filter(
                Tac.tac_id == test_tac.tac_id)
        )
        fetched_tac = result.scalars().first()
        assert updated_tac.tac_id == fetched_tac.tac_id
        assert updated_tac.code == fetched_tac.code
        assert test_tac.tac_id == fetched_tac.tac_id
        assert new_code == fetched_tac.code
    @pytest.mark.asyncio
    async def test_update_invalid_tac(self, tac_manager: TacManager):
        # None tac
        tac = None
        new_code = generate_uuid()
        updated_tac = await tac_manager.update(tac, code=new_code)
        # Assertions
        assert updated_tac is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        test_tac = await TacFactory.create_async(session)
        new_code = generate_uuid()
        with pytest.raises(ValueError):
            updated_tac = await tac_manager.update(
                tac=test_tac,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac_data = await TacFactory.create_async(session)
        result = await session.execute(
            select(Tac).filter(Tac.tac_id == tac_data.tac_id))
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.tac_id == tac_data.tac_id
        deleted_tac = await tac_manager.delete(
            tac_id=tac_data.tac_id)
        result = await session.execute(
            select(Tac).filter(Tac.tac_id == tac_data.tac_id))
        fetched_tac = result.scalars().first()
        assert fetched_tac is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await tac_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await tac_manager.delete("999")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tacs = await tac_manager.get_list()
        assert len(tacs) == 0
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        tacs = await tac_manager.get_list()
        assert len(tacs) == 5
        assert all(isinstance(tac, Tac) for tac in tacs)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac = await TacFactory.build_async(session)
        json_data = tac_manager.to_json(tac)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac = await TacFactory.build_async(session)
        dict_data = tac_manager.to_dict(tac)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac = await TacFactory.create_async(session)
        json_data = tac_manager.to_json(tac)
        deserialized_tac = tac_manager.from_json(json_data)
        assert isinstance(deserialized_tac, Tac)
        assert deserialized_tac.code == tac.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac = await TacFactory.create_async(session)
        schema = TacSchema()
        tac_data = schema.dump(tac)
        deserialized_tac = tac_manager.from_dict(tac_data)
        assert isinstance(deserialized_tac, Tac)
        assert deserialized_tac.code == tac.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tacs_data = [await TacFactory.build_async(session) for _ in range(5)]
        tacs = await tac_manager.add_bulk(tacs_data)
        assert len(tacs) == 5
        for updated_tac in tacs:
            result = await session.execute(select(Tac).filter(Tac.tac_id == updated_tac.tac_id))
            fetched_tac = result.scalars().first()
            assert isinstance(fetched_tac, Tac)
            assert str(fetched_tac.insert_user_id) == (
                str(tac_manager._session_context.customer_code))
            assert str(fetched_tac.last_update_user_id) == (
                str(tac_manager._session_context.customer_code))
            assert fetched_tac.tac_id == updated_tac.tac_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking tac instances
        tac1 = await TacFactory.create_async(session=session)
        tac2 = await TacFactory.create_async(session=session)
        logging.info(tac1.__dict__)
        code_updated1 = generate_uuid()
        code_updated2 = generate_uuid()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update tacs
        updates = [
            {
                "tac_id": 1,
                "code": code_updated1
            },
            {
                "tac_id": 2,
                "code": code_updated2
            }
        ]
        updated_tacs = await tac_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_tacs) == 2
        logging.info(updated_tacs[0].__dict__)
        logging.info(updated_tacs[1].__dict__)
        logging.info('getall')
        tacs = await tac_manager.get_list()
        logging.info(tacs[0].__dict__)
        logging.info(tacs[1].__dict__)
        assert updated_tacs[0].code == code_updated1
        assert updated_tacs[1].code == code_updated2
        assert str(updated_tacs[0].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        assert str(updated_tacs[1].last_update_user_id) == (
            str(tac_manager._session_context.customer_code))
        result = await session.execute(select(Tac).filter(Tac.tac_id == 1))
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.code == code_updated1
        result = await session.execute(select(Tac).filter(Tac.tac_id == 2))
        fetched_tac = result.scalars().first()
        assert isinstance(fetched_tac, Tac)
        assert fetched_tac.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_tac_id(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No tacs to update since tac_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            updated_tacs = await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_tac_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update tacs
        updates = [{"tac_id": 1, "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_tacs = await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"tac_id": "2", "code": generate_uuid()}]
        with pytest.raises(Exception):
            updated_tacs = await tac_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac1 = await TacFactory.create_async(session=session)
        tac2 = await TacFactory.create_async(session=session)
        # Delete tacs
        tac_ids = [1, 2]
        result = await tac_manager.delete_bulk(tac_ids)
        assert result is True
        for tac_id in tac_ids:
            execute_result = await session.execute(
                select(Tac).filter(Tac.tac_id == tac_id))
            fetched_tac = execute_result.scalars().first()
            assert fetched_tac is None
    @pytest.mark.asyncio
    async def test_delete_bulk_tacs_not_found(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac1 = await TacFactory.create_async(session=session)
        # Delete tacs
        tac_ids = [1, 2]
        with pytest.raises(Exception):
            result = await tac_manager.delete_bulk(tac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Delete tacs with an empty list
        tac_ids = []
        result = await tac_manager.delete_bulk(tac_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac_ids = ["1", 2]
        with pytest.raises(Exception):
            result = await tac_manager.delete_bulk(tac_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        count = await tac_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        count = await tac_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add tacs
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        sorted_tacs = await tac_manager.get_sorted_list(sort_by="tac_id")
        assert [tac.tac_id for tac in sorted_tacs] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add tacs
        tacs_data = (
            [await TacFactory.create_async(session) for _ in range(5)])
        sorted_tacs = await tac_manager.get_sorted_list(
            sort_by="tac_id", order="desc")
        assert [tac.tac_id for tac in sorted_tacs] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await tac_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        sorted_tacs = await tac_manager.get_sorted_list(sort_by="tac_id")
        assert len(sorted_tacs) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a tac
        tac1 = await TacFactory.create_async(session=session)
        result = await session.execute(select(Tac).filter(Tac.tac_id == tac1.tac_id))
        tac2 = result.scalars().first()
        assert tac1.code == tac2.code
        updated_code1 = generate_uuid()
        tac1.code = updated_code1
        updated_tac1 = await tac_manager.update(tac1)
        assert updated_tac1.code == updated_code1
        refreshed_tac2 = await tac_manager.refresh(tac2)
        assert refreshed_tac2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        tac = Tac(tac_id=999)
        with pytest.raises(Exception):
            await tac_manager.refresh(tac)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a tac
        tac1 = await TacFactory.create_async(session=session)
        # Check if the tac exists using the manager function
        assert await tac_manager.exists(tac1.tac_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a tac
        tac1 = await TacFactory.create_async(session=session)
        tac2 = await tac_manager.get_by_id(tac_id=tac1.tac_id)
        assert tac_manager.is_equal(tac1, tac2) is True
        tac1_dict = tac_manager.to_dict(tac1)
        tac3 = tac_manager.from_dict(tac1_dict)
        assert tac_manager.is_equal(tac1, tac3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_tac(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await tac_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tac_manager.exists(invalid_id)
        await session.rollback()
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        # Add a tac with a specific pac_id
        tac1 = await TacFactory.create_async(session=session)
        # Fetch the tac using the manager function
        fetched_tacs = await tac_manager.get_by_pac_id(tac1.pac_id)
        assert len(fetched_tacs) == 1
        assert isinstance(fetched_tacs[0], Tac)
        assert fetched_tacs[0].code == tac1.code
        stmt = select(models.Pac).where(
            models.Pac.pac_id == tac1.pac_id)
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert fetched_tacs[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        non_existent_id = 999
        fetched_tacs = await tac_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_tacs) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        tac_manager: TacManager,
        session: AsyncSession
    ):
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await tac_manager.get_by_pac_id(invalid_id)
        await session.rollback()
# endset
