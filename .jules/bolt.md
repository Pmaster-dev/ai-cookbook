# Bolt's Journal - Critical Learnings

## 2025-05-10 - Temporal PayloadCodec Batch Optimization
**Learning:** Temporal `PayloadCodec.encode` and `PayloadCodec.decode` handle batches of payloads (`Iterable[Payload]`). Performing sequential async I/O calls for each payload in a loop creates an $N \times \text{RTT}$ latency bottleneck.
**Action:** Always process payload batches concurrently using `asyncio.gather` in Temporal PayloadCodec implementations to bound network latency to $1 \times \text{RTT}$.
