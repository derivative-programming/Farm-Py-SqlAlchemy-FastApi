# business/tests/plant_base_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
# pylint: disable=redefined-outer-name
# pylint: disable=too-few-public-methods

"""
This module contains unit tests for the
PlantBusObj class.
"""

import math  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from unittest.mock import AsyncMock, Mock, patch

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

import current_runtime  # noqa: F401
import pytest
from business.plant_base import PlantBaseBusObj
from helpers.session_context import SessionContext
from managers.plant import PlantManager
from models import Plant
from models.factory import PlantFactory
from services.logging_config import get_logger

from ..plant import PlantBusObj

##GENINCLUDEFILE[GENVALPascalName.top.include.*]


BUSINESS_PLANT_BASE_MANAGER_PATCH = (
    "business.plant_base"
    ".PlantManager"
)

logger = get_logger(__name__)


@pytest.fixture
def mock_session_context():
    """
    Fixture that returns a fake session context.
    """
    session = Mock()
    session_context = Mock(spec=SessionContext)
    session_context.session = session
    return session_context


@pytest.fixture
def plant():
    """
    Fixture that returns a mock
    plant object.
    """
    return Mock(spec=Plant)


@pytest.fixture
def mock_sess_base_bus_obj(
    mock_session_context, plant
):
    """
    Fixture that returns a
    PlantBaseBusObj instance.
    """
    mock_sess_base_bus_obj = PlantBaseBusObj(
        mock_session_context)
    mock_sess_base_bus_obj.plant = \
        plant
    return mock_sess_base_bus_obj


class TestPlantBaseBusObj:
    """
    Unit tests for the
    PlantBusObj class.
    """

    @pytest_asyncio.fixture(scope="function")
    async def obj_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of the
        PlantManager class.
        """
        session_context = SessionContext({}, session)
        return PlantManager(session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_bus_obj(self, session):
        """
        Fixture that returns an instance of the
        PlantBusObj class.
        """
        session_context = SessionContext({}, session)
        return PlantBusObj(
            session_context)

    @pytest_asyncio.fixture(scope="function")
    async def new_obj(self, session):
        """
        Fixture that returns a new instance of
        the Plant class.
        """

        return await PlantFactory.create_async(
            session)

    @pytest.mark.asyncio
    async def test_create_plant(
        self,
        new_bus_obj: PlantBusObj
    ):
        """
        Test case for creating a new plant.
        """
        # Test creating a new plant

        assert new_bus_obj.plant_id == 0

        assert isinstance(new_bus_obj.plant_id, int)
        assert isinstance(
            new_bus_obj.code, uuid.UUID)

        assert isinstance(
            new_bus_obj.last_change_code, int)

        assert new_bus_obj.insert_user_id == uuid.UUID(int=0)

        assert new_bus_obj.last_update_user_id == uuid.UUID(int=0)

# endset
        assert isinstance(new_bus_obj.flvr_foreign_key_id,
                          int)
        assert isinstance(new_bus_obj.is_delete_allowed,
                          bool)
        assert isinstance(new_bus_obj.is_edit_allowed,
                          bool)
        assert isinstance(new_bus_obj.land_id,
                          int)
        assert isinstance(new_bus_obj.other_flavor,
                          str)
        assert isinstance(new_bus_obj.some_big_int_val,
                          int)
        assert isinstance(new_bus_obj.some_bit_val,
                          bool)
        assert isinstance(new_bus_obj.some_date_val,
                          date)
        assert isinstance(new_bus_obj.some_decimal_val,
                          Decimal)
        assert isinstance(new_bus_obj.some_email_address,
                          str)
        assert isinstance(new_bus_obj.some_float_val,
                          float)
        assert isinstance(new_bus_obj.some_int_val,
                          int)
        assert isinstance(new_bus_obj.some_money_val,
                          Decimal)
        assert isinstance(new_bus_obj.some_n_var_char_val,
                          str)
        assert isinstance(new_bus_obj.some_phone_number,
                          str)
        assert isinstance(new_bus_obj.some_text_val,
                          str)
        # some_uniqueidentifier_val
        assert isinstance(new_bus_obj.some_uniqueidentifier_val,
                          uuid.UUID)
        assert isinstance(new_bus_obj.some_utc_date_time_val,
                          datetime)
        assert isinstance(new_bus_obj.some_var_char_val, str)
# endset

    @pytest.mark.asyncio
    async def test_load_with_plant_obj(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for loading data from a
        plant object instance.
        """

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.plant, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_id(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for loading data from a
        plant ID.
        """

        new_obj_plant_id = \
            new_obj.plant_id

        await new_bus_obj.load_from_id(
            new_obj_plant_id)

        assert obj_manager.is_equal(
            new_bus_obj.plant, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_code(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for loading data from a
        plant code.
        """

        await new_bus_obj.load_from_code(
            new_obj.code)

        assert obj_manager.is_equal(
            new_bus_obj.plant, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_json(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for loading data from a
        plant JSON.
        """

        plant_json = \
            obj_manager.to_json(
                new_obj)

        await new_bus_obj.load_from_json(
            plant_json)

        assert obj_manager.is_equal(
            new_bus_obj.plant, new_obj) is True

    @pytest.mark.asyncio
    async def test_load_with_plant_dict(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for loading data from a
        plant dictionary.
        """

        logger.info("test_load_with_plant_dict 1")

        plant_dict = \
            obj_manager.to_dict(
                new_obj)

        logger.info(plant_dict)

        await new_bus_obj.load_from_dict(
            plant_dict)

        assert obj_manager.is_equal(
            new_bus_obj.plant,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_plant(
        self,
        new_bus_obj: PlantBusObj
    ):
        """
        Test case for retrieving a nonexistent
        plant.
        """
        # Test retrieving a nonexistent
        # plant raises an exception
        await new_bus_obj.load_from_id(-1)

        # Assuming -1 is an id that wouldn't exist
        assert new_bus_obj.is_valid() is False

    @pytest.mark.asyncio
    async def test_update_plant(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for updating a plant's data.
        """
        # Test updating a plant's data

        new_obj_plant_id_value = \
            new_obj.plant_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_plant_id_value)

        assert isinstance(new_obj,
                          Plant)

        new_code = uuid.uuid4()

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert obj_manager.is_equal(
            new_bus_obj.plant,
            new_obj) is True

        new_bus_obj.code = new_code

        await new_bus_obj.save()

        new_obj_plant_id_value = \
            new_obj.plant_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_plant_id_value)

        assert obj_manager.is_equal(
            new_bus_obj.plant,
            new_obj) is True

    @pytest.mark.asyncio
    async def test_delete_plant(
        self,
        obj_manager: PlantManager,
        new_bus_obj: PlantBusObj,
        new_obj: Plant
    ):
        """
        Test case for deleting a plant.
        """

        assert new_bus_obj.plant is not None

        assert new_bus_obj.plant_id == 0

        new_bus_obj.load_from_obj_instance(
            new_obj)

        assert new_bus_obj.plant_id is not None

        await new_bus_obj.delete()

        new_obj_plant_id_value = \
            new_obj.plant_id

        new_obj = await \
            obj_manager.get_by_id(
                new_obj_plant_id_value)

        assert new_obj is None

    def test_get_session_context(
        self,
        mock_sess_base_bus_obj,
        mock_session_context
    ):
        """
        Test case for getting the session context.
        """
        assert mock_sess_base_bus_obj.get_session_context() == \
            mock_session_context

    @pytest.mark.asyncio
    async def test_refresh(
        self,
        mock_sess_base_bus_obj,
        plant
    ):
        """
        Test case for refreshing the plant data.
        """
        with patch(
            BUSINESS_PLANT_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.refresh =\
                AsyncMock(return_value=plant)

            refreshed_mock_sess_base_bus_obj = await \
                mock_sess_base_bus_obj.refresh()
            assert refreshed_mock_sess_base_bus_obj \
                .plant == plant
            mock_obj_manager_instance.refresh \
                .assert_called_once_with(plant)

    def test_is_valid(
            self, mock_sess_base_bus_obj):
        """
        Test case for checking if the plant data is valid.
        """
        assert mock_sess_base_bus_obj.is_valid() is True

        mock_sess_base_bus_obj.plant = None
        assert mock_sess_base_bus_obj.is_valid() is False

    def test_to_dict(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the plant
        data to a dictionary.
        """
        with patch(
            BUSINESS_PLANT_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_dict = Mock(
                return_value={"key": "value"})

            plant_dict = mock_sess_base_bus_obj.to_dict()
            assert plant_dict == {"key": "value"}
            mock_obj_manager_instance.to_dict.assert_called_once_with(
                mock_sess_base_bus_obj.plant)

    def test_to_json(
            self, mock_sess_base_bus_obj):
        """
        Test case for converting the plant data to JSON.
        """
        with patch(
            BUSINESS_PLANT_BASE_MANAGER_PATCH,
            autospec=True
        ) as mock_obj_manager:
            mock_obj_manager_instance = \
                mock_obj_manager.return_value
            mock_obj_manager_instance.to_json = Mock(
                return_value='{"key": "value"}')

            plant_json = mock_sess_base_bus_obj.to_json()
            assert plant_json == '{"key": "value"}'
            mock_obj_manager_instance.to_json.assert_called_once_with(
                mock_sess_base_bus_obj.plant)

    def test_get_obj(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for getting the plant object.
        """
        assert mock_sess_base_bus_obj.get_obj() == plant

    def test_get_object_name(
            self, mock_sess_base_bus_obj):
        """
        Test case for getting the object name.
        """
        assert mock_sess_base_bus_obj \
            .get_object_name() == "plant"

    def test_get_id(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for getting the plant ID.
        """
        plant.plant_id = 1
        assert mock_sess_base_bus_obj.get_id() == 1

    def test_plant_id(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the plant_id property.
        """
        plant.plant_id = 1
        assert mock_sess_base_bus_obj.plant_id == 1

    def test_code(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the code property.
        """
        test_uuid = uuid.uuid4()
        plant.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the code setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.code = test_uuid
        assert mock_sess_base_bus_obj.code == \
            test_uuid

    def test_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.code = "not-a-uuid"

    def test_last_change_code(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case to verify the behavior of the last_change_code
        attribute in the PlantBaseBusiness class.

        Args:
            mock_sess_base_bus_obj (PlantBaseBusiness):
                An instance of the
                PlantBaseBusiness class.
            plant (Plant):
                An instance of the
                Plant class.

        Returns:
            None
        """
        plant.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_change_code setter.
        """
        mock_sess_base_bus_obj.last_change_code = 123
        assert mock_sess_base_bus_obj.last_change_code == 123

    def test_last_change_code_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_change_code property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.last_change_code = "not-an-int"

    def test_insert_user_id(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        insert_user_id property.
        """
        test_uuid = uuid.uuid4()
        plant.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_user_id setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.insert_user_id = test_uuid
        assert mock_sess_base_bus_obj.insert_user_id == \
            test_uuid

    def test_insert_user_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_user_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.insert_user_id = "not-a-uuid"
# endset
    # isDeleteAllowed

    def test_is_delete_allowed(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        is_delete_allowed property.
        """
        plant.is_delete_allowed = True
        assert mock_sess_base_bus_obj \
            .is_delete_allowed is True

    def test_is_delete_allowed_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_delete_allowed setter.
        """
        mock_sess_base_bus_obj.is_delete_allowed = \
            True
        assert mock_sess_base_bus_obj \
            .is_delete_allowed is True

    def test_is_delete_allowed_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_delete_allowed property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.is_delete_allowed = \
                "not-a-boolean"
    # isEditAllowed

    def test_is_edit_allowed(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        is_edit_allowed property.
        """
        plant.is_edit_allowed = \
            True
        assert mock_sess_base_bus_obj \
            .is_edit_allowed is True

    def test_is_edit_allowed_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        is_edit_allowed setter.
        """
        mock_sess_base_bus_obj.is_edit_allowed = \
            True
        assert mock_sess_base_bus_obj \
            .is_edit_allowed is True

    def test_is_edit_allowed_invalid_value(self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        is_edit_allowed property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.is_edit_allowed = \
                "not-a-boolean"
    # otherFlavor

    def test_other_flavor(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        other_flavor property.
        """
        plant.other_flavor = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .other_flavor == "Vanilla"

    def test_other_flavor_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        other_flavor setter.
        """
        mock_sess_base_bus_obj.other_flavor = \
            "Vanilla"
        assert mock_sess_base_bus_obj \
            .other_flavor == "Vanilla"

    def test_other_flavor_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        other_flavor property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.other_flavor = \
                123
    # someBigIntVal

    def test_some_big_int_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_big_int_val property.
        """
        plant.some_big_int_val = \
            1000000
        assert mock_sess_base_bus_obj \
            .some_big_int_val == 1000000

    def test_some_big_int_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_big_int_val setter.
        """
        mock_sess_base_bus_obj.some_big_int_val = \
            1000000
        assert mock_sess_base_bus_obj \
            .some_big_int_val == 1000000

    def test_some_big_int_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_big_int_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_big_int_val = \
                "not-an-int"
    # someBitVal

    def test_some_bit_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_bit_val property.
        """
        plant.some_bit_val = \
            True
        assert mock_sess_base_bus_obj \
            .some_bit_val is True

    def test_some_bit_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_bit_val setter.
        """
        mock_sess_base_bus_obj.some_bit_val = \
            True
        assert mock_sess_base_bus_obj \
            .some_bit_val is True

    def test_some_bit_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_bit_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_bit_val = \
                "not-a-boolean"
    # someDateVal

    def test_some_date_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_date_val property.
        """
        test_date = date.today()
        plant.some_date_val = \
            test_date
        assert mock_sess_base_bus_obj \
            .some_date_val == \
            test_date

    def test_some_date_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_date_val setter.
        """
        test_date = date.today()
        mock_sess_base_bus_obj.some_date_val = \
            test_date
        assert mock_sess_base_bus_obj \
            .some_date_val == \
            test_date

    def test_some_date_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_date_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_date_val = \
                "not-a-date"
    # someDecimalVal

    def test_some_decimal_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_decimal_val property.
        """
        test_decimal = Decimal('10.99')
        plant.some_decimal_val = \
            test_decimal
        assert mock_sess_base_bus_obj \
            .some_decimal_val == \
            test_decimal

    def test_some_decimal_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_decimal_val setter.
        """
        test_decimal = Decimal('10.99')
        mock_sess_base_bus_obj.some_decimal_val = \
            test_decimal
        assert mock_sess_base_bus_obj \
            .some_decimal_val == \
            test_decimal

    def test_some_decimal_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_decimal_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_decimal_val = \
                "not-a-decimal"
    # someEmailAddress

    def test_some_email_address(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_email_address property.
        """
        plant.some_email_address = \
            "test@example.com"
        assert mock_sess_base_bus_obj \
            .some_email_address == "test@example.com"

    def test_some_email_address_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_email_address setter.
        """
        mock_sess_base_bus_obj.some_email_address = \
            "test@example.com"
        assert mock_sess_base_bus_obj \
            .some_email_address == "test@example.com"

    def test_some_email_address_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_email_address property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_email_address = \
                123
    # someFloatVal

    def test_some_float_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_float_val property.
        """
        plant.some_float_val = 1.23
        assert math.isclose(
            mock_sess_base_bus_obj.some_float_val, 1.23)

    def test_some_float_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_float_val setter.
        """
        mock_sess_base_bus_obj.some_float_val = 1.23
        assert math.isclose(
            mock_sess_base_bus_obj.some_float_val, 1.23)

    def test_some_float_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_float_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_float_val = \
                "not-a-float"
    # someIntVal

    def test_some_int_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_int_val property.
        """
        plant.some_int_val = 1
        assert mock_sess_base_bus_obj \
            .some_int_val == 1

    def test_some_int_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_int_val setter.
        """
        mock_sess_base_bus_obj.some_int_val = 1
        assert mock_sess_base_bus_obj \
            .some_int_val == 1

    def test_some_int_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_int_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_int_val = \
                "not-an-int"
    # someMoneyVal

    def test_some_money_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_money_val property.
        """
        test_money = Decimal('100.00')
        plant.some_money_val = \
            test_money
        assert mock_sess_base_bus_obj \
            .some_money_val == \
            test_money

    def test_some_money_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_money_val setter.
        """
        test_money = Decimal('100.00')
        mock_sess_base_bus_obj.some_money_val = \
            test_money
        assert mock_sess_base_bus_obj \
            .some_money_val == \
            test_money

    def test_some_money_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_money_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_money_val = \
                "not-a-decimal"
    # someNVarCharVal

    def test_some_n_var_char_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_n_var_char_val property.
        """
        plant.some_n_var_char_val = \
            "Some N Var Char"
        assert mock_sess_base_bus_obj \
            .some_n_var_char_val == \
            "Some N Var Char"

    def test_some_n_var_char_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_n_var_char_val setter.
        """
        mock_sess_base_bus_obj.some_n_var_char_val = \
            "Some N Var Char"
        assert mock_sess_base_bus_obj \
            .some_n_var_char_val == \
            "Some N Var Char"

    def test_some_n_var_char_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_n_var_char_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_n_var_char_val = \
                123
    # somePhoneNumber

    def test_some_phone_number(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_phone_number property.
        """
        plant.some_phone_number = "123-456-7890"
        assert mock_sess_base_bus_obj \
            .some_phone_number == "123-456-7890"

    def test_some_phone_number_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_phone_number setter.
        """
        mock_sess_base_bus_obj.some_phone_number = \
            "123-456-7890"
        assert mock_sess_base_bus_obj \
            .some_phone_number == "123-456-7890"

    def test_some_phone_number_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_phone_number property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_phone_number = \
                123
    # someTextVal

    def test_some_text_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_text_val property.
        """
        plant.some_text_val = \
            "Some Text"
        assert mock_sess_base_bus_obj \
            .some_text_val == "Some Text"

    def test_some_text_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_text_val setter.
        """
        mock_sess_base_bus_obj.some_text_val = \
            "Some Text"
        assert mock_sess_base_bus_obj \
            .some_text_val == "Some Text"

    def test_some_text_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_text_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_text_val = \
                123
    # someUniqueidentifierVal

    def test_some_uniqueidentifier_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_uniqueidentifier_val property.
        """
        test_uuid = uuid.uuid4()
        plant.some_uniqueidentifier_val = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .some_uniqueidentifier_val == \
            test_uuid

    def test_some_uniqueidentifier_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_uniqueidentifier_val setter.
        """
        test_uuid = uuid.uuid4()
        mock_sess_base_bus_obj.some_uniqueidentifier_val = \
            test_uuid
        assert mock_sess_base_bus_obj \
            .some_uniqueidentifier_val == \
            test_uuid

    def test_some_uniqueidentifier_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_uniqueidentifier_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_uniqueidentifier_val = \
                "not-a-uuid"
    # someUTCDateTimeVal

    def test_some_utc_date_time_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_utc_date_time_val property.
        """
        test_datetime = datetime.now(timezone.utc)
        plant.some_utc_date_time_val = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .some_utc_date_time_val == \
            test_datetime

    def test_some_utc_date_time_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_utc_date_time_val setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.some_utc_date_time_val = \
            test_datetime
        assert mock_sess_base_bus_obj \
            .some_utc_date_time_val == \
            test_datetime

    def test_some_utc_date_time_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_utc_date_time_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_utc_date_time_val = \
                "not-a-datetime"
    # someVarCharVal

    def test_some_var_char_val(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        some_var_char_val property.
        """
        plant.some_var_char_val = \
            "Some Var Char"
        assert mock_sess_base_bus_obj \
            .some_var_char_val == \
            "Some Var Char"

    def test_some_var_char_val_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        some_var_char_val setter.
        """
        mock_sess_base_bus_obj.some_var_char_val = \
            "Some Var Char"
        assert mock_sess_base_bus_obj \
            .some_var_char_val == \
            "Some Var Char"

    def test_some_var_char_val_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        some_var_char_val property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.some_var_char_val = \
                123
    # FlvrForeignKeyID
    # LandID
# endset
    # someNVarCharVal
    # somePhoneNumber
    # someTextVal
    # someUniqueidentifierVal
    # FlvrForeignKeyID

    def test_flvr_foreign_key_id(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the
        flvr_foreign_key_id property.
        """
        plant.flvr_foreign_key_id = 1
        assert mock_sess_base_bus_obj \
            .flvr_foreign_key_id == 1

    def test_flvr_foreign_key_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        flvr_foreign_key_id setter.
        """
        mock_sess_base_bus_obj.flvr_foreign_key_id = 1
        assert mock_sess_base_bus_obj \
            .flvr_foreign_key_id == 1

    def test_flvr_foreign_key_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        flvr_foreign_key_id property.
        """
        with pytest.raises(ValueError):
            mock_sess_base_bus_obj.flvr_foreign_key_id = \
                "not-an-int"
    # LandID

    def test_land_id(
            self, mock_sess_base_bus_obj, plant):
        """
        Test case for the land_id property.
        """
        plant.land_id = 1
        assert mock_sess_base_bus_obj \
            .land_id == 1

    def test_land_id_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the land_id setter.
        """
        mock_sess_base_bus_obj.land_id = 1
        assert mock_sess_base_bus_obj \
            .land_id == 1

    def test_land_id_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        land_id property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.land_id = \
                "not-an-int"
    # isDeleteAllowed
    # isEditAllowed
    # otherFlavor
    # someBigIntVal
    # someBitVal
    # someDecimalVal
    # someEmailAddress
    # someFloatVal
    # someIntVal
    # someMoneyVal
    # someVarCharVal
    # someDateVal
    # someUTCDateTimeVal
# endset

    def test_insert_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            plant):
        """
        Test case for the
        insert_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        plant.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        insert_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.insert_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .insert_utc_date_time == \
            test_datetime

    def test_insert_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        insert_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.insert_utc_date_time = \
                "not-a-datetime"

    def test_last_update_utc_date_time(
            self,
            mock_sess_base_bus_obj,
            plant):
        """
        Test case for the
        last_update_utc_date_time property.
        """
        test_datetime = datetime.now(timezone.utc)
        plant.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_setter(
            self, mock_sess_base_bus_obj):
        """
        Test case for the
        last_update_utc_date_time setter.
        """
        test_datetime = datetime.now(timezone.utc)
        mock_sess_base_bus_obj.last_update_utc_date_time = test_datetime
        assert mock_sess_base_bus_obj \
            .last_update_utc_date_time == \
            test_datetime

    def test_last_update_utc_date_time_invalid_value(
            self, mock_sess_base_bus_obj):
        """
        Test case for setting an invalid value for the
        last_update_utc_date_time property.
        """
        with pytest.raises(AssertionError):
            mock_sess_base_bus_obj.last_update_utc_date_time = \
                "not-a-datetime"

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
