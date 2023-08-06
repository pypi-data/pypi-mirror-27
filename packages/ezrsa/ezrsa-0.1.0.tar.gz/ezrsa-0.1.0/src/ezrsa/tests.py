import os
import string
import random
from django.test import TestCase



class TestEzrsa(TestCase):
    def test_0101(self):
        from .utils import generate_rsa_key
        from .utils import get_rsa_public_key
        from .utils import export_key
        from .utils import import_key
        from .utils import rsa_encrypt
        from .utils import rsa_decrypt
        from .utils import rsa_encrypt_string
        from .utils import rsa_decrypt_string
        from .utils import rsa_sha256_sign
        from .utils import rsa_sha256_verify
        from .utils import rsa_sha256_sign_string
        from .utils import rsa_sha256_verify_string

        sk1 = generate_rsa_key(2048)
        pk1 = get_rsa_public_key(sk1)
        sks = export_key(sk1, 'hello')
        pks = export_key(pk1)
        sk2 = import_key(sks, 'hello')
        pk2 = import_key(pks)
        assert sk1 == sk2
        assert sk2 == sk2

        data1 = os.urandom(214)
        data2 = rsa_encrypt(data1, pk1)
        data3 = rsa_decrypt(data2, sk1)
        assert data1 == data3

        chars = list((string.printable * 3)[:214])
        random.shuffle(chars)
        message1 = "".join(chars)
        message2 = rsa_encrypt_string(message1, pk1)
        message3 = rsa_decrypt_string(message2, sk1)
        assert message1 == message3

        data = os.urandom(1024)
        sig = rsa_sha256_sign(data, sk1)
        assert rsa_sha256_verify(data, sig, pk1) == True

        data = string.printable * 30
        sig = rsa_sha256_sign_string(data, sk1)
        assert rsa_sha256_verify_string(data, sig, pk1) == True

    def test_0102(self):
        from .utils import aes_encrypt
        from .utils import aes_decrypt
        from .utils import aes_encrypt_string
        from .utils import aes_decrypt_string
        key = os.urandom(32)
        data1 = os.urandom(1024)
        data2 = aes_encrypt(data1, key)
        data3 = aes_decrypt(data2, key)
        assert data1 == data3

        key = "hello"
        message1 = string.printable * 32
        message2 = aes_encrypt_string(message1, key)
        message3 = aes_decrypt_string(message2, key)
        assert message1 == message3

    def test_0103(self):
        from .utils import generate_rsa_key
        from .utils import get_rsa_public_key
        from .utils import rsa_aes_encrypt
        from .utils import rsa_aes_decrypt
        from .utils import rsa_aes_decrypt
        from .utils import rsa_aes_encrypt_string
        from .utils import rsa_aes_decrypt_string
        sk1 = generate_rsa_key(2048)
        pk1 = get_rsa_public_key(sk1)

        data1 = os.urandom(1024)
        data2 = rsa_aes_encrypt(data1, pk1)
        data3 = rsa_aes_decrypt(data2, sk1)
        assert data1 == data3

        message1 = string.printable * 64
        message2 = rsa_aes_encrypt_string(message1, pk1)
        message2 = rsa_aes_decrypt_string(message2, sk1)
        assert message1 == message2

    def test_0201(self):
        from .services import generate_rsa_key
        from .services import rsa_encrypt_string
        from .services import rsa_decrypt_string
        from .services import aes_encrypt_string
        from .services import aes_decrypt_string
        from .services import rsa_aes_encrypt_string
        from .services import rsa_aes_decrypt_string
        from .services import rsa_sha256_sign_string
        from .services import rsa_sha256_verify_string

        key_name = "test01_20171220184300"
        key = generate_rsa_key(2048, key_name)

        message1 = "a" * 100
        message2 = rsa_encrypt_string(message1, key_name)
        message3 = rsa_decrypt_string(message2, key_name)
        assert message1 == message3

        message1 = string.printable * 30
        message2 = aes_encrypt_string(message1, key_name)
        message3 = aes_decrypt_string(message2, key_name)
        assert message1 == message3

        message1 = string.printable * 30
        message2 = rsa_aes_encrypt_string(message1, key_name)
        message3 = rsa_aes_decrypt_string(message2, key_name)
        assert message1 == message3

        message1 = string.printable * 30
        sig = rsa_sha256_sign_string(message1, key_name)
        assert rsa_sha256_verify_string(message1, sig, key_name)
