# api/models/factories.py
import uuid
import factory
from factory import Faker

from apis.models import PlantUserPropertyRandomUpdatePostModelRequest
from datetime import date, datetime
from decimal import Decimal
class PlantUserPropertyRandomUpdatePostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PlantUserPropertyRandomUpdatePostModelRequest

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)

