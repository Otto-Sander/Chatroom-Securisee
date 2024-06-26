from Cryptodome.Cipher import AES
import base64

def generate_aes_key():
    """ Generate a random 256-bit AES key for encryption """
    return AES.get_random_bytes(32)  # Génère une clé AES de 256 bits

def aes_encrypt(message, key):
    """ Encrypt a message using AES encryption with EAX mode. """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def aes_decrypt(encrypted_message, key):
    """ Decrypt a message using AES encryption with EAX mode. """
    encrypted_message = base64.b64decode(encrypted_message)
    nonce, tag, ciphertext = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        raise ValueError("Incorrect decryption")
    return decrypted_message.decode('utf-8')
