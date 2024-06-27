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
    try:
        encrypted_message = base64.b64decode(encrypted_message)
        nonce, tag, ciphertext = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_message.decode('utf-8')
    except (ValueError, KeyError) as e:
        raise ValueError(f"Incorrect decryption: {e}")

# if __name__ == "__main__":
#     # Test simple pour vérifier le chiffrement et le déchiffrement
#     key = generate_aes_key()
#     message = "This is a secret message"
#     print(message)
#     encrypted_message = aes_encrypt(message, key)
#     print(f"Encrypted: {encrypted_message}")
#
#     decrypted_message = aes_decrypt(encrypted_message, key)
#     print(f"Decrypted: {decrypted_message}")
#
#     assert message == decrypted_message, "Le message déchiffré ne correspond pas au message original"
#     print("Test réussi !")
