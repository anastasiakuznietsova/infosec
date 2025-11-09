from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from config import PUBLIC_EXPONENT_RSA, KEY_SIZE_RSA


def get_private_key(password):
    privt_key = generate_private_key(PUBLIC_EXPONENT_RSA, KEY_SIZE_RSA)
    prvt_ser_pem = privt_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    return prvt_ser_pem

def get_public_key(pemlines, password):
    private_key = serialization.load_pem_private_key(pemlines, password)
    publc_key = private_key.public_key()
    pblc_ser_pem = publc_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pblc_ser_pem

def get_encryption_rsa(pemlines, input_bits):
    encrypt_input=[]
    encrypt_output = []
    publc_key = serialization.load_pem_public_key(pemlines)

    key_size_bytes = publc_key.key_size // 8
    max_chunk_size = key_size_bytes - 2 * 32 - 2

    if len(input_bits)<=max_chunk_size:
        encrypt_input.append(input_bits)
    else:
        for i in range(0,len(input_bits),max_chunk_size):
            encrypt_input.append(input_bits[i:i+max_chunk_size])
    for line in encrypt_input:
        encrypt_output.append(publc_key.encrypt(
            line,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None)
            )
        )
    return encrypt_output

def get_decrypted_rsa(pemlines,ciphertext,password):
    decrypt_input = []
    decrypt_output = []
    privt_key = serialization.load_pem_private_key(pemlines, password)
    key_size_bytes = privt_key.key_size // 8
    if len(ciphertext)<=key_size_bytes:
        decrypt_input.append(ciphertext)
    else:
        for i in range(0,len(ciphertext),key_size_bytes):
            decrypt_input.append(ciphertext[i:i+key_size_bytes])
    for line in decrypt_input:
         decrypt_output.append(privt_key.decrypt(
            line,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
         )
    )
    return decrypt_output