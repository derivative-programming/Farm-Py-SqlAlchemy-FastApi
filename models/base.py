# base.py

"""
This module contains the base classes and types for the SQLAlchemy models.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator, LargeBinary
from services.encryption import encrypt_message, decrypt_message

Base = declarative_base()


class EncryptedType(TypeDecorator):
    """
    A custom SQLAlchemy type decorator for encrypting and decrypting values.

    This type decorator encrypts the value before storing it in the database
    and decrypts it when retrieving it from the database.
    """
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        """
        Encrypts the value before storing it in the database.

        Args:
            value: The value to be encrypted.
            dialect: The SQLAlchemy dialect.

        Returns:
            The encrypted value.
        """
        if value is not None:
            value = encrypt_message(value)
        return value

    def process_result_value(self, value, dialect):
        """
        Decrypts the value retrieved from the database.

        Args:
            value: The value retrieved from the database.
            dialect: The SQLAlchemy dialect.

        Returns:
            The decrypted value.
        """
        if value is not None:
            value = decrypt_message(value)
        return value
