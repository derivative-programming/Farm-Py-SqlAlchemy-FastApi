# farm/models/factories.py
import uuid
import factory 
from factory import Faker
from django.utils import timezone
from models.factory import FlavorFactory #requestFlavorCode
from apis.models import LandPlantListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
class LandPlantListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandPlantListGetModelRequest
    flavorCode:uuid = factory.LazyFunction(lambda: (FlavorFactory.create()).code)
    someIntVal:int = Faker('random_int')
    someBigIntVal:int = Faker('random_int')
    someFloatVal:float = Faker('pyfloat', positive=True)
    someBitVal:bool = Faker('boolean')
    isEditAllowed:bool = Faker('boolean')
    isDeleteAllowed:bool = Faker('boolean')
    someDecimalVal:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    someMinUTCDateTimeVal:datetime = factory.LazyFunction(datetime.datetime.utcnow)
    someMinDateVal:date = Faker('date_object')
    someMoneyVal:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    someNVarCharVal:str = Faker('sentence', nb_words=4)
    someVarCharVal:str = Faker('sentence', nb_words=4)
    someTextVal:str = Faker('text')
    somePhoneNumber:str = Faker('sentence', nb_words=4)
    someEmailAddress:str = Faker('sentence', nb_words=4)
    pageNumber = 1
    itemCountPerPage = 1
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)
