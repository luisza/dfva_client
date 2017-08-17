'''
Created on 3 ago. 2017

@author: luis
'''


from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import io
import hashlib
from base64 import b64decode, b64encode


def pem_to_base64(certificate):
    return certificate.replace("-----BEGIN CERTIFICATE-----\n", '').replace(
        '\n-----END CERTIFICATE-----', ''
    ).replace('\n', '')


def get_digest(digest_name):
    if 'sha256' == digest_name:
        return hashlib.sha256()
    elif 'sha384' == digest_name:
        return hashlib.sha384()
    elif 'sha512' == digest_name:
        return hashlib.sha512()


def get_hash_sum(data, algorithm):
    if type(data) == str:
        data = data.encode()
    digest = get_digest(algorithm)
    digest.update(data)
    hashsum = digest.hexdigest()
    return hashsum


def encrypt(session_key, encypted_key, message):
    if type(message) == str:
        message = message.encode('utf-8')

    file_out = io.BytesIO()
    # Encrypt the session key with the public RSA key

    file_out.write(encypted_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)
    [file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]

    file_out.seek(0)

    return b64encode(file_out.read())
