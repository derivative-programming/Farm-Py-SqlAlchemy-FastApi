# services/tests/encryption_test.py  # pylint: disable=duplicate-code

"""
This module contains unit tests for the encryption module.

The encryption module provides functions for encrypting and
decrypting messages using a specified encryption key.
"""

from services.encryption import encrypt_message, decrypt_message

ENCRYPTION_KEY_SECRET = "your_test_key_here"  # Use a test key


def test_encrypt_decrypt():
    """
    Test the encrypt_message and decrypt_message functions.

    This test encrypts a message using the encrypt_message function
    and then decrypts it using the decrypt_message function.
    It checks if the decrypted message matches the original message.
    """

    original_message = "Hello, World!"

    # Encrypt and then decrypt the message
    encrypted_message = encrypt_message(original_message)
    decrypted_message = decrypt_message(encrypted_message)

    # Check if the decrypted message matches the original
    assert decrypted_message == original_message


def test_empty_string():
    """
    Test encrypting and decrypting an empty string.

    This test encrypts an empty string using the encrypt_message
    function and then decrypts it using the decrypt_message function.
    It checks if the decrypted message matches the original empty string.
    """

    original_message = ""

    encrypted_message = encrypt_message(original_message)
    decrypted_message = decrypt_message(encrypted_message)

    assert decrypted_message == original_message
