## 2025-05-18 - Concurrent Payload Processing in Temporal PayloadCodec
**Learning:** Sequential payload processing in Temporal `PayloadCodec` (`encode`/`decode`) causes serialized network I/O ($O(N \times \text{latency})$) when handling multiple activity or workflow arguments/results. Processing payloads concurrently with `asyncio.gather` reduces network latency to $O(\text{latency})$ while preserving order and exact return contracts.
**Action:** Always use `asyncio.gather` for payload list encoding/decoding in custom Temporal `PayloadCodec` implementations.
