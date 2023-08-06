import base64

from .models import RsaKey
from .utils import rsa_encrypt_string as raw_rsa_encrypt_string
from .utils import rsa_decrypt_string as raw_rsa_decrypt_string
from .utils import aes_encrypt_string as raw_aes_encrypt_string
from .utils import aes_decrypt_string as raw_aes_decrypt_string
from .utils import rsa_aes_encrypt_string as raw_rsa_aes_encrypt_string
from .utils import rsa_aes_decrypt_string as raw_rsa_aes_decrypt_string
from .utils import rsa_sha256_sign_string as raw_rsa_sha256_sign_string
from .utils import rsa_sha256_verify_string as raw_rsa_sha256_verify_string


def generate_rsa_key(nbits, name, title=None):
    key = RsaKey()
    key.name = name
    key.title = title
    key.nbits = nbits
    key.save()
    return key


def rsa_encrypt_string(message, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_encrypt_string(message, rsa_key.rsa_public_key)


def rsa_decrypt_string(message, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_decrypt_string(message, rsa_key.rsa_private_key)


def aes_encrypt_string(message, password):
    return raw_aes_encrypt_string(message, password)


def aes_decrypt_string(message, password):
    return raw_aes_decrypt_string(message, password)


def rsa_aes_encrypt_string(message, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_aes_encrypt_string(message, rsa_key.rsa_public_key)


def rsa_aes_decrypt_string(message, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_aes_decrypt_string(message, rsa_key.rsa_private_key)


def rsa_sha256_sign_string(message, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_sha256_sign_string(message, rsa_key.rsa_private_key)


def rsa_sha256_verify_string(data, signature, name):
    rsa_key = RsaKey.objects.get(name=name)
    return raw_rsa_sha256_verify_string(data, signature, rsa_key.rsa_public_key)
