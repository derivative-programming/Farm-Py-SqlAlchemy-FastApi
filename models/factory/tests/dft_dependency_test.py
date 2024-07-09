# models/factory/tests/dft_dependency_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import, too-many-public-methods
"""
This module contains unit tests for the DFTDependencyFactory
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
from models import Base, DFTDependency
from models.factory import DFTDependencyFactory
from services.logging_config import get_logger

logger = get_logger(__name__)

TEST_DATABASE_URL = "sqlite:///:memory:"


class TestDFTDependencyFactory:
    """
    This class contains unit tests for the DFTDependencyFactory class.
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
        session_local = sessionmaker(
            bind=engine, expire_on_commit=False)
        session_instance = session_local()
        yield session_instance
        session_instance.close()

    def test_dft_dependency_creation(self, session):
        """
        Test case for creating a dft_dependency.
        """
        new_obj = DFTDependencyFactory.create(
            session=session)
        assert new_obj.dft_dependency_id is not None

    def test_code_default(self, session):
        """
        Test case for checking the default value of the code attribute.
        """
        new_obj = DFTDependencyFactory.create(
            session=session)
        assert isinstance(new_obj.code, uuid.UUID)

    def test_last_change_code_default_on_build(self, session):
        """
        Test case for checking the default value of
        the last_change_code attribute on build.
        """
        new_obj: DFTDependency = DFTDependencyFactory.build(
            session=session)
        assert new_obj.last_change_code == 0

    def test_last_change_code_default_on_creation(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on creation.
        """
        new_obj: DFTDependency = DFTDependencyFactory.create(
            session=session)
        assert new_obj.last_change_code == 1

    def test_last_change_code_default_on_update(self, session):
        """
        Test case for checking the default value of the
        last_change_code attribute on update.
        """
        new_obj = DFTDependencyFactory.create(
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
        new_obj = DFTDependencyFactory.build(
            session=session)
        assert new_obj.insert_utc_date_time is not None
        assert isinstance(
            new_obj.insert_utc_date_time, datetime)

    def test_date_inserted_on_initial_save(self, session):
        """
        Test case for checking the value of the
        insert_utc_date_time attribute on initial save.
        """
        new_obj = DFTDependencyFactory.build(
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
        new_obj = DFTDependencyFactory(
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
        new_obj = DFTDependencyFactory.build(
            session=session)
        assert new_obj.last_update_utc_date_time is not None
        assert isinstance(
            new_obj.last_update_utc_date_time, datetime)

    def test_date_updated_on_initial_save(self, session):
        """
        Test case for checking the value of the
        last_update_utc_date_time attribute on initial save.
        """
        new_obj = DFTDependencyFactory.build(
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
        new_obj = DFTDependencyFactory(
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
        dft_dependency model.
        """
        new_obj = DFTDependencyFactory.create(
            session=session)
        session.delete(new_obj)
        session.commit()
        deleted_dft_dependency = session.query(
            DFTDependency).filter_by(
            _dft_dependency_id=(
                new_obj.dft_dependency_id)
        ).first()
        assert deleted_dft_dependency is None

    def test_data_types(self, session):
        """
        Test case for checking the data types of
        the dft_dependency attributes.
        """
        obj = DFTDependencyFactory.create(
            session=session)
        assert isinstance(obj.dft_dependency_id, int)
        assert isinstance(obj.code, uuid.UUID)
        assert isinstance(obj.last_change_code, int)
        assert isinstance(obj.insert_user_id, uuid.UUID)
        assert isinstance(obj.last_update_user_id, uuid.UUID)
        assert isinstance(obj.dependency_df_task_id, int)
        assert isinstance(obj.dyna_flow_task_id, int)
        assert isinstance(obj.is_placeholder, bool)
        # dependencyDFTaskID
        # dynaFlowTaskID

        assert isinstance(
            obj.dyna_flow_task_code_peek, uuid.UUID)
        # isPlaceholder
        assert isinstance(obj.insert_utc_date_time, datetime)
        assert isinstance(obj.last_update_utc_date_time, datetime)

    def test_unique_code_constraint(self, session):
        """
        Test case for checking the unique code constraint.
        """
        dft_dependency_1 = DFTDependencyFactory.create(
            session=session)
        dft_dependency_2 = DFTDependencyFactory.create(
            session=session)
        dft_dependency_2.code = dft_dependency_1.code
        session.add_all([dft_dependency_1,
                         dft_dependency_2])
        with pytest.raises(Exception):
            session.commit()
        session.rollback()

    def test_fields_default(self):
        """
        Test case for checking the default values of
        the dft_dependency fields.
        """
        new_obj = DFTDependency()
        assert new_obj.code is not None
        assert new_obj.last_change_code is not None
        assert new_obj.insert_user_id == uuid.UUID(int=0)
        assert new_obj.last_update_user_id == uuid.UUID(int=0)
        assert new_obj.insert_utc_date_time is not None
        assert new_obj.last_update_utc_date_time is not None
        # dependencyDFTaskID
        # DynaFlowTaskID

        assert isinstance(
            new_obj.dyna_flow_task_code_peek, uuid.UUID)
        # isPlaceholder
        assert new_obj is not None
        assert new_obj.dependency_df_task_id == 0
        assert new_obj.dyna_flow_task_id == 0
        assert new_obj.is_placeholder is False

    def test_last_change_code_concurrency(self, session):
        """
        Test case to verify the concurrency of
        last_change_code in the DFTDependency
        model.

        This test case checks if the last_change_code
        of a DFTDependency object is
        updated correctly
        when multiple changes are made concurrently.
        It creates a DFTDependency object,
        retrieves it from the database, and updates its code
        attribute twice in separate transactions.
        Finally, it asserts that the last_change_code
        of the second retrieved DFTDependency object
        is different from the original last_change_code.

        Args:
            session (Session): The SQLAlchemy session object.

        Returns:
            None
        """

        new_obj = DFTDependencyFactory.create(
            session=session)
        original_last_change_code = \
            new_obj.last_change_code
        dft_dependency_1 = session.query(
            DFTDependency).filter_by(
            _dft_dependency_id=(
                new_obj.dft_dependency_id)
        ).first()
        dft_dependency_1.code = uuid.uuid4()
        session.commit()
        dft_dependency_2 = session.query(
            DFTDependency).filter_by(
            _dft_dependency_id=(
                new_obj.dft_dependency_id)
        ).first()
        dft_dependency_2.code = uuid.uuid4()
        session.commit()
        assert dft_dependency_2.last_change_code != \
            original_last_change_code
    # dependencyDFTaskID
    # DynaFlowTaskID

    def test_invalid_dyna_flow_task_id(self, session):
        """
        Test case to check if an invalid dyna_flow_task ID raises an IntegrityError.

        This test case creates a dft_dependency object using
        the DFTDependencyFactory and assigns an invalid dyna_flow_task ID to it.
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
        new_obj = DFTDependencyFactory.create(
            session=session)
        new_obj.dyna_flow_task_id = 99999
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    # isPlaceholder
