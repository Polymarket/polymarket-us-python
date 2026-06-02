"""Retry helpers shared by the sync and async clients.

The Polymarket US API does not return ``Retry-After`` or ``X-RateLimit-*``
headers, so backoff is computed client-side with exponential growth and jitter.
Only idempotent methods are retried automatically: order placement and other
``POST`` requests are never retried because the API has no idempotency key, so a
retry after a partial failure could submit a duplicate order.
"""

from __future__ import annotations

import random

DEFAULT_MAX_RETRIES = 2

# Status codes that are safe to retry for idempotent requests.
RETRYABLE_STATUS_CODES = frozenset({408, 409, 429, 500, 502, 503, 504})

# Methods without side effects, safe to retry on transient failures.
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "DELETE"})

_BACKOFF_INITIAL_SECONDS = 0.5
_BACKOFF_MAX_SECONDS = 8.0


def is_retryable_status(status_code: int) -> bool:
    """Return whether a response status code is safe to retry."""
    return status_code in RETRYABLE_STATUS_CODES


def can_retry_method(method: str) -> bool:
    """Return whether a request method is safe to retry automatically."""
    return method.upper() in IDEMPOTENT_METHODS


def backoff_delay(attempt: int, retry_after: float | None = None) -> float:
    """Compute the delay before the next retry attempt (0-indexed).

    Honors an explicit ``Retry-After`` value when present (clamped to
    ``_BACKOFF_MAX_SECONDS`` so a hostile or malformed header cannot make the
    client sleep indefinitely); otherwise applies exponential backoff with equal
    jitter to avoid thundering-herd retries.
    """
    if retry_after is not None and retry_after >= 0:
        return min(retry_after, _BACKOFF_MAX_SECONDS)
    capped = min(_BACKOFF_INITIAL_SECONDS * (2**attempt), _BACKOFF_MAX_SECONDS)
    return capped / 2 + random.random() * (capped / 2)


def retry_after_seconds(header_value: str | None) -> float | None:
    """Parse a ``Retry-After`` header expressed in seconds, if present."""
    if not header_value:
        return None
    try:
        return float(header_value)
    except ValueError:
        return None
