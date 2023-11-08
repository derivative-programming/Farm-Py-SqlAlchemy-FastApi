# api/models/factories.py
import uuid
import factory
from factory import Faker

from apis.models import TacRegisterPostModelRequest
from datetime import date, datetime
from decimal import Decimal
class TacRegisterPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = TacRegisterPostModelRequest
    email:str = Faker('email')
    password:str = Faker('sentence', nb_words=4)
    confirmPassword:str = Faker('sentence', nb_words=4)
    firstName:str = Faker('sentence', nb_words=4)
    lastName:str = Faker('sentence', nb_words=4)
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)

