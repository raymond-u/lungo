from datetime import datetime, timedelta
from secrets import token_hex

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ..core.constants import APP_NAME_CAPITALIZED


def generate_self_signed_cert() -> tuple[bytes, bytes]:
    """Generate a self-signed certificate."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    name = x509.Name([x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, APP_NAME_CAPITALIZED)])
    serial_number = x509.random_serial_number()
    now = datetime.utcnow()
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

    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem


def generate_random_hex() -> str:
    """Generate a random hex string."""
    return token_hex(32)
