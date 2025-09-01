# Benchmarks

Environment: macOS (Apple M2), Python 3.11, localhost (127.0.0.1)

This project measures round-trip latency (RTT) and approximate throughput of the Python TCP echo pair.
Client benchmark mode: `client.py --bench` (threaded server on 5050).  
Server: multi-threaded echo (`server.py`).  
Client: single TCP connection, repeated sends + echoes (`client.py`).  

---

## Method

1) Start the echo server on port 5050.
2) Run the client in `--bench` mode with a fixed message length and repeat count.
3) Report:
   - Average RTT (ms) across all repeats
   - p95 RTT (ms)
   - Aggregate throughput in MB/s over the whole run

---

## Results (localhost)

### 1 KB message (1024 bytes)

- Repeats: 2000  
- Avg RTT: 0.030 ms  
- p95 RTT: 0.053 ms  
- Throughput: 32.34 MB/s

---

## Reproduce

Server:

```bash
python3 server.py --host 0.0.0.0 --port 5050
```

Client (1 KB payload, 2000 repeats):

```bash
python3 client.py --host 127.0.0.1 --port 5050 --message "$(python3 -c "print('x'*1024)")" --bench --repeat 2000
```

---

## Notes & Interpretation

- Very low RTTs on loopback are expected (tens of microseconds to a few tenths of a millisecond).
- Throughput with small messages is lower because per-message overhead dominates; larger payloads usually increase MB/s by amortizing syscall and TCP overhead.
- The benchmark uses one TCP connection and measures application-level echo RTT, not raw kernel networking performance.
- Server implementation: thread-per-connection (simple, clear), suitable for a teaching/demo setup.

---

## Asyncio Server (localhost)

### 16 KB message (16384 bytes)

- Repeats: 1000
- Avg RTT: 0.089 ms
- p95 RTT: 0.122 ms
- Throughput: 172.61 MB/s

---

### Single-message example

- Message: 'hello-async'
- Observed RTT: ~5.543 ms

---

### How to reproduce (async)

Server:

```bash
python3 server_async.py --host 0.0.0.0 --port 5051
```

Client:

```bash
python3 client.py --host 127.0.0.1 --port 5051 --message 'hello-async'
```

Client (16 KB payload, 1000 repeats):

```bash
python3 client.py --host 127.0.0.1 --port 5051 --message "$(python3 -c "print('x'*16384)")" --bench --repeat 1000
```
