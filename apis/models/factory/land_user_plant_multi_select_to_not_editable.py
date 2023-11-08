# api/models/factories.py
import uuid
import factory
from factory import Faker

from apis.models import LandUserPlantMultiSelectToNotEditablePostModelRequest
from datetime import date, datetime
from decimal import Decimal
class LandUserPlantMultiSelectToNotEditablePostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest
    plantCodeListCsv:str = ""
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)

