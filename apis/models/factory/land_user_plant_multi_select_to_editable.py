# apis/models/factory/land_user_plant_multi_select_to_editable.py
# pylint: disable=unused-import
"""
Factory module for creating instances of LandUserPlantMultiSelectToEditablePostModelRequest with
various field values for testing.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequest
class LandUserPlantMultiSelectToEditablePostModelRequestFactory(factory.base.Factory):
    """
    Factory class for LandUserPlantMultiSelectToEditablePostModelRequest. Generates
    instances with randomized field values for testing.
    """
    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = LandUserPlantMultiSelectToEditablePostModelRequest
    force_error_message = ""
    plant_code_list_csv = ""
# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        """
        Build method for the factory. If a session is provided,
        it uses the session to create related objects.
        Args:
            model_class: The model class to be instantiated.
            session: The database session to be used for related
                object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of LandUserPlantMultiSelectToEditablePostModelRequest.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(
        cls, model_class, session=None, *args, **kwargs
    ) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        """
        Create method for the factory. Uses the session to
        create related objects and persists the instance.
        Args:
            model_class: The model class to be instantiated.
            session: The database session to be used for related
                object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of LandUserPlantMultiSelectToEditablePostModelRequest.
        """

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.
        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of LandUserPlantMultiSelectToEditablePostModelRequest.
        """

# endset

# endset
        obj = LandUserPlantMultiSelectToEditablePostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

