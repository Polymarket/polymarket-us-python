"""Tests for authentication."""

from polymarket_us.auth import create_auth_headers


class TestCreateAuthHeaders:
    """Tests for create_auth_headers."""

    def test_creates_required_headers(self) -> None:
        """Should create all required headers."""
        # 32-byte key, base64 encoded
        secret_key = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
        headers = create_auth_headers(
            key_id="test-key-id",
            secret_key=secret_key,
            method="GET",
            path="/v1/orders",
        )
        assert "X-PM-Access-Key" in headers
        assert "X-PM-Timestamp" in headers
        assert "X-PM-Signature" in headers

    def test_access_key_matches_key_id(self) -> None:
        """Should set access key to key_id."""
        secret_key = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
        headers = create_auth_headers(
            key_id="my-key-id",
            secret_key=secret_key,
            method="POST",
            path="/v1/orders",
        )
        assert headers["X-PM-Access-Key"] == "my-key-id"

    def test_timestamp_is_numeric_string(self) -> None:
        """Should have numeric timestamp."""
        secret_key = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
        headers = create_auth_headers(
            key_id="test",
            secret_key=secret_key,
            method="GET",
            path="/v1/test",
        )
        timestamp = headers["X-PM-Timestamp"]
        assert timestamp.isdigit()
        # Should be a reasonable timestamp (in milliseconds)
        assert len(timestamp) >= 13

    def test_signature_is_base64(self) -> None:
        """Should have base64 signature."""
        import base64

        secret_key = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A="
        headers = create_auth_headers(
            key_id="test",
            secret_key=secret_key,
            method="GET",
            path="/v1/test",
        )
        signature = headers["X-PM-Signature"]
        # Should decode without error
        decoded = base64.b64decode(signature)
        # Ed25519 signatures are 64 bytes
        assert len(decoded) == 64

    def test_handles_64_byte_key(self) -> None:
        """Should handle 64-byte keys (uses first 32 bytes)."""
        # 64-byte key (seed + public key), base64 encoded
        secret_key_64 = "nWGxne/9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A=" * 2
        # Should not raise
        headers = create_auth_headers(
            key_id="test",
            secret_key=secret_key_64[:88],  # 64 bytes in base64
            method="GET",
            path="/v1/test",
        )
        assert "X-PM-Signature" in headers
