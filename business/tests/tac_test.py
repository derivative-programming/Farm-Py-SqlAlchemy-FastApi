import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.session_context import SessionContext
from models import Tac
from models.factory import TacFactory
from managers.tac import TacManager
from business.tac import TacBusObj
from services.db_config import db_dialect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
import managers as managers_and_enums
import current_runtime

logger = get_logger(__name__)
db_dialect = "sqlite"
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TestTacBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def tac_manager(self, session:AsyncSession):
        session_context = SessionContext(dict(),session)
        return TacManager(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def tac_bus_obj(self, session):
        session_context = SessionContext(dict(),session)
        return TacBusObj(session_context)
    @pytest_asyncio.fixture(scope="function")
    async def new_tac(self, session):
        # Use the TacFactory to create a new tac instance
        # Assuming TacFactory.create() is an async function
        return await TacFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test creating a new tac
        assert tac_bus_obj.tac_id is None
        # assert isinstance(tac_bus_obj.tac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(tac_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(tac_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(tac_bus_obj.code, str)
        assert isinstance(tac_bus_obj.last_change_code, int)
        assert tac_bus_obj.insert_user_id is None
        assert tac_bus_obj.last_update_user_id is None
        assert tac_bus_obj.description == "" or isinstance(tac_bus_obj.description, str)
        assert isinstance(tac_bus_obj.display_order, int)
        assert isinstance(tac_bus_obj.is_active, bool)
        assert tac_bus_obj.lookup_enum_name == "" or isinstance(tac_bus_obj.lookup_enum_name, str)
        assert tac_bus_obj.name == "" or isinstance(tac_bus_obj.name, str)
        assert isinstance(tac_bus_obj.pac_id, int)
    @pytest.mark.asyncio
    async def test_load_with_tac_obj(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(tac_obj_instance=new_tac)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac) == True
    @pytest.mark.asyncio
    async def test_load_with_tac_id(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(tac_id=new_tac.tac_id)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_code(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        await tac_bus_obj.load(code=new_tac.code)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_json(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        tac_json = tac_manager.to_json(new_tac)
        await tac_bus_obj.load(json_data=tac_json)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_load_with_tac_dict(self, session, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        logger.info("test_load_with_tac_dict 1")
        tac_dict = tac_manager.to_dict(new_tac)
        logger.info(tac_dict)
        await tac_bus_obj.load(tac_dict=tac_dict)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test retrieving a nonexistent tac raises an exception
        await tac_bus_obj.load(tac_id=-1)
        assert tac_bus_obj.is_valid() == False # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        # Test updating a tac's data
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        new_code = generate_uuid()
        await tac_bus_obj.load(tac_obj_instance=new_tac)
        tac_bus_obj.code = new_code
        await tac_bus_obj.save()
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        assert tac_manager.is_equal(tac_bus_obj.tac,new_tac)  == True
    @pytest.mark.asyncio
    async def test_delete_tac(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac):
        assert new_tac.tac_id is not None
        assert tac_bus_obj.tac_id is None
        await tac_bus_obj.load(tac_id=new_tac.tac_id)
        assert tac_bus_obj.tac_id is not None
        await tac_bus_obj.delete()
        new_tac = await tac_manager.get_by_id(new_tac.tac_id)
        assert new_tac is None

    @pytest.mark.asyncio
    async def test_build_organization(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac, session:AsyncSession):

        session_context = SessionContext(dict(),session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load(tac_id=new_tac.tac_id)

        organization_bus_obj = await tac_bus_obj.build_organization()

        assert organization_bus_obj.tac_id == tac_bus_obj.tac_id
        assert organization_bus_obj.tac_code_peek == tac_bus_obj.code

        await organization_bus_obj.save()

        assert organization_bus_obj.organization_id > 0

    @pytest.mark.asyncio
    async def test_get_all_organization(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac, session:AsyncSession):

        session_context = SessionContext(dict(),session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load(tac_id=new_tac.tac_id)

        organization_bus_obj = await tac_bus_obj.build_organization()

        await organization_bus_obj.save()

        organization_list = await tac_bus_obj.get_all_organization()

        assert len(organization_list) >= 1

        #assert organization_list[0].organization_id > 0

        #assert organization_list[0].organization_id == organization_bus_obj.organization_id

    @pytest.mark.asyncio
    async def test_build_customer(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac, session:AsyncSession):

        session_context = SessionContext(dict(),session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load(tac_id=new_tac.tac_id)

        customer_bus_obj = await tac_bus_obj.build_customer()

        assert customer_bus_obj.tac_id == tac_bus_obj.tac_id
        assert customer_bus_obj.tac_code_peek == tac_bus_obj.code

        await customer_bus_obj.save()

        assert customer_bus_obj.customer_id > 0

    @pytest.mark.asyncio
    async def test_get_all_customer(self, tac_manager:TacManager, tac_bus_obj:TacBusObj, new_tac:Tac, session:AsyncSession):

        session_context = SessionContext(dict(),session)

        await current_runtime.initialize(session_context)

        await tac_bus_obj.load(tac_id=new_tac.tac_id)

        customer_bus_obj = await tac_bus_obj.build_customer()

        await customer_bus_obj.save()

        customer_list = await tac_bus_obj.get_all_customer()

        assert len(customer_list) >= 1

        #assert customer_list[0].customer_id > 0

        #assert customer_list[0].customer_id == customer_bus_obj.customer_id

