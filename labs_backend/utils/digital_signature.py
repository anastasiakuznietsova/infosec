from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def pad_data(b_data):
    chosen_hash = hashes.SHA256()
    hasher = hashes.Hash(chosen_hash)
    hasher.update(b_data)
    digest = hasher.finalize()
    return digest

def signature_get_private_key():
    private_key = ec.generate_private_key(
        ec.SECP384R1()
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key_pem

def signature_get_public_key(pem_bytes):
    private_key = serialization.load_pem_private_key(
        pem_bytes,
        password=None
    )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem

def get_signature(pem_bytes,data):
    private_key = serialization.load_pem_private_key(
        pem_bytes,
        password=None
    )
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature_okay(digest,signature,pem_bytes):
    public_key = serialization.load_pem_public_key(
        pem_bytes
    )
    try:
        public_key.verify(signature, digest, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
