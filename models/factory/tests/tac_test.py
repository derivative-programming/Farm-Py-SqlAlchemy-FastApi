# models/factory/tests/tac_test.py
# pylint: disable=unused-import
"""
This module contains unit tests for the TacFactory
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
from models import Base, Tac
from models.factory import TacFactory
from services.logging_config import get_logger
logger = get_logger(__name__)

DATABASE_URL = "sqlite:///:memory:"


class TestTacFactory:
    """
    This class contains unit tests for the TacFactory class.
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

    def test_tac_creation(self, session):
        """
        Test case for creating a tac.
        """
        tac = TacFactory.create(
            session=session)
        assert tac.tac_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        logging.info("vrtest")
        tac = TacFactory.create(
            session=session)
        assert isinstance(tac.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        tac: Tac = TacFactory.build(
            session=session)
        assert tac.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        tac: Tac = TacFactory.create(
            session=session)
        assert tac.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        tac = TacFactory.create(
            session=session)
        initial_code = tac.last_change_code
        tac.code = uuid.uuid4()
        session.commit()
        assert tac.last_change_code != \
            initial_code

    def test_date_inserted_on_build(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on build.
        """
        tac = TacFactory.build(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        tac = TacFactory.build(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = uuid.uuid4()
        session.add(tac)
        session.commit()
        assert tac.insert_utc_date_time > \
            initial_time

    def test_date_inserted_on_second_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on second save.
        """
        tac = TacFactory(
            session=session)
        assert tac.insert_utc_date_time is not None
        assert isinstance(
            tac.insert_utc_date_time, datetime)
        initial_time = tac.insert_utc_date_time
        tac.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tac.insert_utc_date_time == initial_time

    def test_date_updated_on_build(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on build.
        """
        tac = TacFactory.build(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        tac = TacFactory.build(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)
        initial_time = datetime.utcnow() + timedelta(days=-1)
        tac.code = uuid.uuid4()
        session.add(tac)
        session.commit()
        assert tac.last_update_utc_date_time > \
            initial_time

    def test_date_updated_on_second_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on second save.
        """
        tac = TacFactory(
            session=session)
        assert tac.last_update_utc_date_time is not None
        assert isinstance(
            tac.last_update_utc_date_time, datetime)
        initial_time = tac.last_update_utc_date_time
        tac.code = uuid.uuid4()
        time.sleep(1)
        session.commit()
        assert tac.last_update_utc_date_time > \
            initial_time

    def test_model_deletion(self, session):
        """
        Test case for deleting a
        tac model.
        """
        tac = TacFactory.create(
            session=session)
        session.delete(tac)
        session.commit()
        deleted_tac = session.query(Tac).filter_by(
            _tac_id=(
                tac.tac_id)
        ).first()
        assert deleted_tac is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the tac attributes.
        """
        tac = TacFactory.create(
            session=session)
        assert isinstance(tac.tac_id, int)
        assert isinstance(tac.code, uuid.UUID)
        assert isinstance(tac.last_change_code, int)
        assert isinstance(tac.insert_user_id, uuid.UUID)
        assert isinstance(tac.last_update_user_id, uuid.UUID)
        assert tac.description == "" or isinstance(
            tac.description, str)
        assert isinstance(tac.display_order, int)
        assert isinstance(tac.is_active, bool)
        assert tac.lookup_enum_name == "" or isinstance(
            tac.lookup_enum_name, str)
        assert tac.name == "" or isinstance(
            tac.name, str)
        assert isinstance(tac.pac_id, int)
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # pacID

        assert isinstance(
            tac.pac_code_peek, uuid.UUID)
        assert isinstance(tac.insert_utc_date_time, datetime)
        assert isinstance(tac.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        tac_1 = TacFactory.create(
            session=session)
        tac_2 = TacFactory.create(
            session=session)
        tac_2.code = tac_1.code
        session.add_all([tac_1,
                         tac_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the tac fields.
        """
        tac = Tac()
        assert tac.code is not None
        assert tac.last_change_code is not None
        assert tac.insert_user_id == uuid.UUID(int=0)
        assert tac.last_update_user_id == uuid.UUID(int=0)
        assert tac.insert_utc_date_time is not None
        assert tac.last_update_utc_date_time is not None
        # description,
        # displayOrder,
        # isActive,
        # lookupEnumName,
        # name,
        # PacID

        assert isinstance(
            tac.pac_code_peek, uuid.UUID)
        assert tac is not None
        assert tac.description == ""
        assert tac.display_order == 0
        assert tac.is_active is False
        assert tac.lookup_enum_name == ""
        assert tac.name == ""
        assert tac.pac_id == 0

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the Tac
        model.

        This test case checks if the last_change_code
        of a Tac object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a Tac object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved Tac object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        tac = TacFactory.create(
            session=session)
        original_last_change_code = tac.last_change_code
        tac_1 = session.query(Tac).filter_by(
            _tac_id=(
                tac.tac_id)
        ).first()
        tac_1.code = uuid.uuid4()
        session.commit()
        tac_2 = session.query(Tac).filter_by(
            _tac_id=(
                tac.tac_id)
        ).first()
        tac_2.code = uuid.uuid4()
        session.commit()
        assert tac_2.last_change_code != \
            original_last_change_code
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    def test_invalid_pac_id(self, session):
        """
        Test case to check if an invalid pac ID raises an IntegrityError.

        This test case creates a tac object using
        the TacFactory and assigns an invalid pac ID to it.
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
        tac = TacFactory.create(
            session=session)
        tac.pac_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

