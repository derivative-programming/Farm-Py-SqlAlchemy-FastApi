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
        return encrypt_message(value) if value is not None else None

    def process_result_value(self, value, dialect):
        """
        Decrypts the value retrieved from the database.

        Args:
            value: The value retrieved from the database.
            dialect: The SQLAlchemy dialect.

        Returns:
            The decrypted value.
        """
        return decrypt_message(value) if value is not None else None

    def process_literal_param(self, value, dialect):
        """
        Processes a literal parameter value.

        Args:
            value: The literal parameter value.
            dialect: The SQLAlchemy dialect.

        Returns:
            The processed value.
        """
        # Implement as needed or remove if not required
        return value

    @property
    def python_type(self):
        """
        Returns the Python type for this type decorator.

        Returns:
            The Python type.
        """
        return bytes
