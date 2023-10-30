# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Land
from .pac import PacFactory #pac_id
class LandFactory(factory.Factory):
    class Meta:
        model = Land
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    pac = SubFactory(PacFactory, session=factory.SelfAttribute('..session')) #pac_id
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
