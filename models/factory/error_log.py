# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import ErrorLog
from .pac import PacFactory #pac_id
class ErrorLogFactory(factory.Factory):
    class Meta:
        model = ErrorLog
    browser_code = factory.LazyFunction(uuid.uuid4)
    context_code = factory.LazyFunction(uuid.uuid4)
    created_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    description = Faker('sentence', nb_words=4)
    is_client_side_error = Faker('boolean')
    is_resolved = Faker('boolean')
    pac = SubFactory(PacFactory, session=factory.SelfAttribute('..session')) #pac_id
    url = Faker('sentence', nb_words=4)
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
