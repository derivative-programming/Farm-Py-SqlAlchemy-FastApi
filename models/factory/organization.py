# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Organization
from .tac import TacFactory #tac_id
class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization
    name = Faker('sentence', nb_words=4)
    tac = SubFactory(TacFactory, session=factory.SelfAttribute('..session')) #tac_id
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
