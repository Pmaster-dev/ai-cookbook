"""Tests for codec/claim_check.py — ClaimCheckCodec encode/decode."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from temporalio.api.common.v1 import Payload
from codec.claim_check import ClaimCheckCodec


def _make_payload(data: bytes, metadata: dict[str, bytes] | None = None) -> Payload:
    return Payload(data=data, metadata=metadata or {})


def _mock_s3_client():
    """Create a mock S3 client that works as an async context manager."""
    s3 = AsyncMock()
    s3.head_bucket = AsyncMock()
    s3.put_object = AsyncMock()

    # For get_object, return a mock with an async Body.read()
    body = AsyncMock()
    body.read = AsyncMock()
    s3.get_object = AsyncMock(return_value={"Body": body})

    return s3, body


def _mock_session(s3_client):
    """Create a mock aioboto3 session whose .client() yields s3_client."""
    session = MagicMock()
    ctx = AsyncMock()
    ctx.__aenter__ = AsyncMock(return_value=s3_client)
    ctx.__aexit__ = AsyncMock(return_value=False)
    session.client = MagicMock(return_value=ctx)
    return session


class TestEncodeSmallPayloads:
    @pytest.mark.asyncio
    async def test_small_payload_passes_through(self):
        codec = ClaimCheckCodec(max_inline_bytes=1024)
        s3, _ = _mock_s3_client()
        codec.session = _mock_session(s3)

        small_payload = _make_payload(b"small data")
        result = await codec.encode([small_payload])

        assert len(result) == 1
        # Small payload should pass through unchanged (no claim-check metadata)
        assert result[0].data == b"small data"
        s3.put_object.assert_not_called()


class TestEncodeLargePayloads:
    @pytest.mark.asyncio
    async def test_large_payload_is_claim_checked(self):
        codec = ClaimCheckCodec(max_inline_bytes=10)
        s3, _ = _mock_s3_client()
        codec.session = _mock_session(s3)

        large_payload = _make_payload(b"x" * 100)
        result = await codec.encode([large_payload])

        assert len(result) == 1
        assert result[0].metadata.get("temporal.io/claim-check-codec") == b"v1"
        s3.put_object.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_large_payloads_concurrently_encoded(self):
        codec = ClaimCheckCodec(max_inline_bytes=10)
        s3, _ = _mock_s3_client()
        codec.session = _mock_session(s3)

        p1 = _make_payload(b"x" * 100)
        p2 = _make_payload(b"y" * 100)
        result = await codec.encode([p1, p2])

        assert len(result) == 2
        assert result[0].metadata.get("temporal.io/claim-check-codec") == b"v1"
        assert result[1].metadata.get("temporal.io/claim-check-codec") == b"v1"
        assert s3.put_object.call_count == 2


class TestDecodeNonClaimChecked:
    @pytest.mark.asyncio
    async def test_non_claim_checked_passes_through(self):
        codec = ClaimCheckCodec()
        s3, _ = _mock_s3_client()
        codec.session = _mock_session(s3)

        payload = _make_payload(b"regular data", metadata={"encoding": b"json/plain"})
        result = await codec.decode([payload])

        assert len(result) == 1
        assert result[0].data == b"regular data"
        s3.get_object.assert_not_called()


class TestDecodeClaimChecked:
    @pytest.mark.asyncio
    async def test_claim_checked_payload_decoded(self):
        codec = ClaimCheckCodec(max_inline_bytes=10)
        s3, body = _mock_s3_client()
        codec.session = _mock_session(s3)

        # Create the original payload and serialize it as S3 would store it
        original = _make_payload(b"original large data")
        serialized = original.SerializeToString()
        body.read.return_value = serialized

        claim_check_payload = _make_payload(
            b"some-uuid-key",
            metadata={
                "encoding": b"claim-checked",
                "temporal.io/claim-check-codec": b"v1",
            },
        )
        result = await codec.decode([claim_check_payload])

        assert len(result) == 1
        assert result[0].data == b"original large data"

    @pytest.mark.asyncio
    async def test_multiple_claim_checked_payloads_concurrently_decoded(self):
        codec = ClaimCheckCodec(max_inline_bytes=10)
        s3, body = _mock_s3_client()
        codec.session = _mock_session(s3)

        original_1 = _make_payload(b"data 1")
        original_2 = _make_payload(b"data 2")

        # Mock get_payload_from_s3 to return serialized original payloads by key
        async def mock_get_payload(key):
            if key == "key-1":
                return original_1.SerializeToString()
            if key == "key-2":
                return original_2.SerializeToString()
            return None

        codec.get_payload_from_s3 = mock_get_payload

        payload_1 = _make_payload(
            b"key-1",
            metadata={
                "encoding": b"claim-checked",
                "temporal.io/claim-check-codec": b"v1",
            },
        )
        payload_2 = _make_payload(
            b"key-2",
            metadata={
                "encoding": b"claim-checked",
                "temporal.io/claim-check-codec": b"v1",
            },
        )

        result = await codec.decode([payload_1, payload_2])

        assert len(result) == 2
        assert result[0].data == b"data 1"
        assert result[1].data == b"data 2"


class TestDecodeMissingKey:
    @pytest.mark.asyncio
    async def test_missing_key_raises_value_error(self):
        codec = ClaimCheckCodec()
        s3, body = _mock_s3_client()
        codec.session = _mock_session(s3)
        body.read.return_value = None

        # Patch get_payload_from_s3 to return None (key not found)
        codec.get_payload_from_s3 = AsyncMock(return_value=None)

        claim_check_payload = _make_payload(
            b"missing-key",
            metadata={
                "encoding": b"claim-checked",
                "temporal.io/claim-check-codec": b"v1",
            },
        )

        with pytest.raises(ValueError, match="Claim check key not found"):
            await codec.decode([claim_check_payload])
