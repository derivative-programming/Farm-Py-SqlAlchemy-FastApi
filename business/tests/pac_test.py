import pytest
import pytest_asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from models import Pac
from models.factory import PacFactory
from managers.pac import PacManager
from business.pac import PacBusObj
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
class TestPacBusObj:
    @pytest_asyncio.fixture(scope="function")
    async def pac_manager(self, session:AsyncSession):
        return PacManager(session)
    @pytest_asyncio.fixture(scope="function")
    async def pac_bus_obj(self, session):
        # Assuming that the PacBusObj requires a session object
        return PacBusObj(session)
    @pytest_asyncio.fixture(scope="function")
    async def new_pac(self, session):
        # Use the PacFactory to create a new pac instance
        # Assuming PacFactory.create() is an async function
        return await PacFactory.create_async(session)
    @pytest.mark.asyncio
    async def test_create_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test creating a new pac
        assert pac_bus_obj.pac_id is None
        # assert isinstance(pac_bus_obj.pac_id, int)
        if db_dialect == 'postgresql':
            assert isinstance(pac_bus_obj.code, UUID)
        elif db_dialect == 'mssql':
            assert isinstance(pac_bus_obj.code, UNIQUEIDENTIFIER)
        else:  # This will cover SQLite, MySQL, and other databases
            assert isinstance(pac_bus_obj.code, str)
        assert isinstance(pac_bus_obj.last_change_code, int)
        assert pac_bus_obj.insert_user_id is None
        assert pac_bus_obj.last_update_user_id is None
        assert pac_bus_obj.description == "" or isinstance(pac_bus_obj.description, str)
        assert isinstance(pac_bus_obj.display_order, int)
        assert isinstance(pac_bus_obj.is_active, bool)
        assert pac_bus_obj.lookup_enum_name == "" or isinstance(pac_bus_obj.lookup_enum_name, str)
        assert pac_bus_obj.name == "" or isinstance(pac_bus_obj.name, str)
    @pytest.mark.asyncio
    async def test_load_with_pac_obj(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(pac_obj_instance=new_pac)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac) == True
    @pytest.mark.asyncio
    async def test_load_with_pac_id(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(pac_id=new_pac.pac_id)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_load_with_pac_code(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        await pac_bus_obj.load(code=new_pac.code)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_load_with_pac_json(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        pac_json = pac_manager.to_json(new_pac)
        await pac_bus_obj.load(json_data=pac_json)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_load_with_pac_dict(self, session, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        logger.info("test_load_with_pac_dict 1")
        pac_dict = pac_manager.to_dict(new_pac)
        logger.info(pac_dict)
        await pac_bus_obj.load(pac_dict=pac_dict)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_get_nonexistent_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test retrieving a nonexistent pac raises an exception
        await pac_bus_obj.load(pac_id=-1)
        assert pac_bus_obj.is_valid() == False # Assuming -1 is an id that wouldn't exist
    @pytest.mark.asyncio
    async def test_update_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        # Test updating a pac's data
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        new_code = generate_uuid()
        await pac_bus_obj.load(pac_obj_instance=new_pac)
        pac_bus_obj.code = new_code
        await pac_bus_obj.save()
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        assert pac_manager.is_equal(pac_bus_obj.pac,new_pac)  == True
    @pytest.mark.asyncio
    async def test_delete_pac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):
        assert new_pac.pac_id is not None
        assert pac_bus_obj.pac_id is None
        await pac_bus_obj.load(pac_id=new_pac.pac_id)
        assert pac_bus_obj.pac_id is not None
        await pac_bus_obj.delete()
        new_pac = await pac_manager.get_by_id(new_pac.pac_id)
        assert new_pac is None

    @pytest.mark.asyncio
    async def test_build_tri_state_filter(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        tri_state_filter_bus_obj = await pac_bus_obj.build_tri_state_filter()

        assert tri_state_filter_bus_obj.pac_id == pac_bus_obj.pac_id
        assert tri_state_filter_bus_obj.pac_code_peek == pac_bus_obj.code

        await tri_state_filter_bus_obj.save()

        assert tri_state_filter_bus_obj.tri_state_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tri_state_filter(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        tri_state_filter_bus_obj = await pac_bus_obj.build_tri_state_filter()

        await tri_state_filter_bus_obj.save()

        tri_state_filter_list = await pac_bus_obj.get_all_tri_state_filter()

        assert len(tri_state_filter_list) >= 1

        #assert tri_state_filter_list[0].tri_state_filter_id > 0

        #assert tri_state_filter_list[0].tri_state_filter_id == tri_state_filter_bus_obj.tri_state_filter_id

    @pytest.mark.asyncio
    async def test_build_tac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        tac_bus_obj = await pac_bus_obj.build_tac()

        assert tac_bus_obj.pac_id == pac_bus_obj.pac_id
        assert tac_bus_obj.pac_code_peek == pac_bus_obj.code

        await tac_bus_obj.save()

        assert tac_bus_obj.tac_id > 0

    @pytest.mark.asyncio
    async def test_get_all_tac(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        tac_bus_obj = await pac_bus_obj.build_tac()

        await tac_bus_obj.save()

        tac_list = await pac_bus_obj.get_all_tac()

        assert len(tac_list) >= 1

        #assert tac_list[0].tac_id > 0

        #assert tac_list[0].tac_id == tac_bus_obj.tac_id

    @pytest.mark.asyncio
    async def test_build_role(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        role_bus_obj = await pac_bus_obj.build_role()

        assert role_bus_obj.pac_id == pac_bus_obj.pac_id
        assert role_bus_obj.pac_code_peek == pac_bus_obj.code

        await role_bus_obj.save()

        assert role_bus_obj.role_id > 0

    @pytest.mark.asyncio
    async def test_get_all_role(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        role_bus_obj = await pac_bus_obj.build_role()

        await role_bus_obj.save()

        role_list = await pac_bus_obj.get_all_role()

        assert len(role_list) >= 1

        #assert role_list[0].role_id > 0

        #assert role_list[0].role_id == role_bus_obj.role_id

    @pytest.mark.asyncio
    async def test_build_land(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        land_bus_obj = await pac_bus_obj.build_land()

        assert land_bus_obj.pac_id == pac_bus_obj.pac_id
        assert land_bus_obj.pac_code_peek == pac_bus_obj.code

        await land_bus_obj.save()

        assert land_bus_obj.land_id > 0

    @pytest.mark.asyncio
    async def test_get_all_land(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        land_bus_obj = await pac_bus_obj.build_land()

        await land_bus_obj.save()

        land_list = await pac_bus_obj.get_all_land()

        assert len(land_list) >= 1

        #assert land_list[0].land_id > 0

        #assert land_list[0].land_id == land_bus_obj.land_id

    @pytest.mark.asyncio
    async def test_build_flavor(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        flavor_bus_obj = await pac_bus_obj.build_flavor()

        assert flavor_bus_obj.pac_id == pac_bus_obj.pac_id
        assert flavor_bus_obj.pac_code_peek == pac_bus_obj.code

        await flavor_bus_obj.save()

        assert flavor_bus_obj.flavor_id > 0

    @pytest.mark.asyncio
    async def test_get_all_flavor(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        flavor_bus_obj = await pac_bus_obj.build_flavor()

        await flavor_bus_obj.save()

        flavor_list = await pac_bus_obj.get_all_flavor()

        assert len(flavor_list) >= 1

        #assert flavor_list[0].flavor_id > 0

        #assert flavor_list[0].flavor_id == flavor_bus_obj.flavor_id

    @pytest.mark.asyncio
    async def test_build_error_log(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        error_log_bus_obj = await pac_bus_obj.build_error_log()

        assert error_log_bus_obj.pac_id == pac_bus_obj.pac_id
        assert error_log_bus_obj.pac_code_peek == pac_bus_obj.code

        await error_log_bus_obj.save()

        assert error_log_bus_obj.error_log_id > 0

    @pytest.mark.asyncio
    async def test_get_all_error_log(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        error_log_bus_obj = await pac_bus_obj.build_error_log()

        await error_log_bus_obj.save()

        error_log_list = await pac_bus_obj.get_all_error_log()

        assert len(error_log_list) >= 1

        #assert error_log_list[0].error_log_id > 0

        #assert error_log_list[0].error_log_id == error_log_bus_obj.error_log_id

    @pytest.mark.asyncio
    async def test_build_date_greater_than_filter(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        date_greater_than_filter_bus_obj = await pac_bus_obj.build_date_greater_than_filter()

        assert date_greater_than_filter_bus_obj.pac_id == pac_bus_obj.pac_id
        assert date_greater_than_filter_bus_obj.pac_code_peek == pac_bus_obj.code

        await date_greater_than_filter_bus_obj.save()

        assert date_greater_than_filter_bus_obj.date_greater_than_filter_id > 0

    @pytest.mark.asyncio
    async def test_get_all_date_greater_than_filter(self, pac_manager:PacManager, pac_bus_obj:PacBusObj, new_pac:Pac):

        await current_runtime.initialize(session=pac_manager.session)

        await pac_bus_obj.load(pac_id=new_pac.pac_id)

        date_greater_than_filter_bus_obj = await pac_bus_obj.build_date_greater_than_filter()

        await date_greater_than_filter_bus_obj.save()

        date_greater_than_filter_list = await pac_bus_obj.get_all_date_greater_than_filter()

        assert len(date_greater_than_filter_list) >= 1

        #assert date_greater_than_filter_list[0].date_greater_than_filter_id > 0

        #assert date_greater_than_filter_list[0].date_greater_than_filter_id == date_greater_than_filter_bus_obj.date_greater_than_filter_id

