"""Authentication utilities for Polymarket US API."""

import base64
import time

from nacl.signing import SigningKey


def create_auth_headers(
    key_id: str,
    secret_key: str,
    method: str,
    path: str,
) -> dict[str, str]:
    """Create authentication headers for API requests.

    Args:
        key_id: The API key ID (UUID)
        secret_key: Base64-encoded Ed25519 private key
        method: HTTP method (GET, POST, etc.)
        path: Request path (e.g., /v1/orders)

    Returns:
        Dict with X-PM-Access-Key, X-PM-Timestamp, and X-PM-Signature headers
    """
    timestamp = str(int(time.time() * 1000))
    message = f"{timestamp}{method}{path}"

    # Decode secret key from base64
    secret_key_bytes = base64.b64decode(secret_key)

    # Ed25519 expects 32-byte seed; if 64-byte key provided, use first 32 bytes
    if len(secret_key_bytes) == 64:
        secret_key_bytes = secret_key_bytes[:32]

    signing_key = SigningKey(secret_key_bytes)
    signed = signing_key.sign(message.encode())
    signature_b64 = base64.b64encode(signed.signature).decode()

    return {
        "X-PM-Access-Key": key_id,
        "X-PM-Timestamp": timestamp,
        "X-PM-Signature": signature_b64,
    }
