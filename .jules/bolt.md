## 2025-05-18 - Reuse S3 client contexts across batch codec operations
**Learning:** Temporal `PayloadCodec` processes lists of payloads in `encode` and `decode`. Creating individual `aioboto3` client contexts per payload creates redundant HTTP client sessions and connection pool initializations.
**Action:** Always wrap batch codec processing loops (`encode`/`decode`) in a single client context manager and pass the active client instance into individual payload helper methods.
