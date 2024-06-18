# base.py

"""
    #TODO add comment
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator, LargeBinary
from services.encryption import encrypt_message, decrypt_message

Base = declarative_base()


class EncryptedType(TypeDecorator):
    """
    #TODO add comment
    """
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = encrypt_message(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = decrypt_message(value)
        return value
