# api/models/factories.py
import uuid
import factory 
from factory import Faker 
from models.factory import FlavorFactory #requestFlavorCode
from apis.models import LandAddPlantPostModelRequest
from datetime import date, datetime
from decimal import Decimal
class LandAddPlantPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandAddPlantPostModelRequest
    requestFlavorCode:uuid = factory.LazyFunction(lambda: (FlavorFactory.create()).code)
    requestOtherFlavor:str = ""
    requestSomeIntVal:int = Faker('random_int')
    requestSomeBigIntVal:int = Faker('random_int')
    requestSomeBitVal:bool = Faker('boolean')
    requestIsEditAllowed:bool = Faker('boolean')
    requestIsDeleteAllowed:bool = Faker('boolean')
    requestSomeFloatVal:float = Faker('pyfloat', positive=True)
    requestSomeDecimalVal:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    requestSomeUTCDateTimeVal:datetime = factory.LazyFunction(datetime.datetime.utcnow)
    requestSomeDateVal:date = Faker('date_object')
    requestSomeMoneyVal:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    requestSomeNVarCharVal:str = Faker('sentence', nb_words=4)
    requestSomeVarCharVal:str = Faker('sentence', nb_words=4)
    requestSomeTextVal:str = Faker('text')
    requestSomePhoneNumber:str = Faker('phone_number')
    requestSomeEmailAddress:str = Faker('email')
    requestSampleImageUploadFile:str = ""
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create to use the dataclass's constructor."""
        return model_class(*args, **kwargs)


