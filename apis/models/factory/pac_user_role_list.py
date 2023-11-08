# farm/models/factories.py
import uuid
import factory
from factory import Faker

from apis.models import PacUserRoleListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
class PacUserRoleListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PacUserRoleListGetModelRequest

    pageNumber = 1
    itemCountPerPage = 1
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)
