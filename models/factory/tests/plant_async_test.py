# models/factory/tests/plant_async_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-argument, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains unit tests for the asynchronous
operations of the PlantFactory class.
"""

import asyncio
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401
from typing import AsyncGenerator, Generator

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

import pytest
from models import Base, Plant
from models.factory import PlantFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestPlantFactoryAsync:
    """
    This class contains unit tests for the asynchronous
    operations of the PlantFactory class.
    """

    @pytest.fixture(scope="function")
    def event_loop(self) -> Generator[asyncio.AbstractEventLoop, None, None]:
        """
        Fixture that returns an asyncio event loop for the test functions.
        """
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()

    @pytest.fixture(scope="function")
    def engine(self):
        """
        Fixture that returns an async engine for the test functions.
        """
        engine = create_async_engine(TEST_DATABASE_URL, echo=False)
        yield engine
        engine.sync_engine.dispose()

    @pytest_asyncio.fixture(scope="function")
    async def session(self, engine) -> AsyncGenerator[AsyncSession, None]:
        """
        Fixture that returns an async session for the test functions.
        """
        @event.listens_for(engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        async with engine.begin() as connection:
            await connection.begin_nested()
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)
            testing_session_local = sessionmaker(
                expire_on_commit=False,
                class_=AsyncSession,
                bind=engine,
            )
            async with testing_session_local(bind=connection) as session:  # type: ignore # noqa: E501
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
        """
        Test case for creating a plant
        asynchronously.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the plant ID
                is None after creation.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        assert plant.plant_id is not None

    @pytest.mark.asyncio
    async def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the code attribute is not
                an instance of uuid.UUID.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        assert isinstance(plant.code, uuid.UUID)

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the build_async method.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not 0.
        """
        plant: Plant = await \
            PlantFactory.build_async(
                session=session)
        assert plant.last_change_code == 0

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute when using the create_async method.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not 1.
        """
        plant: Plant = await \
            PlantFactory.create_async(
                session=session)
        assert plant.last_change_code == 1

    @pytest.mark.asyncio
    async def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute after updating the plant.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_change_code attribute is not updated.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        initial_code = plant.last_change_code
        plant.code = uuid.uuid4()
        await session.commit()
        assert plant.last_change_code != initial_code

    @pytest.mark.asyncio
    async def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the insert_utc_date_time
        attribute when using the build_async method.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the insert_utc_date_time attribute
            is None or not an instance of datetime.
        """
        plant = await \
            PlantFactory.build_async(
                session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the initial save.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is None or not an instance of datetime.
        """
        plant = await \
            PlantFactory.build_async(
                session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        plant.code = uuid.uuid4()
        session.add(plant)
        await session.commit()
        assert plant.insert_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute after the second save.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the insert_utc_date_time
            attribute is not the same as the initial time.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)
        initial_time = plant.insert_utc_date_time
        plant.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert plant.insert_utc_date_time == \
            initial_time

    @pytest.mark.asyncio
    async def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute when using
        the build_async method.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        plant = await \
            PlantFactory.build_async(
                session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the initial save.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is None or not an instance of datetime.
        """
        plant = await \
            PlantFactory.build_async(
                session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        plant.code = uuid.uuid4()
        session.add(plant)
        await session.commit()
        assert plant.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute after the second save.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the last_update_utc_date_time
            attribute is not greater than the initial time.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)
        initial_time = plant.last_update_utc_date_time
        plant.code = uuid.uuid4()
        time.sleep(1)
        await session.commit()
        assert plant.last_update_utc_date_time > \
            initial_time

    @pytest.mark.asyncio
    async def test_model_deletion(self, session):
        """
        Test case for deleting a plant
        from the database.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If the deleted
            plant is still
            found in the database.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        await session.delete(plant)
        await session.commit()

        # Construct the select statement
        stmt = select(Plant).where(
            Plant._plant_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                plant.plant_id))

        # Execute the statement asynchronously
        result = await session.execute(stmt)

        # Fetch all results
        deleted_plant = result.scalars().first()

        assert deleted_plant is None

    @pytest.mark.asyncio
    async def test_data_types(self, session):
        """
        Test case for checking the data types of
        the plant attributes.

        Args:
            session: The database session to use.

        Returns:
            None

        Raises:
            AssertionError: If any of the attribute types are incorrect.
        """
        obj = await \
            PlantFactory.create_async(
                session=session)
        assert isinstance(obj.plant_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.flvr_foreign_key_id, int)
        assert isinstance(obj.is_delete_allowed, bool)
        assert isinstance(obj.is_edit_allowed, bool)
        assert isinstance(obj.land_id, int)
        assert obj.other_flavor == "" or isinstance(
            obj.other_flavor, str)
        assert isinstance(obj.some_big_int_val, int)
        assert isinstance(obj.some_bit_val, bool)
        assert isinstance(obj.some_date_val, date)
        assert isinstance(obj.some_decimal_val, Decimal)
        assert obj.some_email_address == "" or isinstance(
            obj.some_email_address, str)
        assert isinstance(obj.some_float_val, float)
        assert isinstance(obj.some_int_val, int)
        assert isinstance(obj.some_money_val, Decimal)
        assert obj.some_n_var_char_val == "" or isinstance(
            obj.some_n_var_char_val, str)
        assert obj.some_phone_number == "" or isinstance(
            obj.some_phone_number, str)
        assert obj.some_text_val == "" or isinstance(
            obj.some_text_val, str)
        assert isinstance(obj.some_uniqueidentifier_val, uuid.UUID)
        assert isinstance(obj.some_utc_date_time_val, datetime)
        assert obj.some_var_char_val == "" or isinstance(
            obj.some_var_char_val, str)
        # Check for the peek values
# endset
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
        # flvrForeignKeyID

        assert isinstance(obj.flvr_foreign_key_code_peek, uuid.UUID)
        # landID

        assert isinstance(obj.land_code_peek, uuid.UUID)
        # someNVarCharVal
        # somePhoneNumber
        # someTextVal
        # someUniqueidentifierVal
# endset

        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    @pytest.mark.asyncio
    async def test_unique_code_constraint(self, session):
        """
        Test case to check the unique code constraint
        for plants.

        This test creates two plant
        instances using
        the PlantFactoryand assigns
        the same code to both plants.
        Then it adds both plants to the session and
        attempts to commit the changes.
        The test expects an exception to be raised,
        indicating that the unique code constraint has been violated.
        Finally, the test rolls back the session to
        ensure no changes are persisted.

        Note: This test assumes that the
        PlantFactory.create_async()
        method creates unique codes for
        each plant.
        """

        obj_1 = await PlantFactory.create_async(
            session=session)
        obj_2 = await PlantFactory.create_async(
            session=session)
        obj_2.code = obj_1.code
        session.add_all([obj_1,
                         obj_2])
        with pytest.raises(Exception):
            await session.commit()
        await session.rollback()

    @pytest.mark.asyncio
    async def test_fields_default(self):
        """
        Test case to verify the default values of
        the fields in the Plant model.

        This test case checks that the default values
        of various fields in the Plant
        model are set correctly.
        It asserts that the default values are not None
        or empty, and that the data types of certain fields are correct.
        """

        new_obj = Plant()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id is not None
        assert new_obj.last_update_user_id is not None
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None

# endset
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
        # someNVarCharVal
        # someDateVal
        # someUTCDateTimeVal
        # LandID

        assert isinstance(new_obj.land_code_peek, uuid.UUID)
        # FlvrForeignKeyID

        assert isinstance(new_obj.flvr_foreign_key_code_peek, uuid.UUID)
        # somePhoneNumber
        # someTextVal
        # someUniqueidentifierVal
        # someVarCharVal
# endset

        assert new_obj.flvr_foreign_key_id == 0
        assert new_obj.is_delete_allowed is False
        assert new_obj.is_edit_allowed is False
        assert new_obj.land_id == 0
        assert new_obj.other_flavor == ""
        assert new_obj.some_big_int_val == 0
        assert new_obj.some_bit_val is False
        assert new_obj.some_date_val == date(1753, 1, 1)
        assert new_obj.some_decimal_val == 0
        assert new_obj.some_email_address == ""
        assert math.isclose(new_obj.some_float_val, 0.0, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert new_obj.some_int_val == 0
        assert new_obj.some_money_val == 0
        assert new_obj.some_n_var_char_val == ""
        assert new_obj.some_phone_number == ""
        assert new_obj.some_text_val == ""
        assert isinstance(new_obj.some_uniqueidentifier_val, uuid.UUID)
        assert new_obj.some_utc_date_time_val == \
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.some_var_char_val == ""
# endset

    @pytest.mark.asyncio
    async def test_last_change_code_concurrency(self, session):
        """
        Test the concurrency of last_change_code
        in the Plant model.

        This test verifies that the last_change_code
        attribute of a Plant object
        is updated correctly when multiple instances
        of the object are modified
        concurrently.

        Steps:
        1. Create a new
            Plant object using
            the PlantFactory.
        2. Get the original value of the
            last_change_code attribute.
        3. Query the database for the Plant
            object using the
            plant_id.
        4. Modify the code attribute of the
            retrieved Plant object.
        5. Commit the changes to the database.
        6. Query the database again for the
            Plant object using the
            plant_id.
        7. Get the modified Plant object.
        8. Verify that the last_change_code attribute
            of the modified Plant object
            is different from the original value.

        Raises:
            AssertionError: If the last_change_code attribute
                            of the modified Plant
                            object is the same as the original value.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        original_last_change_code = plant.last_change_code

        stmt = select(Plant).where(
            Plant._plant_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                plant.plant_id))
        result = await session.execute(stmt)
        obj_1 = result.scalars().first()

        obj_1.code = uuid.uuid4()
        await session.commit()

        stmt = select(Plant).where(
            Plant._plant_id == (  # type: ignore # pylint: disable=protected-access  # noqa: ignore=E501
                plant.plant_id))
        result = await session.execute(stmt)
        obj_2 = result.scalars().first()

        obj_2.code = uuid.uuid4()
        await session.commit()
        assert obj_2.last_change_code != original_last_change_code
# endset

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
    # someNVarCharVal
    # someDateVal
    # someUTCDateTimeVal
    # LandID

    @pytest.mark.asyncio
    async def test_invalid_land_id(self, session):
        """
        Test case for handling an invalid land ID.

        This test case creates a plant using the
        PlantFactory and sets an invalid land ID.
        It then asserts that committing the session
        raises an IntegrityError and rolls back the session.

        Args:
            session: The SQLAlchemy session object.

        Raises:
            IntegrityError: If committing the session
            fails due to an integrity constraint violation.
        """
        plant = await \
            PlantFactory.create_async(
                session=session)
        plant.land_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # FlvrForeignKeyID

    @pytest.mark.asyncio
    async def test_invalid_flvr_foreign_key_id(self, session):
        """
        Test case to check if an invalid foreign key ID
        for the 'flvr_foreign_key_id' attribute of a
        Plant instance raises
        an IntegrityError.

        Args:
            session (Session): The SQLAlchemy session object.

        Raises:
            IntegrityError: If the foreign key constraint is violated.

        Returns:
            None
        """

        plant = await \
            PlantFactory.create_async(
                session=session)
        plant.flvr_foreign_key_id = 99999
        with pytest.raises(IntegrityError):
            await session.commit()
        await session.rollback()
    # somePhoneNumber
    # someTextVal
    # someUniqueidentifierVal
    # someVarCharVal
# endset
