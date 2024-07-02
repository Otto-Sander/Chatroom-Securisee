from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, AES
import base64


def generate_rsa_keys():
    try :
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
    except Exception as e:
        print(f"Error generating RSA keys: {e}")
        return None, None
    return private_key, public_key


def rsa_encrypt(message, public_key):
    try :
        rsa_public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_public_key)
        encrypted_message = cipher.encrypt(message)
    except Exception as e:
        print(f"Error encrypting message: {e}")
        return None
    return base64.b64encode(encrypted_message)


def rsa_decrypt(encrypted_message, private_key):
    try:
        rsa_private_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_private_key)
        decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    except Exception as e:
        print(f"Error decrypting message: {e}")
        return None
    return decrypted_message
