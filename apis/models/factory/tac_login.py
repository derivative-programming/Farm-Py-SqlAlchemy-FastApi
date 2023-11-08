# api/models/factories.py
import uuid
import factory
from factory import Faker

from apis.models import TacLoginPostModelRequest
from datetime import date, datetime
from decimal import Decimal
class TacLoginPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = TacLoginPostModelRequest
    email:str = Faker('email')
    password:str = Faker('sentence', nb_words=4)
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)

