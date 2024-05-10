import hashlib
from datetime import datetime, timedelta, UTC
from secrets import token_hex
from typing import BinaryIO

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

from ..core.constants import APP_NAME_CAPITALIZED


def generate_raw_ed25519_keypair() -> tuple[bytes, bytes]:
    """Generate a raw Ed25519 keypair."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return public_key_bytes, private_key_bytes


def generate_self_signed_cert() -> tuple[bytes, bytes]:
    """Generate a self-signed certificate."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    name = x509.Name([x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, APP_NAME_CAPITALIZED)])
    serial_number = x509.random_serial_number()
    now = datetime.now(UTC)
    basic_constraints = x509.BasicConstraints(ca=True, path_length=0)

    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(serial_number)
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=36500))
        .add_extension(basic_constraints, False)
        .sign(key, hashes.SHA256(), default_backend())
    )

    cert_bytes = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_bytes, key_bytes


def generate_random_hex() -> str:
    """Generate a random hex string."""
    return token_hex(32)


def hash_stream(f: BinaryIO) -> str:
    """Hash a stream using SHA-256."""
    return hashlib.file_digest(f, "sha256").hexdigest()


def hash_text(text: str) -> str:
    """Hash a text using SHA-256."""
    return hashlib.sha256(text.encode()).hexdigest()
