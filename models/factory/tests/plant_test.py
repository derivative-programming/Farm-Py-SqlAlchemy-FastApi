# models/factory/tests/plant_test.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import, too-many-public-methods
"""
This module contains unit tests for the PlantFactory
class in the models.factory package.
"""

import logging
import math  # noqa: F401
import time
import uuid  # noqa: F401
from datetime import date, datetime, timedelta, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import pytest
from models import Base, Plant
from models.factory import PlantFactory
from services.logging_config import get_logger

logger = get_logger(__name__)

TEST_DATABASE_URL = "sqlite:///:memory:"


class TestPlantFactory:
    """
    This class contains unit tests for the PlantFactory class.
    """

    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(TEST_DATABASE_URL, echo=False)
        # FKs are not activated by default in sqllite
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
        yield engine
        engine.dispose()

    @pytest.fixture
    def session(self, engine):
        """
        Fixture for creating a database session.
        """
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(  # pylint: disable=invalid-name
            bind=engine, expire_on_commit=False)
        session_instance = SessionLocal()
        yield session_instance
        session_instance.close()

    def test_plant_creation(self, session):
        """
        Test case for creating a plant.
        """
        new_obj = PlantFactory.create(
            session=session)
        assert new_obj.plant_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = PlantFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: Plant = PlantFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: Plant = PlantFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = PlantFactory.create(
            session=session)
        initial_code = new_obj.last_change_code
        new_obj.code = uuid.uuid4()
        session.commit()
        assert new_obj.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        new_obj = PlantFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = PlantFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        new_obj.code = uuid.uuid4()
        session.add(new_obj)
        session.commit()
        assert new_obj.insert_utc_date_time > \
            initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        new_obj = PlantFactory(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)
        initial_time = new_obj.insert_utc_date_time
        new_obj.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert new_obj.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        new_obj = PlantFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = PlantFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)
        initial_time = datetime.now(timezone.utc) + timedelta(days=-1)
        new_obj.code = uuid.uuid4()
        session.add(new_obj)
        session.commit()
        assert new_obj.last_update_utc_date_time > \
            initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        new_obj = PlantFactory(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)
        initial_time = new_obj.last_update_utc_date_time
        new_obj.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert new_obj.last_update_utc_date_time > \
            initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        plant model.
        """
        new_obj = PlantFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_plant = session.query(
            Plant).filter_by(
            _plant_id=(
                new_obj.plant_id)
        ).first()
        assert deleted_plant is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the plant attributes.
        """
        obj = PlantFactory.create(
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
        # someUniqueidentifierVal
        assert isinstance(
            obj.some_uniqueidentifier_val, uuid.UUID)
        assert isinstance(obj.some_utc_date_time_val,
                          datetime)
        assert obj.some_var_char_val == "" or isinstance(
            obj.some_var_char_val, str)
        # Check for the peek values,
        # assuming they are UUIDs based on your model
# endset
        # isDeleteAllowed,
        # isEditAllowed,
        # otherFlavor,
        # someBigIntVal,
        # someBitVal,
        # someDecimalVal,
        # someEmailAddress,
        # someFloatVal,
        # someIntVal,
        # someMoneyVal,
        # someVarCharVal,
        # someDateVal
        # someUTCDateTimeVal
        # flvrForeignKeyID

        assert isinstance(
            obj.flvr_foreign_key_code_peek, uuid.UUID)
        # landID

        assert isinstance(
            obj.land_code_peek, uuid.UUID)
        # someNVarCharVal,
        # somePhoneNumber,
        # someTextVal,
        # someUniqueidentifierVal,
# endset
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        plant_1 = PlantFactory.create(
            session=session)
        plant_2 = PlantFactory.create(
            session=session)
        plant_2.code = plant_1.code
        session.add_all([plant_1,
                         plant_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the plant fields.
        """
        new_obj = Plant()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
# endset
        # isDeleteAllowed,
        # isEditAllowed,
        # otherFlavor,
        # someBigIntVal,
        # someBitVal,
        # someDecimalVal,
        # someEmailAddress,
        # someFloatVal,
        # someIntVal,
        # someMoneyVal,
        # someNVarCharVal,
        # someDateVal
        # someUTCDateTimeVal
        # LandID

        assert isinstance(
            new_obj.land_code_peek, uuid.UUID)
        # FlvrForeignKeyID

        assert isinstance(
            new_obj.flvr_foreign_key_code_peek,
            uuid.UUID)
        # somePhoneNumber,
        # someTextVal,
        # someUniqueidentifierVal,
        # someVarCharVal,
# endset
        assert new_obj is not None
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
        # some_uniqueidentifier_val
        assert isinstance(
            new_obj.some_uniqueidentifier_val,
            uuid.UUID
        )
        assert new_obj.some_utc_date_time_val == datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert new_obj.some_var_char_val == ""
# endset

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Plant
        model.

        This test case checks if the last_change_code
        of a Plant object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Plant object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Plant object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = PlantFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        plant_1 = session.query(
            Plant).filter_by(
            _plant_id=(
                new_obj.plant_id)
        ).first()
        plant_1.code = uuid.uuid4()
        session.commit()
        plant_2 = session.query(
            Plant).filter_by(
            _plant_id=(
                new_obj.plant_id)
        ).first()
        plant_2.code = uuid.uuid4()
        session.commit()
        assert plant_2.last_change_code != \
            original_last_change_code
# endset
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # LandID

    def test_invalid_land_id(self, session):
        """
        Test case to check if an invalid land ID raises an IntegrityError.

        This test case creates a plant object using
        the PlantFactory and assigns an invalid land ID to it.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.

        Args:
            session (Session): The SQLAlchemy session object.

        Raises:
            IntegrityError: If the changes to the
                session violate any integrity constraints.

        """
        new_obj = PlantFactory.create(
            session=session)
        new_obj.land_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # FlvrForeignKeyID

    def test_invalid_flvr_foreign_key_id(self, session):
        """
        Test case to check if an invalid foreign key ID
        for flavor is handled correctly.

        This test creates a new plant object using
        the PlantFactory and sets an invalid foreign key ID for the flavor.
        It then tries to commit the changes to the
        session and expects an IntegrityError to be raised.
        Finally, it rolls back the session to ensure
        no changes are persisted.

        Note: This test assumes that the PlantFactory
            and session objects are properly set up.

        Args:
            session (Session): The SQLAlchemy session object.

        Raises:
            IntegrityError: If the changes to the
            session violate the integrity constraints.

        Returns:
            None
        """
        new_obj = PlantFactory.create(
            session=session)
        new_obj.flvr_foreign_key_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset
