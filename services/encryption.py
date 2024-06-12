# services/encryption.py

"""
    #TODO add comment
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from config import ENCRYPTION_KEY_SECRET


def encrypt_message(message):
    """
        #TODO add comment
    """
    password = ENCRYPTION_KEY_SECRET

    # Hash the password to create a key
    key = hashlib.sha256(password.encode()).digest()

    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Create a Cipher object using the key and IV
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend())

    # Pad the message and then encrypt
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_message


def decrypt_message(encrypted_message):
    """
        #TODO add comment
    """
    password = ENCRYPTION_KEY_SECRET

    # Hash the password to create a key
    key = hashlib.sha256(password.encode()).digest()

    # Extract the IV (first 16 bytes)
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]

    # Create a Cipher object using the key and IV
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend())

    # Decrypt and then unpad the message
    decryptor = cipher.decryptor()
    decrypted_padded_message = (
        decryptor.update(encrypted_message) + decryptor.finalize())

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = (
        unpadder.update(decrypted_padded_message) + unpadder.finalize())

    return decrypted_message.decode()
