# services/tests/encryption_test.py

"""
    #TODO add comment
"""
 
from services.encryption import encrypt_message, decrypt_message

ENCRYPTION_KEY_SECRET = "your_test_key_here"  # Use a test key


def test_encrypt_decrypt():
    original_message = "Hello, World!"

    # Encrypt and then decrypt the message
    encrypted_message = encrypt_message(original_message)
    decrypted_message = decrypt_message(encrypted_message)

    # Check if the decrypted message matches the original
    assert decrypted_message == original_message


def test_empty_string():
    original_message = ""

    encrypted_message = encrypt_message(original_message)
    decrypted_message = decrypt_message(encrypted_message)

    assert decrypted_message == original_message
