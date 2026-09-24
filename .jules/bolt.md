## 2025-05-18 - Top-k Retrieval Optimization with heapq.nlargest
**Learning:** For BM25 context chunk retrieval or score-based ranking, replacing `sorted(..., key=lambda i: scores[i], reverse=True)[:k]` with `heapq.nlargest(k, range(len(scores)), key=scores.__getitem__)` reduces complexity from $O(N \log N)$ to $O(N \log k)$ and avoids lambda lookup overhead.
**Action:** Use `heapq.nlargest` for top-k index retrieval over sequence scores when $k \ll N$.
