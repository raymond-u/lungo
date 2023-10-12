from datetime import datetime, timedelta
from os import PathLike
from secrets import token_urlsafe

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ..app.state import file_utils
from ..core.constants import APP_NAME_CAPITALIZED


def generate_self_signed_cert(cert_file: str | PathLike[str], key_file: str | PathLike[str]) -> None:
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

    file_utils().write_bytes(cert_file, cert_pem)
    file_utils().write_bytes(key_file, key_pem)


def generate_random_string() -> str:
    """Generate a random string."""
    return token_urlsafe(64)
