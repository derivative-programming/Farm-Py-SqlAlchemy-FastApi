from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY_SECRET


def encrypt_message(message):
    """Encrypt a message using the provided key."""
    fernet = Fernet(ENCRYPTION_KEY_SECRET)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    """Decrypt a message using the provided key."""
    fernet = Fernet(ENCRYPTION_KEY_SECRET)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message