from __future__ import unicode_literals
import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


def generate_rsa_key(nbits=2048):
    return RSA.generate(nbits)


def get_rsa_public_key(rsa_private_key):
    return rsa_private_key.publickey()


def export_key(key, passphrase=None):
    passphrase = isinstance(passphrase, str) and passphrase.encode("utf-8") or passphrase
    return key.exportKey(passphrase=passphrase).decode("utf-8")


def import_key(text, passphrase=None):
    text = isinstance(text, str) and text.encode("utf-8") or text
    passphrase = isinstance(passphrase, str) and passphrase.encode("utf-8") or passphrase
    return RSA.importKey(text, passphrase)


def rsa_encrypt_string(message, rsa_public_key):
    return base64.encodebytes(rsa_encrypt(message.encode("utf-8"), rsa_public_key)).decode("utf-8")


def rsa_encrypt(data, rsa_public_key):
    cipher = PKCS1_OAEP.new(rsa_public_key)
    return cipher.encrypt(data)


def rsa_decrypt_string(message, rsa_private_key):
    return rsa_decrypt(base64.decodebytes(message.encode("utf-8")), rsa_private_key).decode("utf-8")


def rsa_decrypt(data, rsa_private_key):
    cipher = PKCS1_OAEP.new(rsa_private_key)
    return cipher.decrypt(data)


def aes_password_clean(password):
    if isinstance(password, str):
        password = password.encode("utf-8")
    if len(password) in [16, 32]:
        return password
    return hashlib.md5(password).digest()


def aes_encrypt_string(message, password):
    key = aes_password_clean(password)
    message = message.encode("utf-8")
    return base64.encodebytes(aes_encrypt(message, key)).decode("utf-8")


def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext


def aes_decrypt_string(message, password):
    key = aes_password_clean(password)
    message = base64.decodebytes(message.encode("utf-8"))
    return aes_decrypt(message, key).decode("utf-8")


def aes_decrypt(data, key):
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def rsa_aes_encrypt_string(message, rsa_public_key):
    message = message.encode("utf-8")
    return base64.encodebytes(rsa_aes_encrypt(message, rsa_public_key)).decode("utf-8")


def rsa_aes_encrypt(data, rsa_public_key):
    session_key = get_random_bytes(32)
    session_key_secret = rsa_encrypt(session_key, rsa_public_key)
    data_secret = aes_encrypt(data, session_key)
    return session_key_secret + data_secret


def rsa_aes_decrypt_string(message, rsa_private_key):
    message = base64.decodebytes(message.encode("utf-8"))
    return rsa_aes_decrypt(message, rsa_private_key).decode("utf-8")


def rsa_aes_decrypt(data, rsa_private_key):
    session_key_secret = data[:256]
    data_secret = data[256:]
    session_key = rsa_decrypt(session_key_secret, rsa_private_key)
    return aes_decrypt(data_secret, session_key)


def rsa_sha256_sign_string(message, rsa_private_key):
    message = message.encode("utf-8")
    signature = rsa_sha256_sign(message, rsa_private_key)
    return base64.encodebytes(signature).decode("utf-8")


def rsa_sha256_sign(data, rsa_private_key):
    hash = SHA256.new(data)
    signer = PKCS1_v1_5.new(rsa_private_key)
    return signer.sign(hash)


def rsa_sha256_verify_string(message, signature, rsa_public_key):
    message = message.encode("utf-8")
    signature = base64.decodebytes(signature.encode("utf-8"))
    return rsa_sha256_verify(message, signature, rsa_public_key)


def rsa_sha256_verify(data, signature, rsa_public_key):
    hash = SHA256.new(data)
    verifier = PKCS1_v1_5.new(rsa_public_key)
    return verifier.verify(hash, signature)

