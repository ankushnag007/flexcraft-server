import base64
import secrets

from slugify import slugify


def generate_invite_code(domain, length=8):
    return (
        domain
        + base64.urlsafe_b64encode(secrets.token_bytes(6)).decode("utf-8")[:length]
    )


def generate_unique_company_id(name: str, domain: str) -> str:
    return slugify(f"{name}-{domain}")
