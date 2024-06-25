# models/factory/tests/plant_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the PlantFactory
class in the models.factory package.
"""

from decimal import Decimal  # noqa: F401
import time
import math
import uuid  # noqa: F401
import logging
from datetime import datetime, date, timedelta  # noqa: F401
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Plant
from models.factory import PlantFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestPlantFactory:
    """
    This class contains unit tests for the PlantFactory class.
    """

    @pytest.fixture(scope="module")
    def engine(self):
        """
        Fixture for creating a database engine.
        """
        engine = create_engine(DATABASE_URL, echo=False)
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
        plant = PlantFactory.create(
            session=session)
        assert plant.plant_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        plant = PlantFactory.create(
            session=session)
        assert isinstance(plant.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        plant: Plant = PlantFactory.build(
            session=session)
        assert plant.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        plant: Plant = PlantFactory.create(
            session=session)
        assert plant.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        plant = PlantFactory.create(
            session=session)
        initial_code = plant.last_change_code
        plant.code = uuid.uuid4()
        session.commit()
        assert plant.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        plant = PlantFactory.build(
            session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        plant = PlantFactory.build(
            session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        plant.code = uuid.uuid4()
        session.add(plant)
        session.commit()
        assert plant.insert_utc_date_time > \
            initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        plant = PlantFactory(
            session=session)
        assert plant.insert_utc_date_time is not None
        assert isinstance(
            plant.insert_utc_date_time, datetime)
        initial_time = plant.insert_utc_date_time
        plant.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert plant.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        plant = PlantFactory.build(
            session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        plant = PlantFactory.build(
            session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        plant.code = uuid.uuid4()
        session.add(plant)
        session.commit()
        assert plant.last_update_utc_date_time > \
            initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        plant = PlantFactory(
            session=session)
        assert plant.last_update_utc_date_time is not None
        assert isinstance(
            plant.last_update_utc_date_time, datetime)
        initial_time = plant.last_update_utc_date_time
        plant.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert plant.last_update_utc_date_time > \
            initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        plant model.
        """
        plant = PlantFactory.create(
            session=session)
        session.delete(plant)
        session.commit()
        deleted_plant = session.query(Plant).filter_by(
            _plant_id=(
                plant.plant_id)
        ).first()
        assert deleted_plant is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the plant attributes.
        """
        plant = PlantFactory.create(
            session=session)
        assert isinstance(plant.plant_id, int)
        assert isinstance(plant.code, uuid.UUID)
        assert isinstance(plant.last_change_code, int)
        assert isinstance(plant.insert_user_id, uuid.UUID)
        assert isinstance(plant.last_update_user_id, uuid.UUID)
        assert isinstance(plant.flvr_foreign_key_id, int)
        assert isinstance(plant.is_delete_allowed, bool)
        assert isinstance(plant.is_edit_allowed, bool)
        assert isinstance(plant.land_id, int)
        assert plant.other_flavor == "" or isinstance(
            plant.other_flavor, str)
        assert isinstance(plant.some_big_int_val, int)
        assert isinstance(plant.some_bit_val, bool)
        assert isinstance(plant.some_date_val, date)
        assert isinstance(plant.some_decimal_val, Decimal)
        assert plant.some_email_address == "" or isinstance(
            plant.some_email_address, str)
        assert isinstance(plant.some_float_val, float)
        assert isinstance(plant.some_int_val, int)
        assert isinstance(plant.some_money_val, Decimal)
        assert plant.some_n_var_char_val == "" or isinstance(
            plant.some_n_var_char_val, str)
        assert plant.some_phone_number == "" or isinstance(
            plant.some_phone_number, str)
        assert plant.some_text_val == "" or isinstance(
            plant.some_text_val, str)
        # someUniqueidentifierVal
        assert isinstance(
            plant.some_uniqueidentifier_val, uuid.UUID)
        assert isinstance(plant.some_utc_date_time_val,
                          datetime)
        assert plant.some_var_char_val == "" or isinstance(
            plant.some_var_char_val, str)
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
            plant.flvr_foreign_key_code_peek, uuid.UUID)
        # landID

        assert isinstance(
            plant.land_code_peek, uuid.UUID)
        # someNVarCharVal,
        # somePhoneNumber,
        # someTextVal,
        # someUniqueidentifierVal,
# endset
        assert isinstance(plant.insert_utc_date_time, datetime)
        assert isinstance(plant.last_update_utc_date_time, datetime)

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
        plant = Plant()
        assert plant.code is not None
        assert plant.last_change_code is not None
        assert plant.insert_user_id == uuid.UUID(int=0)
        assert plant.last_update_user_id == uuid.UUID(int=0)
        assert plant.insert_utc_date_time is not None
        assert plant.last_update_utc_date_time is not None
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
            plant.land_code_peek, uuid.UUID)
        # FlvrForeignKeyID

        assert isinstance(
            plant.flvr_foreign_key_code_peek,
            uuid.UUID)
        # somePhoneNumber,
        # someTextVal,
        # someUniqueidentifierVal,
        # someVarCharVal,
# endset
        assert plant is not None
        assert plant.flvr_foreign_key_id == 0
        assert plant.is_delete_allowed is False
        assert plant.is_edit_allowed is False
        assert plant.land_id == 0
        assert plant.other_flavor == ""
        assert plant.some_big_int_val == 0
        assert plant.some_bit_val is False
        assert plant.some_date_val == date(1753, 1, 1)
        assert plant.some_decimal_val == 0
        assert plant.some_email_address == ""
        assert math.isclose(plant.some_float_val, 0.0, rel_tol=1e-9), (
            "Values must be approximately equal")
        assert plant.some_int_val == 0
        assert plant.some_money_val == 0
        assert plant.some_n_var_char_val == ""
        assert plant.some_phone_number == ""
        assert plant.some_text_val == ""
        # some_uniqueidentifier_val
        assert isinstance(
            plant.some_uniqueidentifier_val,
            uuid.UUID
        )
        assert plant.some_utc_date_time_val == datetime(1753, 1, 1)
        assert plant.some_var_char_val == ""
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

        plant = PlantFactory.create(
            session=session)
        original_last_change_code = plant.last_change_code
        plant_1 = session.query(
            Plant).filter_by(
            _plant_id=(
                plant.plant_id)
        ).first()
        plant_1.code = uuid.uuid4()
        session.commit()
        plant_2 = session.query(
            Plant).filter_by(
            _plant_id=(
                plant.plant_id)
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
        plant = PlantFactory.create(
            session=session)
        plant.land_id = 99999
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
        plant = PlantFactory.create(
            session=session)
        plant.flvr_foreign_key_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset
