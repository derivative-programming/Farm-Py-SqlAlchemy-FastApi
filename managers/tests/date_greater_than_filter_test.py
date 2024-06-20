# models/managers/tests/date_greater_than_filter_test.py
# pylint: disable=protected-access
# pylint: disable=unused-argument
"""
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
"""
# TODO file too big. split into separate test files
import logging
from typing import List
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
from helpers.session_context import SessionContext
from managers.date_greater_than_filter import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
from models.factory import DateGreaterThanFilterFactory
from models.serialization_schema.date_greater_than_filter import DateGreaterThanFilterSchema
class TestDateGreaterThanFilterManager:
    """
    This class contains unit tests for the
    `DateGreaterThanFilterManager` class.
    """
    @pytest_asyncio.fixture(scope="function")
    async def date_greater_than_filter_manager(self, session: AsyncSession):
        """
        Fixture that returns an instance of
        `DateGreaterThanFilterManager` for testing.
        """
        session_context = SessionContext(dict(), session)
        session_context.customer_code = uuid.uuid4()
        return DateGreaterThanFilterManager(session_context)
    @pytest.mark.asyncio
    async def test_build(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `build` method of
        `DateGreaterThanFilterManager`.
        """
        # Define mock data for our date_greater_than_filter
        mock_data = {
            "code": uuid.uuid4()
        }
        # Call the build function of the manager
        date_greater_than_filter = await date_greater_than_filter_manager.build(**mock_data)
        # Assert that the returned object is an instance of DateGreaterThanFilter
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        # Assert that the attributes of the date_greater_than_filter match our mock data
        assert date_greater_than_filter.code == mock_data["code"]
    @pytest.mark.asyncio
    async def test_build_with_missing_data(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `build` method of
        `DateGreaterThanFilterManager` with missing data.
        """
        # Define mock data with a missing key
        mock_data = {
            "non_existant_property": "Rose"
        }
        # If the build method is expected to raise an exception for
        # missing data, test for that
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.build(**mock_data)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_add_correctly_adds_date_greater_than_filter_to_database(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DateGreaterThanFilterManager` that checks if a
        date_greater_than_filter is correctly added to the database.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        assert test_date_greater_than_filter.date_greater_than_filter_id == 0
        # Add the date_greater_than_filter using the manager's add method
        added_date_greater_than_filter = await date_greater_than_filter_manager.add(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(added_date_greater_than_filter, DateGreaterThanFilter)
        assert str(added_date_greater_than_filter.insert_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        assert str(added_date_greater_than_filter.last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        assert added_date_greater_than_filter.date_greater_than_filter_id > 0
        # Fetch the date_greater_than_filter from the database directly
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == added_date_greater_than_filter.date_greater_than_filter_id  # type: ignore
            )
        )
        fetched_date_greater_than_filter = result.scalars().first()
        # Assert that the fetched date_greater_than_filter is not None and matches the added date_greater_than_filter
        assert fetched_date_greater_than_filter is not None
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.date_greater_than_filter_id == added_date_greater_than_filter.date_greater_than_filter_id
    @pytest.mark.asyncio
    async def test_add_returns_correct_date_greater_than_filter_object(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `add` method of
        `DateGreaterThanFilterManager` that checks if the
        correct date_greater_than_filter object is returned.
        """
        # Create a test date_greater_than_filter using the DateGreaterThanFilterFactory
        # without persisting it to the database
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        assert test_date_greater_than_filter.date_greater_than_filter_id == 0
        test_date_greater_than_filter.code = uuid.uuid4()
        # Add the date_greater_than_filter using the manager's add method
        added_date_greater_than_filter = await date_greater_than_filter_manager.add(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(added_date_greater_than_filter, DateGreaterThanFilter)
        assert str(added_date_greater_than_filter.insert_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        assert str(added_date_greater_than_filter.last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        assert added_date_greater_than_filter.date_greater_than_filter_id > 0
        # Assert that the returned date_greater_than_filter matches the test date_greater_than_filter
        assert added_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert added_date_greater_than_filter.code == test_date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_id` method of
        `DateGreaterThanFilterManager`.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(test_date_greater_than_filter.date_greater_than_filter_id)
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        assert test_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `get_by_id` method of
        `DateGreaterThanFilterManager` when the date_greater_than_filter is not found.
        """
        non_existent_id = 9999  # An ID that's not in the database
        retrieved_date_greater_than_filter = await date_greater_than_filter_manager.get_by_id(non_existent_id)
        assert retrieved_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_get_by_code_returns_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `get_by_code` method of
        `DateGreaterThanFilterManager` that checks if a date_greater_than_filter is
        returned by its code.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_code(test_date_greater_than_filter.code)
        assert isinstance(date_greater_than_filter, DateGreaterThanFilter)
        assert test_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_get_by_code_returns_none_for_nonexistent_code(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `get_by_code` method of
        `DateGreaterThanFilterManager` when the code does not exist.
        """
        # Generate a random UUID that doesn't correspond to
        # any DateGreaterThanFilter in the database
        random_code = uuid.uuid4()
        date_greater_than_filter = await date_greater_than_filter_manager.get_by_code(random_code)
        assert date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_update(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `DateGreaterThanFilterManager`
        that checks if a date_greater_than_filter is correctly updated.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        test_date_greater_than_filter.code = uuid.uuid4()
        updated_date_greater_than_filter = await date_greater_than_filter_manager.update(date_greater_than_filter=test_date_greater_than_filter)
        assert isinstance(updated_date_greater_than_filter, DateGreaterThanFilter)
        assert str(updated_date_greater_than_filter.last_update_user_id) == str(
            date_greater_than_filter_manager._session_context.customer_code)
        assert updated_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == test_date_greater_than_filter.code
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert updated_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == fetched_date_greater_than_filter.code
        assert test_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert test_date_greater_than_filter.code == fetched_date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_update_via_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `DateGreaterThanFilterManager`
        that checks if a date_greater_than_filter is correctly updated using a dictionary.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        new_code = uuid.uuid4()
        updated_date_greater_than_filter = await date_greater_than_filter_manager.update(
            date_greater_than_filter=test_date_greater_than_filter,
            code=new_code
        )
        assert isinstance(updated_date_greater_than_filter, DateGreaterThanFilter)
        assert str(updated_date_greater_than_filter.last_update_user_id) == str(
            date_greater_than_filter_manager._session_context.customer_code
        )
        assert updated_date_greater_than_filter.date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == new_code
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == test_date_greater_than_filter.date_greater_than_filter_id)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert updated_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert updated_date_greater_than_filter.code == fetched_date_greater_than_filter.code
        assert test_date_greater_than_filter.date_greater_than_filter_id == fetched_date_greater_than_filter.date_greater_than_filter_id
        assert new_code == fetched_date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_update_invalid_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case for the `update` method of `DateGreaterThanFilterManager`
        with an invalid date_greater_than_filter.
        """
        # None date_greater_than_filter
        date_greater_than_filter = None
        new_code = uuid.uuid4()
        updated_date_greater_than_filter = await (
            date_greater_than_filter_manager.update(date_greater_than_filter, code=new_code))  # type: ignore
        # Assertions
        assert updated_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_update_with_nonexistent_attribute(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `update` method of `DateGreaterThanFilterManager`
        with a nonexistent attribute.
        """
        test_date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        new_code = uuid.uuid4()
        with pytest.raises(ValueError):
            await date_greater_than_filter_manager.update(
                date_greater_than_filter=test_date_greater_than_filter,
                xxx=new_code
            )
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case for the `delete` method of `DateGreaterThanFilterManager`.
        """
        date_greater_than_filter_data = await DateGreaterThanFilterFactory.create_async(session)
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id
        await date_greater_than_filter_manager.delete(
            date_greater_than_filter_id=date_greater_than_filter_data.date_greater_than_filter_id)
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter_data.date_greater_than_filter_id)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert fetched_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_delete_nonexistent(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete(999)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete("999")  # type: ignore
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_list(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        assert len(date_greater_than_filters) == 0
        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(date_greater_than_filters_data, List)
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        assert len(date_greater_than_filters) == 5
        assert all(isinstance(date_greater_than_filter, DateGreaterThanFilter) for date_greater_than_filter in date_greater_than_filters)
    @pytest.mark.asyncio
    async def test_to_json(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        json_data = date_greater_than_filter_manager.to_json(date_greater_than_filter)
        assert json_data is not None
    @pytest.mark.asyncio
    async def test_to_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.build_async(session)
        dict_data = date_greater_than_filter_manager.to_dict(date_greater_than_filter)
        assert dict_data is not None
    @pytest.mark.asyncio
    async def test_from_json(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        json_data = date_greater_than_filter_manager.to_json(date_greater_than_filter)
        deserialized_date_greater_than_filter = date_greater_than_filter_manager.from_json(json_data)
        assert isinstance(deserialized_date_greater_than_filter, DateGreaterThanFilter)
        assert deserialized_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_from_dict(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter = await DateGreaterThanFilterFactory.create_async(session)
        schema = DateGreaterThanFilterSchema()
        date_greater_than_filter_data = schema.dump(date_greater_than_filter)
        assert isinstance(date_greater_than_filter_data, dict)
        deserialized_date_greater_than_filter = date_greater_than_filter_manager.from_dict(date_greater_than_filter_data)
        assert isinstance(deserialized_date_greater_than_filter, DateGreaterThanFilter)
        assert deserialized_date_greater_than_filter.code == date_greater_than_filter.code
    @pytest.mark.asyncio
    async def test_add_bulk(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filters_data = [
            await DateGreaterThanFilterFactory.build_async(session) for _ in range(5)]
        date_greater_than_filters = await date_greater_than_filter_manager.add_bulk(date_greater_than_filters_data)
        assert len(date_greater_than_filters) == 5
        for updated_date_greater_than_filter in date_greater_than_filters:
            result = await session.execute(
                select(DateGreaterThanFilter).filter(
                    DateGreaterThanFilter._date_greater_than_filter_id == updated_date_greater_than_filter.date_greater_than_filter_id  # type: ignore
                )
            )
            fetched_date_greater_than_filter = result.scalars().first()
            assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
            assert str(fetched_date_greater_than_filter.insert_user_id) == (
                str(date_greater_than_filter_manager._session_context.customer_code))
            assert str(fetched_date_greater_than_filter.last_update_user_id) == (
                str(date_greater_than_filter_manager._session_context.customer_code))
            assert fetched_date_greater_than_filter.date_greater_than_filter_id == updated_date_greater_than_filter.date_greater_than_filter_id
    @pytest.mark.asyncio
    async def test_update_bulk_success(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Mocking date_greater_than_filter instances
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(session=session)
        logging.info(date_greater_than_filter1.__dict__)
        code_updated1 = uuid.uuid4()
        code_updated2 = uuid.uuid4()
        logging.info(code_updated1)
        logging.info(code_updated2)
        # Update date_greater_than_filters
        updates = [
            {
                "date_greater_than_filter_id": date_greater_than_filter1.date_greater_than_filter_id,
                "code": code_updated1
            },
            {
                "date_greater_than_filter_id": date_greater_than_filter2.date_greater_than_filter_id,
                "code": code_updated2
            }
        ]
        updated_date_greater_than_filters = await date_greater_than_filter_manager.update_bulk(updates)
        logging.info('bulk update results')
        # Assertions
        assert len(updated_date_greater_than_filters) == 2
        logging.info(updated_date_greater_than_filters[0].__dict__)
        logging.info(updated_date_greater_than_filters[1].__dict__)
        logging.info('getall')
        date_greater_than_filters = await date_greater_than_filter_manager.get_list()
        logging.info(date_greater_than_filters[0].__dict__)
        logging.info(date_greater_than_filters[1].__dict__)
        assert updated_date_greater_than_filters[0].code == code_updated1
        assert updated_date_greater_than_filters[1].code == code_updated2
        assert str(updated_date_greater_than_filters[0].last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        assert str(updated_date_greater_than_filters[1].last_update_user_id) == (
            str(date_greater_than_filter_manager._session_context.customer_code))
        result = await session.execute(
            select(DateGreaterThanFilter).filter(DateGreaterThanFilter._date_greater_than_filter_id == 1)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.code == code_updated1
        result = await session.execute(
            select(DateGreaterThanFilter).filter(DateGreaterThanFilter._date_greater_than_filter_id == 2)  # type: ignore
        )
        fetched_date_greater_than_filter = result.scalars().first()
        assert isinstance(fetched_date_greater_than_filter, DateGreaterThanFilter)
        assert fetched_date_greater_than_filter.code == code_updated2
    @pytest.mark.asyncio
    async def test_update_bulk_missing_date_greater_than_filter_id(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # No date_greater_than_filters to update since date_greater_than_filter_id is missing
        updates = [{"name": "Red Rose"}]
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_date_greater_than_filter_not_found(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Update date_greater_than_filters
        updates = [{"date_greater_than_filter_id": 1, "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_update_bulk_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        updates = [{"date_greater_than_filter_id": "2", "code": uuid.uuid4()}]
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.update_bulk(updates)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_success(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter2 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [date_greater_than_filter1.date_greater_than_filter_id, date_greater_than_filter2.date_greater_than_filter_id]
        result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        assert result is True
        for date_greater_than_filter_id in date_greater_than_filter_ids:
            execute_result = await session.execute(
                select(DateGreaterThanFilter).filter(
                    DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter_id)  # type: ignore
            )
            fetched_date_greater_than_filter = execute_result.scalars().first()
            assert fetched_date_greater_than_filter is None
    @pytest.mark.asyncio
    async def test_delete_bulk_date_greater_than_filters_not_found(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        assert isinstance(date_greater_than_filter1, DateGreaterThanFilter)
        # Delete date_greater_than_filters
        date_greater_than_filter_ids = [1, 2]
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_delete_bulk_empty_list(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
            #TODO add comment
        """
        # Delete date_greater_than_filters with an empty list
        date_greater_than_filter_ids = []
        result = await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        # Assertions
        assert result is True
    @pytest.mark.asyncio
    async def test_delete_bulk_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter_ids = ["1", 2]
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.delete_bulk(date_greater_than_filter_ids)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_count_basic_functionality(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(date_greater_than_filters_data, List)
        count = await date_greater_than_filter_manager.count()
        assert count == 5
    @pytest.mark.asyncio
    async def test_count_empty_database(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
            #TODO add comment
        """
        count = await date_greater_than_filter_manager.count()
        assert count == 0
    @pytest.mark.asyncio
    async def test_get_sorted_list_basic_sorting(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add date_greater_than_filters
        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(date_greater_than_filters_data, List)
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(
            sort_by="_date_greater_than_filter_id")
        assert [date_greater_than_filter.date_greater_than_filter_id for date_greater_than_filter in sorted_date_greater_than_filters] == (
            [(i + 1) for i in range(5)])
    @pytest.mark.asyncio
    async def test_get_sorted_list_descending_sorting(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add date_greater_than_filters
        date_greater_than_filters_data = (
            [await DateGreaterThanFilterFactory.create_async(session) for _ in range(5)])
        assert isinstance(date_greater_than_filters_data, List)
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(
            sort_by="date_greater_than_filter_id", order="desc")
        assert [date_greater_than_filter.date_greater_than_filter_id for date_greater_than_filter in sorted_date_greater_than_filters] == (
            [(i + 1) for i in reversed(range(5))])
    @pytest.mark.asyncio
    async def test_get_sorted_list_invalid_attribute(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        with pytest.raises(AttributeError):
            await date_greater_than_filter_manager.get_sorted_list(sort_by="invalid_attribute")
        await session.rollback()
    @pytest.mark.asyncio
    async def test_get_sorted_list_empty_database(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
            #TODO add comment
        """
        sorted_date_greater_than_filters = await date_greater_than_filter_manager.get_sorted_list(sort_by="date_greater_than_filter_id")
        assert len(sorted_date_greater_than_filters) == 0
    @pytest.mark.asyncio
    async def test_refresh_basic(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test the basic functionality of refreshing a date_greater_than_filter instance.
        This test performs the following steps:
        1. Creates a date_greater_than_filter instance using the DateGreaterThanFilterFactory.
        2. Retrieves the date_greater_than_filter from the database to ensure
            it was added correctly.
        3. Updates the date_greater_than_filter's code and verifies the update.
        4. Refreshes the original date_greater_than_filter instance and checks if
            it reflects the updated code.
        Args:
            date_greater_than_filter_manager (DateGreaterThanFilterManager): The manager responsible
                for date_greater_than_filter operations.
            session (AsyncSession): The SQLAlchemy asynchronous session.
        """
        # Add a date_greater_than_filter
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Retrieve the date_greater_than_filter from the database
        result = await session.execute(
            select(DateGreaterThanFilter).filter(
                DateGreaterThanFilter._date_greater_than_filter_id == date_greater_than_filter1.date_greater_than_filter_id)  # type: ignore
        )  # type: ignore
        date_greater_than_filter2 = result.scalars().first()
        # Verify that the retrieved date_greater_than_filter matches the added date_greater_than_filter
        assert date_greater_than_filter1.code == date_greater_than_filter2.code
        # Update the date_greater_than_filter's code
        updated_code1 = uuid.uuid4()
        date_greater_than_filter1.code = updated_code1
        updated_date_greater_than_filter1 = await date_greater_than_filter_manager.update(date_greater_than_filter1)
        # Verify that the updated date_greater_than_filter is of type DateGreaterThanFilter
        # and has the updated code
        assert isinstance(updated_date_greater_than_filter1, DateGreaterThanFilter)
        assert updated_date_greater_than_filter1.code == updated_code1
        # Refresh the original date_greater_than_filter instance
        refreshed_date_greater_than_filter2 = await date_greater_than_filter_manager.refresh(date_greater_than_filter2)
        # Verify that the refreshed date_greater_than_filter reflects the updated code
        assert refreshed_date_greater_than_filter2.code == updated_code1
    @pytest.mark.asyncio
    async def test_refresh_nonexistent_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        date_greater_than_filter = DateGreaterThanFilter(date_greater_than_filter_id=999)
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.refresh(date_greater_than_filter)
        await session.rollback()
    @pytest.mark.asyncio
    async def test_exists_with_existing_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a date_greater_than_filter
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Check if the date_greater_than_filter exists using the manager function
        assert await date_greater_than_filter_manager.exists(date_greater_than_filter1.date_greater_than_filter_id) is True
    @pytest.mark.asyncio
    async def test_is_equal_with_existing_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        # Add a date_greater_than_filter
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        date_greater_than_filter2 = await date_greater_than_filter_manager.get_by_id(date_greater_than_filter_id=date_greater_than_filter1.date_greater_than_filter_id)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter1, date_greater_than_filter2) is True
        date_greater_than_filter1_dict = date_greater_than_filter_manager.to_dict(date_greater_than_filter1)
        date_greater_than_filter3 = date_greater_than_filter_manager.from_dict(date_greater_than_filter1_dict)
        assert date_greater_than_filter_manager.is_equal(date_greater_than_filter1, date_greater_than_filter3) is True
    @pytest.mark.asyncio
    async def test_exists_with_nonexistent_date_greater_than_filter(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
            #TODO add comment
        """
        non_existent_id = 999
        assert await date_greater_than_filter_manager.exists(non_existent_id) is False
    @pytest.mark.asyncio
    async def test_exists_with_invalid_id_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
            #TODO add comment
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.exists(invalid_id)  # type: ignore  # noqa: E501
        await session.rollback()
# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @pytest.mark.asyncio
    async def test_get_by_pac_id_existing(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when a date_greater_than_filter with
        a specific pac_id exists.
        Steps:
        1. Create a date_greater_than_filter using the DateGreaterThanFilterFactory.
        2. Fetch the date_greater_than_filter using the
            `get_by_pac_id` method of the date_greater_than_filter_manager.
        3. Assert that the fetched date_greater_than_filters list contains
            only one date_greater_than_filter.
        4. Assert that the fetched date_greater_than_filter is an instance
            of the DateGreaterThanFilter class.
        5. Assert that the code of the fetched date_greater_than_filter
            matches the code of the created date_greater_than_filter.
        6. Fetch the corresponding pac object
            using the pac_id of the created date_greater_than_filter.
        7. Assert that the fetched pac object is
            an instance of the Pac class.
        8. Assert that the pac_code_peek of the fetched
            date_greater_than_filter matches the code of the fetched pac.
        """
        # Add a date_greater_than_filter with a specific pac_id
        date_greater_than_filter1 = await DateGreaterThanFilterFactory.create_async(session=session)
        # Fetch the date_greater_than_filter using the manager function
        fetched_date_greater_than_filters = await date_greater_than_filter_manager.get_by_pac_id(date_greater_than_filter1.pac_id)
        assert len(fetched_date_greater_than_filters) == 1
        assert isinstance(fetched_date_greater_than_filters[0], DateGreaterThanFilter)
        assert fetched_date_greater_than_filters[0].code == date_greater_than_filter1.code
        stmt = select(models.Pac).where(
            models.Pac._pac_id == date_greater_than_filter1.pac_id)  # type: ignore  # noqa: E501
        result = await session.execute(stmt)
        pac = result.scalars().first()
        assert isinstance(pac, models.Pac)
        assert fetched_date_greater_than_filters[0].pac_code_peek == pac.code
    @pytest.mark.asyncio
    async def test_get_by_pac_id_nonexistent(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager
    ):
        """
        Test case to verify the behavior of the
        get_by_pac_id method when the pac ID does not exist.
        This test case ensures that when a non-existent
        pac ID is provided to the get_by_pac_id method,
        an empty list is returned.
        """
        non_existent_id = 999
        fetched_date_greater_than_filters = await date_greater_than_filter_manager.get_by_pac_id(non_existent_id)
        assert len(fetched_date_greater_than_filters) == 0
    @pytest.mark.asyncio
    async def test_get_by_pac_id_invalid_type(
        self,
        date_greater_than_filter_manager: DateGreaterThanFilterManager,
        session: AsyncSession
    ):
        """
        Test case to verify the behavior of the
        `get_by_pac_id` method when an invalid pac ID is provided.
        Args:
            date_greater_than_filter_manager (DateGreaterThanFilterManager): An
                instance of the DateGreaterThanFilterManager class.
            session (AsyncSession): An instance
                of the AsyncSession class.
        Raises:
            Exception: If an exception is raised during
            the execution of the `get_by_pac_id` method.
        Returns:
            None
        """
        invalid_id = "invalid_id"
        with pytest.raises(Exception):
            await date_greater_than_filter_manager.get_by_pac_id(invalid_id)  # type: ignore
        await session.rollback()
# endset
